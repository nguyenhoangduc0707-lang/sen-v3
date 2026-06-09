"""
Scheduler API (Phase 3)

Endpoints to create, list, and cancel scheduled tasks that will be
automatically picked up by the SchedulerWorker.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Any, Dict

from web.dependencies import get_current_user, get_db
from src.db.models import User, ScheduledTask
from src.db.crud import create_scheduled_task
from sqlalchemy import select, update

router = APIRouter(prefix="/schedules", tags=["Scheduler"])


class ScheduleCreate(BaseModel):
    task_type: str = Field(..., description="e.g. post_to_page, fetch_campaigns, update_commission")
    data: Dict[str, Any] = Field(..., description="Payload that will be passed to the worker")
    scheduled_at: datetime
    priority: int = Field(default=0, ge=0, le=2, description="0=normal, 1=high, 2=urgent")


class ScheduleResponse(BaseModel):
    id: int
    task_type: str
    data: Dict[str, Any]
    scheduled_at: datetime
    is_processed: bool
    is_active: bool
    priority: int
    created_by: Optional[int]
    processed_at: Optional[datetime]
    task_id: Optional[int]
    created_at: datetime


@router.post("/", response_model=ScheduleResponse, status_code=status.HTTP_201_CREATED)
async def create_schedule(
    schedule: ScheduleCreate,
    current_user: User = Depends(get_current_user),
    db=Depends(get_db),
):
    """Create a new scheduled task."""

    # Validation: scheduled_at must be in the future (handle both naive and aware datetimes from Pydantic/ISO)
    scheduled_at = schedule.scheduled_at
    if getattr(scheduled_at, "tzinfo", None) is not None:
        scheduled_at = scheduled_at.replace(tzinfo=None)
    if scheduled_at <= datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="scheduled_at must be in the future"
        )

    scheduled = create_scheduled_task(
        db=db,
        task_type=schedule.task_type,
        data=schedule.data,
        scheduled_at=schedule.scheduled_at,
        created_by=current_user.id,
        priority=schedule.priority,
    )

    return ScheduleResponse(
        id=scheduled.id,
        task_type=scheduled.task_type,
        data=scheduled.data or {},
        scheduled_at=scheduled.scheduled_at,
        is_processed=scheduled.is_processed,
        is_active=scheduled.is_active,
        priority=scheduled.priority,
        created_by=scheduled.created_by,
        processed_at=scheduled.processed_at,
        task_id=scheduled.task_id,
        created_at=scheduled.created_at,
    )


@router.get("/", response_model=List[ScheduleResponse])
async def list_schedules(
    current_user: User = Depends(get_current_user),
    db=Depends(get_db),
):
    """List all schedules belonging to the current user (or all for admin)."""

    query = select(ScheduledTask).order_by(ScheduledTask.scheduled_at.asc())

    if current_user.role != "admin":
        query = query.where(ScheduledTask.created_by == current_user.id)

    result = db.execute(query)
    schedules = result.scalars().all()

    return [
        ScheduleResponse(
            id=s.id,
            task_type=s.task_type,
            data=s.data or {},
            scheduled_at=s.scheduled_at,
            is_processed=s.is_processed,
            is_active=s.is_active,
            priority=s.priority,
            created_by=s.created_by,
            processed_at=s.processed_at,
            task_id=s.task_id,
            created_at=s.created_at,
        )
        for s in schedules
    ]


@router.delete("/{schedule_id}", status_code=status.HTTP_200_OK)
async def delete_schedule(
    schedule_id: int,
    current_user: User = Depends(get_current_user),
    db=Depends(get_db),
):
    """Soft-cancel a scheduled task (set is_active=False). Only owner or admin can cancel."""

    query = (
        update(ScheduledTask)
        .where(ScheduledTask.id == schedule_id)
        .where(ScheduledTask.is_active == True)
    )

    if current_user.role != "admin":
        query = query.where(ScheduledTask.created_by == current_user.id)

    result = db.execute(query.values(is_active=False))
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Schedule not found or already cancelled"
        )

    return {"status": "cancelled", "schedule_id": schedule_id}


@router.get("/{schedule_id}", response_model=ScheduleResponse)
async def get_schedule(
    schedule_id: int,
    current_user: User = Depends(get_current_user),
    db=Depends(get_db),
):
    """Get details of a specific schedule."""
    result = db.execute(
        select(ScheduledTask).where(ScheduledTask.id == schedule_id)
    )
    schedule = result.scalar_one_or_none()

    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")

    if current_user.role != "admin" and schedule.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    return ScheduleResponse(
        id=schedule.id,
        task_type=schedule.task_type,
        data=schedule.data or {},
        scheduled_at=schedule.scheduled_at,
        is_processed=schedule.is_processed,
        is_active=schedule.is_active,
        priority=schedule.priority,
        created_by=schedule.created_by,
        processed_at=schedule.processed_at,
        task_id=schedule.task_id,
        created_at=schedule.created_at,
    )


@router.put("/{schedule_id}", response_model=ScheduleResponse)
async def update_schedule(
    schedule_id: int,
    schedule_update: ScheduleCreate,
    current_user: User = Depends(get_current_user),
    db=Depends(get_db),
):
    """Update an existing schedule (only if not yet processed)."""
    result = db.execute(
        select(ScheduledTask).where(ScheduledTask.id == schedule_id)
    )
    schedule = result.scalar_one_or_none()

    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")

    if current_user.role != "admin" and schedule.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    if schedule.is_processed:
        raise HTTPException(status_code=400, detail="Cannot update a processed schedule")

    schedule.task_type = schedule_update.task_type
    schedule.data = schedule_update.data
    schedule.scheduled_at = schedule_update.scheduled_at
    schedule.priority = schedule_update.priority

    db.commit()
    db.refresh(schedule)

    return ScheduleResponse(
        id=schedule.id,
        task_type=schedule.task_type,
        data=schedule.data or {},
        scheduled_at=schedule.scheduled_at,
        is_processed=schedule.is_processed,
        is_active=schedule.is_active,
        priority=schedule.priority,
        created_by=schedule.created_by,
        processed_at=schedule.processed_at,
        task_id=schedule.task_id,
        created_at=schedule.created_at,
    )


@router.post("/{schedule_id}/pause", status_code=status.HTTP_200_OK)
async def pause_schedule(
    schedule_id: int,
    current_user: User = Depends(get_current_user),
    db=Depends(get_db),
):
    """Temporarily pause a schedule."""
    result = db.execute(
        select(ScheduledTask).where(ScheduledTask.id == schedule_id)
    )
    schedule = result.scalar_one_or_none()

    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")

    if current_user.role != "admin" and schedule.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    schedule.is_active = False
    db.commit()

    return {"status": "paused", "schedule_id": schedule_id}


@router.post("/{schedule_id}/resume", status_code=status.HTTP_200_OK)
async def resume_schedule(
    schedule_id: int,
    current_user: User = Depends(get_current_user),
    db=Depends(get_db),
):
    """Resume a paused schedule."""
    result = db.execute(
        select(ScheduledTask).where(ScheduledTask.id == schedule_id)
    )
    schedule = result.scalar_one_or_none()

    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")

    if current_user.role != "admin" and schedule.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    schedule.is_active = True
    db.commit()

    return {"status": "resumed", "schedule_id": schedule_id}
