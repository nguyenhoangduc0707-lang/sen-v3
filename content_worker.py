"""
Content Worker - Xử lý task content creation
"""
import asyncio
import logging
import random
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ContentWorker:
    def __init__(self, worker_id: str = None):
        self.worker_id = worker_id or f"worker_{random.randint(1000, 9999)}"
        self.running = False
    
    async def process_task(self, task: dict):
        """Xử lý một task"""
        logger.info(f"[{self.worker_id}] Processing task: {task.get('task_type')}")
        
        # Simulate processing
        await asyncio.sleep(random.uniform(0.5, 2))
        
        # Return success
        return {
            "success": True,
            "worker_id": self.worker_id,
            "processed_at": datetime.now().isoformat()
        }
    
    async def run(self):
        """Main worker loop"""
        self.running = True
        logger.info(f"🚀 Worker {self.worker_id} started")
        
        while self.running:
            try:
                # Simulate getting task from queue
                # In real implementation, get from Redis/PostgreSQL
                task = {"task_type": "content_generation", "data": {}}
                
                result = await self.process_task(task)
                logger.debug(f"Task completed: {result}")
                
                await asyncio.sleep(5)  # Wait before next task
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                logger.error(f"Worker error: {e}")
                await asyncio.sleep(10)
        
        logger.info(f"🛑 Worker {self.worker_id} stopped")
    
    def stop(self):
        self.running = False


async def main():
    worker = ContentWorker()
    try:
        await worker.run()
    except KeyboardInterrupt:
        worker.stop()


if __name__ == "__main__":
    asyncio.run(main())
