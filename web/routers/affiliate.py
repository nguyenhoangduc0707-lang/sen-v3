"""
Affiliate Management API (Phase 2)
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

from web.dependencies import get_current_user, get_task_queue, get_db
from src.db.models import User
from src.task_queue_db import TaskQueueDB
from src.db.crud import create_scheduled_task

router = APIRouter(prefix="/affiliate", tags=["Affiliate"])


class CampaignFilter(BaseModel):
    limit: int = 20
    category: Optional[str] = None
    keyword: Optional[str] = None


class AffiliateLinkRequest(BaseModel):
    campaign_id: int
    url: str
    tracking_id: Optional[str] = None


@router.post("/campaigns/fetch")
async def fetch_campaigns(
    filters: CampaignFilter,
    current_user: User = Depends(get_current_user),
    queue: TaskQueueDB = Depends(get_task_queue),
):
    """Trigger fetching latest campaigns from AccessTrade."""
    task_id = queue.add_task(
        category="affiliate",
        worker_name="affiliate",
        payload={
            "type": "fetch_campaigns",
            "data": filters.dict(),
            "user_id": current_user.id,
        },
    )
    return {"task_id": task_id, "status": "queued", "message": "Campaign fetch enqueued"}


@router.post("/links")
async def create_affiliate_link(
    req: AffiliateLinkRequest,
    current_user: User = Depends(get_current_user),
    queue: TaskQueueDB = Depends(get_task_queue),
):
    """Create a tracking affiliate link."""
    task_id = queue.add_task(
        category="affiliate",
        worker_name="affiliate",
        payload={
            "type": "create_affiliate_link",
            "data": req.dict(),
            "user_id": current_user.id,
        },
    )
    return {"task_id": task_id, "status": "queued"}


@router.get("/campaigns")
async def get_campaigns(
    limit: int = 20,
    current_user: User = Depends(get_current_user),
):
    """Direct (sync for now) campaign list via the client."""
    from src.accesstrade_client import get_accesstrade_client

    client = await get_accesstrade_client()
    result = await client.get_campaigns(limit=limit)
    await client.close()
    return result


@router.post("/commission")
async def record_commission(
    data: dict,
    current_user: User = Depends(get_current_user),
    queue: TaskQueueDB = Depends(get_task_queue),
):
    """Record a commission event (usually called by conversion webhook)."""
    task_id = queue.add_task(
        category="affiliate",
        worker_name="affiliate",
        payload={
            "type": "update_commission",
            "data": data,
            "user_id": current_user.id,
        },
    )
    return {"task_id": task_id, "status": "recorded"}


@router.get("/commission")
async def get_commission_report(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: User = Depends(get_current_user),
):
    """Simple commission report for the current user (or all if admin)."""
    from src.db.session import get_session
    from src.db.models import CommissionLog
    from sqlalchemy import select, func

    with get_session() as db:
        query = select(CommissionLog)
        if current_user.role != "admin":
            query = query.where(CommissionLog.member_id == current_user.id)

        if start_date:
            query = query.where(CommissionLog.created_at >= start_date)
        if end_date:
            query = query.where(CommissionLog.created_at <= end_date)

        logs = db.execute(query).scalars().all()

    total = sum(l.total_commission for l in logs)
    return {
        "total_commission": total,
        "count": len(logs),
        "logs": [
            {
                "id": l.id,
                "total": l.total_commission,
                "admin_share": l.admin_share_amount,
                "member_share": l.member_share_amount,
                "status": l.status,
                "created_at": l.created_at,
            }
            for l in logs
        ],
    }
