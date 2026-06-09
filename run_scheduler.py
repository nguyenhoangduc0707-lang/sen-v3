import asyncio
import sys
import os

sys.path.insert(0, os.getcwd())

from src.task_queue_db_async import AsyncTaskQueueDB
from src.workers.scheduler_worker import SchedulerWorker

async def main():
    print("🗓️ Starting Scheduler Worker...")
    queue = AsyncTaskQueueDB()  # Không cần initialize
    scheduler = SchedulerWorker(queue, check_interval=60)
    await scheduler.run()

if __name__ == "__main__":
    asyncio.run(main())
