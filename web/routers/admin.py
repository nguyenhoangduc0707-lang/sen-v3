# web/routers/admin.py
"""
Admin Management APIs - Quản lý Member, Token, Commission
Chỉ dành cho Admin
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timedelta

from src.db.database import get_db
from src.db.models import User, Task, CommissionLog, AIAffiliateProduct, UserRole
from src.auth.jwt import get_current_admin

router = APIRouter(prefix="/api/v1/admin", tags=["Admin Management"])


# ========== PYDANTIC SCHEMAS ==========
class MemberCreateRequest(BaseModel):
    username: str = Field(..., min_length=3)
    email: str
    password: str = Field(..., min_length=6)
    full_name: Optional[str] = None
    token_quota: int = Field(50000, ge=1000, le=1000000)

class TokenTopupRequest(BaseModel):
    user_id: int
    additional_tokens: int = Field(..., gt=0, le=500000)
    reason: Optional[str] = None

class AffiliateProductCreate(BaseModel):
    name: str
    affiliate_link: str
    commission_rate: float = Field(0.20, ge=0, le=1)
    is_recurring: bool = True
    target_task_type: str
    description: Optional[str] = None


# ========== MEMBER MANAGEMENT ==========
@router.post("/members")
def create_member(
    request: MemberCreateRequest,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Tạo Member mới"""
    from src.auth.jwt import get_password_hash
    
    # Kiểm tra trùng lặp
    if db.query(User).filter(User.username == request.username).first():
        raise HTTPException(400, "Username already exists")
    if db.query(User).filter(User.email == request.email).first():
        raise HTTPException(400, "Email already exists")
    
    new_member = User(
        username=request.username,
        email=request.email,
        hashed_password=get_password_hash(request.password),
        role=UserRole.MEMBER,
        full_name=request.full_name,
        token_quota=request.token_quota,
        tokens_used=0,
        parent_admin_id=current_user.id,  # Member thuộc quản lý của Admin này
        is_active=True
    )
    
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    
    return {"message": "Member created successfully", "member_id": new_member.id}


