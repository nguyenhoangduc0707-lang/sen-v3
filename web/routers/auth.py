from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from src.db.database import get_db
from src.db.models import User
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from src.auth.jwt import create_access_token

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    full_name: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

@router.post("/register")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    # Kiểm tra user đã tồn tại
    existing = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username or email already registered")

    # Tạo user mới
    hashed_password = pwd_context.hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {"username": db_user.username, "email": db_user.email, "id": db_user.id}

@router.post("/login")
async def login(login_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == login_data.username).first()
    if not user or not pwd_context.verify(login_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
