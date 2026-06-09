import sqlite3
import json
from datetime import datetime, timedelta

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

# Lên lịch bài đăng cho 1 giờ nữa
scheduled_time = datetime.now() + timedelta(hours=1)

content = f'''📢 THÔNG BÁO LỊCH ĐĂNG BÀI

Bài đăng này sẽ được đăng tự động vào lúc: 
{scheduled_time.strftime('%H:%M:%S')}

Hệ thống DYT_01 - Tự động hóa marketing! 🚀'''

cursor.execute('''
    INSERT INTO tasks (title, description, task_type, worker_name, status, priority, payload, scheduled_at, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
''', (
    'Bài đăng đã lên lịch',
    'Tự động đăng theo lịch trình',
    'facebook_post',
    'facebook_autoposter',
    'SCHEDULED',
    7,
    json.dumps({'content': content, 'platform': 'facebook'}),
    scheduled_time.isoformat(),
    datetime.now().isoformat()
))

task_id = cursor.lastrowid
conn.commit()
conn.close()

print(f'✅ Scheduled Task #{task_id} created!')
print(f'📅 Will be posted at: {scheduled_time.strftime("%Y-%m-%d %H:%M:%S")}')