@router.get("/members")
def list_members(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Danh sách Members (phân trang)"""
    query = db.query(User).filter(User.role == UserRole.MEMBER)
    
    if search:
        query = query.filter(
            (User.username.contains(search)) | (User.email.contains(search))
        )
    
    total = query.count()
    members = query.offset((page - 1) * limit).limit(limit).all()
    
    return {
        "total": total,
        "page": page,
        "limit": limit,
        "members": [
            {
                "id": m.id,
                "username": m.username,
                "email": m.email,
                "full_name": m.full_name,
                "token_quota": m.token_quota,
                "tokens_used": m.tokens_used,
                "available_tokens": m.available_tokens,
                "total_commission": sum(log.total_commission for log in m.commission_logs),
                "is_active": m.is_active,
                "created_at": m.created_at
            }
            for m in members
        ]
    }


# ========== TOKEN MANAGEMENT ==========
@router.post("/tokens/topup")
def topup_tokens(
    request: TokenTopupRequest,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Nạp token cho Member"""
    user = db.query(User).filter(User.id == request.user_id).first()
    if not user:
        raise HTTPException(404, "User not found")
    
    user.token_quota += request.additional_tokens
    
    # Ghi log nạp token (tùy chọn)
    from src.db.models import TokenUsageHistory
    log = TokenUsageHistory(
        user_id=user.id,
        tokens_used=request.additional_tokens,
        endpoint="/admin/tokens/topup",
        request_data=f"Admin {current_user.id}: {request.reason or 'No reason'}"
    )
    db.add(log)
    
    db.commit()
    
    return {
        "message": "Tokens topped up successfully",
        "user_id": user.id,
        "username": user.username,
        "additional_tokens": request.additional_tokens,
        "new_quota": user.token_quota,
        "available_tokens": user.available_tokens
    }


# ========== COMMISSION & REVENUE ==========
@router.get("/dashboard/stats")
def admin_dashboard_stats(
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Admin Dashboard - Thống kê toàn hệ thống"""
    
    # Thống kê Users
    total_members = db.query(User).filter(User.role == UserRole.MEMBER).count()
    total_users = db.query(User).filter(User.role == UserRole.USER_KHOAHOC).count()
    active_members = db.query(User).filter(
        User.role == UserRole.MEMBER,
        User.is_active == True
    ).count()
    
    # Thống kê Commission (30 ngày)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    commissions_30d = db.query(CommissionLog).filter(
        CommissionLog.created_at >= thirty_days_ago
    ).all()
    
    total_revenue_30d = sum(c.total_commission for c in commissions_30d)
    admin_income_30d = sum(c.admin_share_amount for c in commissions_30d)
    member_payout_30d = sum(c.member_share_amount for c in commissions_30d)
    
    # Thống kê Tasks
    tasks_30d = db.query(Task).filter(Task.created_at >= thirty_days_ago).all()
    completed_tasks = [t for t in tasks_30d if t.status == "COMPLETED"]
    
    # Thống kê Token
    total_tokens_allocated = db.query(func.sum(User.token_quota)).scalar() or 0
    total_tokens_used = db.query(func.sum(User.tokens_used)).scalar() or 0
    
    # Top Members by commission
    top_members = db.query(
        User.id,
        User.username,
        func.sum(CommissionLog.member_share_amount).label('total_earned')
    ).join(CommissionLog).filter(
        CommissionLog.created_at >= thirty_days_ago
    ).group_by(User.id).order_by(desc('total_earned')).limit(5).all()
    
    return {
        "users_summary": {
            "total_members": total_members,
            "active_members": active_members,
            "total_regular_users": total_users,
            "member_activation_rate": (active_members / total_members * 100) if total_members > 0 else 0
        },
        "revenue_summary": {
            "total_revenue_30d": total_revenue_30d,
            "admin_passive_income": admin_income_30d,
            "member_payout": member_payout_30d,
            "admin_profit_margin": (admin_income_30d / total_revenue_30d * 100) if total_revenue_30d > 0 else 0
        },
        "tasks_summary": {
            "total_tasks_30d": len(tasks_30d),
            "completed_tasks": len(completed_tasks),
            "completion_rate": (len(completed_tasks) / len(tasks_30d) * 100) if tasks_30d else 0
        },
        "token_summary": {
            "total_allocated": total_tokens_allocated,
            "total_used": total_tokens_used,
            "remaining_tokens": total_tokens_allocated - total_tokens_used,
            "usage_percent": (total_tokens_used / total_tokens_allocated * 100) if total_tokens_allocated > 0 else 0
        },
        "top_performing_members": [
            {"id": m.id, "username": m.username, "earned_30d": float(m.total_earned)}
            for m in top_members
        ]
    }


# ========== AFFILIATE PRODUCT MANAGEMENT ==========
@router.post("/affiliate-products")
def create_affiliate_product(
    request: AffiliateProductCreate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Thêm sản phẩm AI Affiliate mới"""
    product = AIAffiliateProduct(
        name=request.name,
        affiliate_link=request.affiliate_link,
        commission_rate=request.commission_rate,
        is_recurring=request.is_recurring,
        target_task_type=request.target_task_type,
        description=request.description,
        is_active=True
    )
    
    db.add(product)
    db.commit()
    db.refresh(product)
    
    return {"message": "Product created", "product_id": product.id}


@router.get("/affiliate-products")
def list_affiliate_products(
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Danh sách sản phẩm AI Affiliate"""
    products = db.query(AIAffiliateProduct).all()
    
    return {
        "products": [
            {
                "id": p.id,
                "name": p.name,
                "commission_rate": p.commission_rate,
                "is_recurring": p.is_recurring,
                "target_task_type": p.target_task_type,
                "total_clicks": p.total_clicks,
                "total_conversions": p.total_conversions,
                "estimated_revenue": p.total_revenue,
                "is_active": p.is_active
            }
            for p in products
        ]
    }