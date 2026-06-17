import time
import sys
import os
import logging
from datetime import datetime
from sqlalchemy import create_engine, text

sys.path.insert(0, os.getcwd())

from sqlalchemy.orm import sessionmaker

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
                # Dùng text() cho SQL thuần
                result = session.execute(
                    text("SELECT id, status, content, scheduled_at FROM facebook_posts WHERE status = 'PENDING' LIMIT 1")
                )
                task = result.fetchone()
                
                if task:
                    logger.info(f"Processing post {task[0]}")
                    # Update status
                    session.execute(
                        text("UPDATE facebook_posts SET status = 'RUNNING' WHERE id = :id"),
                        {"id": task[0]}
                    )
                    session.commit()
                    
                    # TODO: Xử lý post lên Facebook
                    content = task[2] if task[2] else "[No content]"
                    logger.info(f"Content preview: {content[:100]}...")
                    
                    # Update thành công
                    session.execute(
                        text("UPDATE facebook_posts SET status = 'COMPLETED' WHERE id = :id"),
                        {"id": task[0]}
                    )
                    session.commit()
                    logger.info(f"Post {task[0]} completed")
                else:
                    logger.info("No pending posts, waiting...")
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
