# web/routers/auth.py
"""
Authentication API - Đăng nhập, đăng ký, refresh token
Tích hợp Core Upgrade
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional
from datetime import timedelta

from src.db.database import get_db
from src.db.models import User, UserRole
from src.auth.jwt import (
    authenticate_user, create_access_token, get_password_hash,
    get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])

# ========== PYDANTIC SCHEMAS ==========
class LoginRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)

class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    password: str = Field(..., min_length=6)
    full_name: Optional[str] = None
    affiliate_code: Optional[str] = None  # Mã giới thiệu từ Member

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = ACCESS_TOKEN_EXPIRE_MINUTES * 60

class UserInfoResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: Optional[str]
    role: str
    token_quota: int
    tokens_used: int
    available_tokens: int


# ========== API ENDPOINTS ==========
@router.post("/login", response_model=TokenResponse)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Đăng nhập hệ thống
    
    - Admin: Quản lý toàn bộ
    - Member: Xử lý tasks, nhận hoa hồng
    - User: Chỉ xem nội dung khóa học
    """
    user = authenticate_user(db, request.username, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.id})
    
    return TokenResponse(
        access_token=access_token,
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )


@router.post("/register", response_model=UserInfoResponse)
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db)
):
    """
    Đăng ký tài khoản mới (mặc định là USER_KHOAHOC)
    Có thể đăng ký làm Member nếu có mã giới thiệu từ Member khác
    """
    # Kiểm tra username tồn tại
    existing_user = db.query(User).filter(User.username == request.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # Kiểm tra email tồn tại
    existing_email = db.query(User).filter(User.email == request.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Xác định role
    role = UserRole.USER_KHOAHOC
    parent_admin_id = None
    
    # Nếu có affiliate_code, tìm member giới thiệu
    if request.affiliate_code:
        referrer = db.query(User).filter(
            User.username == request.affiliate_code,
            User.role == UserRole.MEMBER
        ).first()
        if referrer:
            role = UserRole.MEMBER  # Đăng ký trực tiếp làm Member
            parent_admin_id = referrer.parent_admin_id  # Member mới thuộc cùng Admin
        else:
            raise HTTPException(status_code=400, detail="Invalid affiliate code")
    
    # Tạo user mới
    new_user = User(
        username=request.username,
        email=request.email,
        hashed_password=get_password_hash(request.password),
        role=role,
        full_name=request.full_name,
        token_quota=50000 if role == UserRole.MEMBER else 10000,  # Member có quota cao hơn
        tokens_used=0,
        parent_admin_id=parent_admin_id,
        is_active=True
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return UserInfoResponse(
        id=new_user.id,
        username=new_user.username,
        email=new_user.email,
        full_name=new_user.full_name,
        role=new_user.role.value,
        token_quota=new_user.token_quota,
        tokens_used=new_user.tokens_used,
        available_tokens=new_user.available_tokens
    )


@router.get("/me", response_model=UserInfoResponse)
def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """Lấy thông tin user hiện tại"""
    return UserInfoResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        full_name=current_user.full_name,
        role=current_user.role.value,
        token_quota=current_user.token_quota,
        tokens_used=current_user.tokens_used,
        available_tokens=current_user.available_tokens
    )


@router.post("/refresh")
def refresh_token(
    current_user: User = Depends(get_current_user)
):
    """Refresh JWT token"""
    new_token = create_access_token(data={"sub": current_user.id})
    return TokenResponse(
        access_token=new_token,
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )