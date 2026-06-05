# web/routers/ai_generate.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from src.db.database import get_db
from src.db.models import User, Task, TokenUsageHistory, UserRole
from src.auth.jwt import get_current_user

router = APIRouter(prefix="/api/v1/ai", tags=["AI Processing"])

class GenerateContentRequest(BaseModel):
    prompt: str = Field(..., min_length=10, max_length=5000)
    task_id: int
    model: str = "gemini-pro"
    temperature: float = 0.7

@router.post("/generate-content")
def generate_affiliate_content(
    request: GenerateContentRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate content with Gemini AI"""
    
    task = db.query(Task).filter(Task.id == request.task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if current_user.role not in [UserRole.MEMBER, UserRole.ADMIN]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    estimated_tokens = 2000
    
    available_tokens = current_user.token_quota - current_user.tokens_used
    if available_tokens < estimated_tokens:
        raise HTTPException(
            status_code=402,
            detail=f"Insufficient tokens. Need {estimated_tokens}, have {available_tokens}"
        )
    
    # Simulated response
    generated_content = f"Generated content for: {request.prompt}"
    
    current_user.tokens_used += estimated_tokens
    db.commit()
    
    return {
        "status": "success",
        "generated_content": generated_content,
        "tokens_used": estimated_tokens,
        "remaining_tokens": current_user.token_quota - current_user.tokens_used
    }

@router.post("/admin/token/topup")
def admin_topup_tokens(
    user_id: int,
    additional_tokens: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Admin: Add tokens to user"""
    
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin only")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.token_quota += additional_tokens
    db.commit()
    
    return {
        "status": "success",
        "user_id": user_id,
        "additional_tokens": additional_tokens,
        "new_quota": user.token_quota,
        "available_tokens": user.token_quota - user.tokens_used
    }
