import time
import sqlite3
import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('affiliate_worker')

def run_affiliate_worker():
    logger.info("Affiliate Worker started (sync mode)")
    conn = sqlite3.connect('sen_v3.db')
    conn.row_factory = sqlite3.Row
    
    while True:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, title, task_type, status, payload 
                FROM tasks 
                WHERE task_type = 'affiliate' AND status = 'PENDING'
                ORDER BY id LIMIT 1
            """)
            task = cursor.fetchone()
            
            if task:
                task_id = task["id"]
                logger.info(f"Processing affiliate task {task_id}")
                cursor.execute("UPDATE tasks SET status = 'COMPLETED' WHERE id = ?", (task_id,))
                conn.commit()
                logger.info(f"Affiliate task {task_id} completed")
            else:
                time.sleep(5)
        except Exception as e:
            logger.error(f"Worker error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    run_affiliate_worker()
