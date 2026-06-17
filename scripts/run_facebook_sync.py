import time
import sys
import os
import logging

sys.path.insert(0, os.getcwd())

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.db.models import Task

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("facebook_worker")

class SyncFacebookWorker:
    def __init__(self):
        self.engine = create_engine('sqlite:///sen_v3.db')
        self.Session = sessionmaker(bind=self.engine)
        self.running = True
    
    def run(self):
        logger.info("Facebook Worker started (sync mode)")
        while self.running:
            session = self.Session()
            try:
                task = session.query(Task).filter(Task.status == "PENDING").first()
                
                if task:
                    logger.info(f"Processing task {task.id}")
                    task.status = "RUNNING"
                    session.commit()
                    
                    # TODO: Xử lý task Facebook ở đây
                    # result = await self.poster.post_to_page(...)
                    
                    task.status = "COMPLETED"
                    session.commit()
                    logger.info(f"Task {task.id} completed")
                else:
                    time.sleep(5)
            except Exception as e:
                logger.error(f"Worker error: {e}")
                session.rollback()
                time.sleep(5)
            finally:
                session.close()

if __name__ == "__main__":
    print("🚀 Starting Facebook Worker (sync mode)...")
    worker = SyncFacebookWorker()
    worker.run()
