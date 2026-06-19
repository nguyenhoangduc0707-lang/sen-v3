from src.task_queue_db_async import AsyncTaskQueueDB
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from src.db.models import ScheduledTask
from datetime import datetime
import logging
import asyncio

logger = logging.getLogger(__name__)

class SchedulerWorker:
    def __init__(self, queue: AsyncTaskQueueDB, check_interval: int = 60):
        self.queue = queue
        self.engine = queue.engine
        self.check_interval = check_interval
        self.running = True

    async def run(self):
        """Vòng lặp chính của scheduler"""
        logger.info(f"Scheduler started with check_interval={self.check_interval}s")
        while self.running:
            try:
                await self._process_due_tasks()
            except Exception as e:
                logger.error(f"Scheduler error: {e}")
            await asyncio.sleep(self.check_interval)

    async def _process_due_tasks(self):
        """Lấy và xử lý các task đến hạn"""
        tasks = await self._get_due_tasks()
        if tasks:
            logger.info(f"Found {len(tasks)} due tasks")
            for task in tasks:
                # Gửi task vào hàng đợi chính (ví dụ)
                await self.queue.enqueue_task({
                    "type": task.task_type,
                    "data": task.data,
                    "scheduled_id": task.id
                })
                await self.mark_processed(task.id)

    async def _get_due_tasks(self, limit: int = 100):
        """Lấy các task đến hạn chưa xử lý"""
        async with AsyncSession(self.engine) as session:
            stmt = select(ScheduledTask).where(
                ScheduledTask.scheduled_at <= datetime.utcnow(),
                ScheduledTask.is_processed == False,
                ScheduledTask.is_active == True
            ).order_by(ScheduledTask.scheduled_at.asc()).limit(limit)
            result = await session.execute(stmt)
            return result.scalars().all()

    async def enqueue_task(self, task_type: str, data: dict, scheduled_at: datetime, priority: int = 0):
        """Thêm task mới vào hàng đợi"""
        async with AsyncSession(self.engine) as session:
            task = ScheduledTask(
                task_type=task_type,
                data=data,
                scheduled_at=scheduled_at,
                priority=priority,
                is_active=True,
                is_processed=False
            )
            session.add(task)
            await session.commit()
            return task.id

    async def mark_processed(self, task_id: int):
        """Đánh dấu task đã xử lý"""
        async with AsyncSession(self.engine) as session:
            stmt = update(ScheduledTask).where(
                ScheduledTask.id == task_id
            ).values(
                is_processed=True,
                processed_at=datetime.utcnow()
            )
            await session.execute(stmt)
            await session.commit()

    async def batch_processing(self, task_ids: list):
        """Xử lý hàng loạt task"""
        for tid in task_ids:
            await self.mark_processed(tid)

    def stop(self):
        """Dừng scheduler"""
        self.running = False