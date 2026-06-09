"""
Async Task Queue DB (Phase 2.5+)

Fully asynchronous version of TaskQueueDB.
Supports PostgreSQL with SKIP LOCKED and SQLite fallback.
"""

from datetime import datetime
from typing import Any, Dict, Optional
import json

from sqlalchemy import text, select, update, or_
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.config import settings
from src.db.models import Task, DeadLetter, ExecutionLog, Worker


MAX_RETRIES_DEFAULT = 3


def _get_async_engine(db_url: Optional[str] = None):
    url = db_url or settings.DATABASE_URL
    if url.startswith("sqlite:///"):
        url = url.replace("sqlite:///", "sqlite+aiosqlite:///", 1)
    elif url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+asyncpg://", 1)

    # Better pool settings for production
    engine_kwargs = {"echo": False}
    if "postgresql" in url:
        engine_kwargs.update({
            "pool_size": 10,
            "max_overflow": 20,
            "pool_pre_ping": True,
            "pool_recycle": 3600,
        })

    return create_async_engine(url, **engine_kwargs)


class AsyncTaskQueueDB:
    """Complete async task queue."""

    def __init__(self, db_url: Optional[str] = None):
        self.engine = _get_async_engine(db_url)
        self.async_session = async_sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

    async def add_task(
        self,
        category: Optional[str],
        worker_name: str,
        payload: Dict[str, Any],
        priority: int = 0,
        scheduled_at: Optional[datetime] = None,
    ) -> int:
        payload_str = json.dumps(payload) if payload else None
        async with self.async_session() as session:
            task = Task(
                title=category or f"task-{worker_name}",
                task_type="generic",
                category=category,
                worker_name=worker_name,
                payload=payload_str,
                status="PENDING",
                priority=priority,
                scheduled_at=scheduled_at,
                retries=0,
            )
            session.add(task)
            await session.commit()
            await session.refresh(task)
            return task.id

    async def claim_next_task(self, worker_name: str) -> Optional[Dict[str, Any]]:
        now = datetime.utcnow()
        async with self.async_session() as session:
            is_postgres = "postgresql" in str(self.engine.url)
            if is_postgres:
                stmt = (
                    select(Task)
                    .where(Task.status == "PENDING")
                    # # .where(or_(Task.scheduled_at.is_(None), Task.scheduled_at <= now))  # Táº¡m thá»i comment
                    .order_by(Task.priority.desc(), Task.created_at)
                    .limit(1)
                    .with_for_update(skip_locked=True)
                )
                result = await session.execute(stmt)
                task = result.scalar_one_or_none()
            else:
                stmt = (
                    select(Task)
                    .where(Task.status == "PENDING")
                    # .where(or_(Task.scheduled_at.is_(None), Task.scheduled_at <= now))
                    .order_by(Task.priority.desc(), Task.created_at)
                    .limit(1)
                )
                result = await session.execute(stmt)
                task = result.scalar_one_or_none()

            if not task:
                return None

            task.status = "RUNNING"
            task.worker_name = worker_name
            task.started_at = now
            await session.commit()
            await session.refresh(task)

            return {
                "id": task.id,
                "title": task.title,
                "category": task.category,
                "task_type": task.task_type,
                "worker_name": task.worker_name,
                "payload": json.loads(task.payload) if task.payload else {},
                "priority": task.priority,
                "status": task.status,
                "retries": task.retries,
                "created_at": task.created_at,
            }

    async def mark_completed(self, task_id: int) -> None:
        async with self.async_session() as session:
            task = await session.get(Task, task_id)
            if task:
                task.status = "COMPLETED"
                task.finished_at = datetime.utcnow()
                await session.commit()

    async def mark_failed(
        self, task_id: int, error_message: Optional[str] = None, max_retries: int = MAX_RETRIES_DEFAULT
    ) -> None:
        async with self.async_session() as session:
            task = await session.get(Task, task_id)
            if not task:
                return
            task.last_error = error_message
            if (task.retries or 0) < max_retries:
                task.retries = (task.retries or 0) + 1
                task.status = "PENDING"
                task.started_at = None
            else:
                dead = DeadLetter(
                    original_task_id=task.id,
                    category=task.category,
                    worker_name=task.worker_name,
                    payload=task.payload,
                    failure_reason=error_message,
                )
                session.add(dead)
                task.status = "FAILED"
                task.finished_at = datetime.utcnow()
            await session.commit()

    async def log_execution(self, task_id: Optional[int], worker_name: Optional[str], level: str, message: str) -> None:
        async with self.async_session() as session:
            log = ExecutionLog(task_id=task_id, worker_name=worker_name, log_level=level, message=message)
            session.add(log)
            await session.commit()

    async def close(self):
        await self.engine.dispose()

    # Alias methods for BaseWorker compatibility
    async def claim_task(self, worker_name: str):
        """Alias for claim_next_task"""
        return await self.claim_next_task(worker_name)

    async def complete_task(self, task_id: int):
        """Alias for mark_completed"""
        return await self.mark_completed(task_id)

    async def fail_task(self, task_id: int, reason: str = None):
        """Alias for mark_failed"""
        return await self.mark_failed(task_id, reason)
