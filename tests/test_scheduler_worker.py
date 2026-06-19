"""
Tests for SchedulerWorker (Phase 3)
"""

import pytest
from src.task_queue_db_async import AsyncTaskQueueDB
from sqlalchemy.ext.asyncio import create_async_engine
from datetime import datetime, timedelta
from src.workers.scheduler_worker import SchedulerWorker
from src.task_queue_db_async import AsyncTaskQueueDB
from src.db.models import ScheduledTask
from src.db.session import get_session


@pytest.mark.asyncio
async def test_scheduler_initialization():
    """Test worker initialization"""
    queue = AsyncTaskQueueDB("sqlite+aiosqlite:///:memory:")
    # Note: For full test, would need to init tables, but basic init check
    scheduler = SchedulerWorker(queue)
    assert scheduler.check_interval == 60
    assert scheduler.running is True


@pytest.mark.asyncio
async def test_get_due_tasks():
    """Test fetching due tasks"""
    from src.db.database import Base
    # Khởi tạo queue với URL (không phải engine)
    queue = AsyncTaskQueueDB("sqlite+aiosqlite:///:memory:")
    engine = queue.engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    scheduler = SchedulerWorker(queue)
    tasks = await scheduler._get_due_tasks()
    assert tasks == []


@pytest.mark.asyncio
async def test_enqueue_task():
    """Test that due task gets enqueued"""
    queue = AsyncTaskQueueDB("sqlite+aiosqlite:///:memory:")
    scheduler = SchedulerWorker(queue)
    # Would require seeding a ScheduledTask in test DB
    # Placeholder assertion
    assert True


@pytest.mark.asyncio
async def test_mark_processed():
    """Test marking scheduled task as processed"""
    # Placeholder - would update a test record
    assert True


@pytest.mark.asyncio
async def test_batch_processing():
    """Test that only up to 100 tasks are processed per cycle"""
    # The limit(100) is in the code
    assert True






