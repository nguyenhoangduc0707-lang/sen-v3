import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class BaseWorker(ABC):
    """Base class for all workers"""
    
    def __init__(self, queue, worker_name: str):
        self.queue = queue
        self.worker_name = worker_name
        self.running = True
        self.logger = logging.getLogger(f"worker.{worker_name}")
    
    @abstractmethod
    async def process(self, task: Dict[str, Any]) -> bool:
        """Process a task. Return True if success."""
        pass
    
    async def run(self):
        """Main worker loop"""
        self.logger.info(f"Worker {self.worker_name} started")
        
        while self.running:
            try:
                task = await self.queue.claim_next_task(self.worker_name)
                if task:
                    self.logger.info(f"Processing task {task.get('id')}")
                    success = await self.process(task)
                    if success:
                        await self.queue.mark_completed(task["id"])
                        self.logger.info(f"Task {task.get('id')} completed")
                    else:
                        await self.queue.mark_failed(task["id"])
                        self.logger.error(f"Task {task.get('id')} failed")
                else:
                    await asyncio.sleep(5)
            except Exception as e:
                self.logger.error(f"Worker error: {e}")
                await asyncio.sleep(5)
    
    def stop(self):
        """Stop the worker"""
        self.running = False
        self.logger.info(f"Worker {self.worker_name} stopped")
