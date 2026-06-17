import time
import sys
import os
import logging
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

sys.path.insert(0, os.getcwd())

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("facebook_worker")

# Định nghĩa model cho bảng facebook_posts
Base = declarative_base()

class FacebookPost(Base):
    __tablename__ = 'facebook_posts'
    __table_args__ = {'autoload_with': create_engine('sqlite:///sen_v3.db')}

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
                # Query ORM
                task = session.query(FacebookPost).filter(
                    FacebookPost.status == "PENDING"
                ).first()
                
                if task:
                    logger.info(f"Processing post {task.id}")
                    task.status = "RUNNING"
                    session.commit()
                    
                    # TODO: Xử lý post lên Facebook
                    content = task.content if task.content else "[No content]"
                    logger.info(f"Content preview: {content[:100]}...")
                    
                    # Đánh dấu hoàn thành
                    task.status = "COMPLETED"
                    session.commit()
                    logger.info(f"Post {task.id} completed")
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