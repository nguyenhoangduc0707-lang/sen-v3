# web/routers/commission.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from src.db.database import get_db
from src.db.models import User, Task, CommissionLog, UserRole
from src.auth.jwt import get_current_user

router = APIRouter(prefix="/api/v1/commission", tags=["Commission"])

class TaskCompleteRequest(BaseModel):
    total_commission: float
    admin_rate: Optional[float] = 0.10

@router.post("/tasks/{task_id}/complete")
def complete_task(
    task_id: int,
    payload: TaskCompleteRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(404, "Task not found")
    
    if current_user.role != UserRole.ADMIN and task.assigned_to_id != current_user.id:
        raise HTTPException(403, "Not authorized")
    
    admin_share = payload.total_commission * payload.admin_rate
    member_share = payload.total_commission - admin_share
    
    log = CommissionLog(
        member_id=task.assigned_to_id,
        task_id=task.id,
        total_commission=payload.total_commission,
        admin_share_amount=admin_share,
        member_share_amount=member_share,
        status="SETTLED"
    )
    
    task.status = "COMPLETED"
    task.completed_at = datetime.utcnow()
    
    db.add(log)
    db.commit()
    
    return {
        "status": "success",
        "task_id": task.id,
        "admin_share": admin_share,
        "member_share": member_share
    }
