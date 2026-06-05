# web/routers/member_dashboard.py
"""
Member Dashboard - Hiển thị tasks và gợi ý AI Affiliate
Tích hợp Core Upgrade SEN V3
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict

from src.db.database import get_db
from src.db.models import User, Task, AIAffiliateProduct, UserRole
from src.auth.jwt import get_current_user

router = APIRouter(prefix="/api/v1/member", tags=["Member Dashboard"])


@router.get("/dashboard")
def get_member_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    🎯 Dashboard dành riêng cho Member
    
    Features:
    - Hiển thị các task đang chờ
    - Gợi ý công cụ AI affiliate dựa trên loại task
    - Hiển thị thông tin token còn lại
    """
    if current_user.role != UserRole.MEMBER:
        raise HTTPException(status_code=403, detail="Truy cập bị từ chối. Chức năng này chỉ dành cho Member.")
    
    # Lấy tasks đang pending
    pending_tasks = db.query(Task).filter(
        Task.assigned_to_id == current_user.id,
        Task.status == "PENDING"
    ).all()
    
    # Lấy tasks đang running
    running_tasks = db.query(Task).filter(
        Task.assigned_to_id == current_user.id,
        Task.status == "RUNNING"
    ).all()
    
    # Lấy completed tasks (7 ngày gần nhất)
    from datetime import datetime, timedelta
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    completed_tasks = db.query(Task).filter(
        Task.assigned_to_id == current_user.id,
        Task.status == "COMPLETED",
        Task.completed_at >= seven_days_ago
    ).all()
    
    # AI Smart Suggestions - dựa trên task types
    active_task_types = set([task.task_type for task in pending_tasks])
    
    ai_suggestions = []
    for task_type in active_task_types:
        products = db.query(AIAffiliateProduct).filter(
            AIAffiliateProduct.target_task_type == task_type,
            AIAffiliateProduct.is_active == True
        ).all()
        
        for product in products:
            ai_suggestions.append({
                "task_type": task_type,
                "notice": f"💡 Tăng tốc xử lý Task '{task_type}' với AI Tool chuyên nghiệp",
                "tool_name": product.name,
                "recommended_link": product.affiliate_link,
                "benefit_description": product.description,
                "commission_rate": f"{product.commission_rate * 100}%",
                "is_recurring_bonus": product.is_recurring,
                "stats": {
                    "clicks": product.total_clicks,
                    "conversions": product.total_conversions
                }
            })
    
    # Token usage status
    token_status = {
        "quota": current_user.token_quota,
        "used": current_user.tokens_used,
        "available": current_user.available_tokens,
        "usage_percent": current_user.token_usage_percent,
        "reset_date": current_user.token_reset_date
    }
    
    # Performance summary
    total_commission = sum(task.actual_commission for task in completed_tasks if task.actual_commission)
    avg_completion_time = sum(task.processing_time for task in completed_tasks) / len(completed_tasks) if completed_tasks else 0
    
    return {
        "member_info": {
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email,
            "joined_date": current_user.created_at
        },
        "tasks_summary": {
            "pending": len(pending_tasks),
            "running": len(running_tasks),
            "completed_7days": len(completed_tasks),
            "total_commission_7days": total_commission,
            "avg_completion_time_seconds": avg_completion_time
        },
        "pending_tasks_details": [
            {
                "id": task.id,
                "title": task.title,
                "task_type": task.task_type,
                "estimated_tokens": task.estimated_tokens,
                "expected_commission": task.expected_commission,
                "created_at": task.created_at
            }
            for task in pending_tasks
        ],
        "token_status": token_status,
        "admin_smart_ai_recommendations": ai_suggestions,
        "warning": None if current_user.available_tokens > 5000 else {
            "message": f"⚠️ Token sắp hết! Chỉ còn {current_user.available_tokens} tokens",
            "suggestion": "Liên hệ Admin để nạp thêm token hoặc sử dụng các công cụ AI được gợi ý bên trên"
        }
    }


@router.get("/analytics/my-performance")
def get_member_performance_analytics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """📊 Analytics chi tiết về performance của Member"""
    if current_user.role != UserRole.MEMBER:
        raise HTTPException(status_code=403, detail="Chỉ dành cho Member")
    
    from datetime import datetime, timedelta
    
    # Thống kê 30 ngày
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    
    tasks_30d = db.query(Task).filter(
        Task.assigned_to_id == current_user.id,
        Task.created_at >= thirty_days_ago
    ).all()
    
    completed_tasks_30d = [t for t in tasks_30d if t.status == "COMPLETED"]
    
    # Token efficiency
    total_estimated_tokens = sum(t.estimated_tokens for t in tasks_30d)
    total_actual_tokens = sum(t.actual_tokens_used for t in tasks_30d if t.actual_tokens_used)
    token_accuracy = (total_actual_tokens / total_estimated_tokens * 100) if total_estimated_tokens > 0 else 0
    
    # Commission earned
    commissions = db.query(CommissionLog).filter(
        CommissionLog.member_id == current_user.id,
        CommissionLog.created_at >= thirty_days_ago
    ).all()
    
    return {
        "period": "Last 30 days",
        "productivity": {
            "total_tasks_created": len(tasks_30d),
            "completed_tasks": len(completed_tasks_30d),
            "completion_rate": (len(completed_tasks_30d) / len(tasks_30d) * 100) if tasks_30d else 0,
            "avg_tasks_per_day": len(tasks_30d) / 30
        },
        "token_efficiency": {
            "estimated_tokens": total_estimated_tokens,
            "actual_tokens_used": total_actual_tokens,
            "accuracy": token_accuracy,
            "tokens_saved": total_estimated_tokens - total_actual_tokens
        },
        "earnings": {
            "total_commission": sum(c.total_commission for c in commissions),
            "member_share": sum(c.member_share_amount for c in commissions),
            "avg_commission_per_task": sum(c.member_share_amount for c in commissions) / len(commissions) if commissions else 0,
            "top_performing_task": max(commissions, key=lambda x: x.member_share_amount).task_id if commissions else None
        }
    }