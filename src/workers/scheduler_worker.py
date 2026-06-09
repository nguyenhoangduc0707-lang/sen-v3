"""
Scheduler Worker (Phase 3)

Scans the scheduled_tasks table every minute and enqueues due tasks
into the AsyncTaskQueueDB for processing by specialized workers
(FacebookWorker, AffiliateWorker, etc.).
"""

import asyncio
import logging
from datetime import datetime
from typing import List

from sqlalchemy import select, update
from src.db.models import ScheduledTask
from src.task_queue_db_async import AsyncTaskQueueDB

logger = logging.getLogger("scheduler")


class SchedulerWorker:
    """Worker responsible for checking due scheduled tasks and enqueuing them."""

    def __init__(self, queue: AsyncTaskQueueDB, check_interval: int = 60):
        self.queue = queue
        self.check_interval = check_interval  # seconds
        self.running = True
        self.logger = logger

    async def run(self):
        """Main loop - checks for due tasks every check_interval seconds."""
        self.logger.info("ðŸš€ SchedulerWorker started")
        self.logger.info(f"   Check interval: {self.check_interval}s")

        while self.running:
            try:
                due_tasks = await self._get_due_tasks()

                if due_tasks:
                    self.logger.info(f"Found {len(due_tasks)} due scheduled task(s)")

                    for st in due_tasks:
                        try:
                            # Enqueue into the main async task queue
                            task_id = await self.queue.add_task(
                                category=st.task_type,
                                worker_name=st.task_type,  # e.g. "post_to_page", "fetch_campaigns"
                                payload=st.data or {},
                                priority=st.priority or 0,
                            )

                            # Mark the scheduled task as processed
                            await self._mark_processed(st.id, task_id)

                            self.logger.info(
                                f"âœ… Enqueued scheduled_task#{st.id} "
                                f"(type={st.task_type}) -> main_task#{task_id}"
                            )

                        except Exception as e:
                            self.logger.error(f"Failed to enqueue scheduled_task#{st.id}: {e}")

                else:
                    self.logger.debug("No due scheduled tasks at this check")

                await asyncio.sleep(self.check_interval)

            except Exception as e:
                self.logger.error(f"Scheduler loop error: {e}", exc_info=True)
                await asyncio.sleep(self.check_interval)

    async def _get_due_tasks(self) -> List[ScheduledTask]:
        """Fetch unprocessed scheduled tasks that are due now."""
        async with self.queue.async_session() as session:
            result = await session.execute(
                select(ScheduledTask)
                .where(ScheduledTask.scheduled_at <= datetime.utcnow())
                .where(ScheduledTask.is_processed == False)
                .where(ScheduledTask.is_active == True)
                .order_by(ScheduledTask.scheduled_at.asc())
                .limit(100)  # Process in reasonable batches
            )
            return list(result.scalars().all())

    async def _mark_processed(self, scheduled_id: int, main_task_id: int):
        """Mark a scheduled task as processed and record the resulting task id."""
        async with self.queue.async_session() as session:
            await session.execute(
                update(ScheduledTask)
                .where(ScheduledTask.id == scheduled_id)
                .values(
                    is_processed=True,
                    processed_at=datetime.utcnow(),
                    task_id=main_task_id,
                )
            )
            await session.commit()

    def stop(self):
        """Gracefully stop the scheduler loop."""
        self.running = False
        self.logger.info("SchedulerWorker stop signal received")
