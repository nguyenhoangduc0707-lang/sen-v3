import asyncio
import sys
import os
import logging

sys.path.insert(0, os.getcwd())

from src.task_queue_db_async import AsyncTaskQueueDB

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("facebook_worker")

class SimpleFacebookWorker:
    def __init__(self, queue):
        self.queue = queue
        self.running = True
    
    async def run(self):
        logger.info("Facebook Worker started")
        while self.running:
            task = await self.queue.claim_next_task("facebook")
            if task:
                logger.info(f"Processing task {task.get('id')}")
                # TODO: Xử lý task
                await self.queue.mark_completed(task["id"])
                logger.info(f"Task {task.get('id')} completed")
            else:
                await asyncio.sleep(5)

async def main():
    print("🚀 Starting Facebook Worker...")
    queue = AsyncTaskQueueDB()
    worker = SimpleFacebookWorker(queue)
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
