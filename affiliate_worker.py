import sqlite3
import json
from datetime import datetime
import time

class AffiliateWorker:
    def __init__(self):
        self.db_path = 'app.db'
    
    def process_pending_tasks(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, title, payload 
            FROM tasks 
            WHERE task_type = 'affiliate_post' 
            AND status = 'PENDING'
            ORDER BY priority DESC, created_at
            LIMIT 5
        ''')
        
        tasks = cursor.fetchall()
        
        for task_id, title, payload_str in tasks:
            print(f'🔄 Processing affiliate task #{task_id}: {title}')
            
            try:
                payload = json.loads(payload_str)
                content = payload.get('content', '')
                affiliate_link = payload.get('affiliate_link', '')
                
                print(f'   📝 Content preview: {content[:100]}...')
                print(f'   🔗 Link: {affiliate_link}')
                
                # TODO: Thực hiện đăng bài thực tế
                # Gọi Facebook API hoặc các nền tảng khác
                
                # Cập nhật trạng thái thành công
                cursor.execute('''
                    UPDATE tasks 
                    SET status = 'COMPLETED', 
                        completed_at = ?
                    WHERE id = ?
                ''', (datetime.now().isoformat(), task_id))
                
                print(f'   ✅ Task #{task_id} completed!')
                
            except Exception as e:
                print(f'   ❌ Task #{task_id} failed: {e}')
                cursor.execute('''
                    UPDATE tasks 
                    SET status = 'FAILED', 
                        last_error = ?
                    WHERE id = ?
                ''', (str(e), task_id))
            
            conn.commit()
        
        conn.close()
        return len(tasks)
    
    def run(self):
        print('🚀 Affiliate Worker Started')
        print('Checking for pending tasks every 30 seconds...\n')
        
        try:
            while True:
                count = self.process_pending_tasks()
                if count > 0:
                    print(f'📊 Processed {count} tasks\n')
                time.sleep(30)
        except KeyboardInterrupt:
            print('\n👋 Affiliate Worker stopped')

if __name__ == '__main__':
    worker = AffiliateWorker()
    worker.run()
