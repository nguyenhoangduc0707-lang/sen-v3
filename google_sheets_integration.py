import gspread
from oauth2client.service_account import ServiceAccountCredentials
import sqlite3
import json
from datetime import datetime, timedelta
import time
import os

class GoogleSheetsIntegration:
    def __init__(self, credentials_file='google_credentials.json', sheet_name='DYT01_Content_Schedule'):
        # Kiểm tra file credentials
        if not os.path.exists(credentials_file):
            print(f'⚠️  File {credentials_file} not found!')
            print('   Using CSV fallback mode...')
            self.use_csv = True
            return
        
        self.use_csv = False
        try:
            scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
            creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
            self.client = gspread.authorize(creds)
            self.sheet = self.client.open(sheet_name).sheet1
            print('✅ Connected to Google Sheets!')
        except Exception as e:
            print(f'❌ Google Sheets connection failed: {e}')
            print('   Using CSV fallback mode...')
            self.use_csv = True
    
    def get_pending_posts(self):
        if self.use_csv:
            return self._get_posts_from_csv()
        return self._get_posts_from_sheets()
    
    def _get_posts_from_sheets(self):
        records = self.sheet.get_all_records()
        pending_posts = []
        
        for i, row in enumerate(records, start=2):
            if row.get('Status') == 'PENDING':
                pending_posts.append({
                    'row_num': i,
                    'time': row.get('Time', '09:00'),
                    'content': row.get('Content', ''),
                    'image_url': row.get('Image URL', ''),
                    'platform': row.get('Platform', 'facebook'),
                    'priority': int(row.get('Priority', 5))
                })
        return pending_posts
    
    def _get_posts_from_csv(self):
        pending_posts = []
        if not os.path.exists('posts_schedule.csv'):
            return pending_posts
        
        import csv
        with open('posts_schedule.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader, start=2):
                if row.get('Status') == 'PENDING':
                    pending_posts.append({
                        'row_num': i,
                        'time': row.get('Time', '09:00'),
                        'content': row.get('Content', ''),
                        'image_url': row.get('Image URL', ''),
                        'platform': row.get('Platform', 'facebook'),
                        'priority': int(row.get('Priority', 5))
                    })
        return pending_posts
    
    def update_status(self, row_num, status):
        if self.use_csv:
            print(f'   [CSV] Would update row {row_num} to {status}')
            return
        
        try:
            self.sheet.update(f'F{row_num}', status)
            print(f'✅ Updated row {row_num} to {status}')
        except Exception as e:
            print(f'⚠️  Could not update row {row_num}: {e}')

class DYT01TaskCreator:
    def __init__(self):
        self.conn = sqlite3.connect('app.db')
        self.cursor = self.conn.cursor()
    
    def create_task(self, post_data):
        now = datetime.now()
        hour, minute = map(int, post_data['time'].split(':'))
        scheduled = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        if scheduled < now:
            scheduled += timedelta(days=1)
        
        payload = {
            'content': post_data['content'],
            'platform': post_data['platform']
        }
        if post_data['image_url']:
            payload['image_url'] = post_data['image_url']
        
        self.cursor.execute('''
            INSERT INTO tasks (title, description, task_type, worker_name, status, priority, payload, scheduled_at, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            f'Bài đăng lúc {post_data["time"]}',
            f'Tự động tạo từ schedule',
            'facebook_post',
            'facebook_autoposter',
            'SCHEDULED',
            post_data['priority'],
            json.dumps(payload),
            scheduled.isoformat(),
            now.isoformat()
        ))
        
        task_id = self.cursor.lastrowid
        self.conn.commit()
        return task_id
    
    def close(self):
        self.conn.close()

def sync_from_sheets():
    print('\n🔄 Syncing...', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    sheets = GoogleSheetsIntegration()
    task_creator = DYT01TaskCreator()
    
    pending_posts = sheets.get_pending_posts()
    
    if not pending_posts:
        print('📭 No pending posts found')
        task_creator.close()
        return
    
    print(f'📋 Found {len(pending_posts)} pending posts')
    
    for post in pending_posts:
        try:
            task_id = task_creator.create_task(post)
            sheets.update_status(post['row_num'], 'SCHEDULED')
            print(f'✅ Created task #{task_id} for post at {post["time"]}')
        except Exception as e:
            print(f'❌ Error creating task: {e}')
    
    task_creator.close()
    print('✅ Sync completed!')

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--once':
        # Chạy một lần
        sync_from_sheets()
    else:
        # Chạy liên tục
        print('🚀 Starting Google Sheets sync service...')
        print('Will check for new posts every 5 minutes')
        print('Press Ctrl+C to stop\n')
        
        try:
            while True:
                sync_from_sheets()
                print('⏰ Waiting 5 minutes...\n')
                time.sleep(300)
        except KeyboardInterrupt:
            print('\n👋 Sync service stopped')
