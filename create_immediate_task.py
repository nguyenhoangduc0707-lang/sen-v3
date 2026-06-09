import sqlite3
import json
from datetime import datetime

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

cursor.execute('''
    INSERT INTO tasks (title, description, task_type, worker_name, status, priority, payload, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
''', (
    'Task chạy ngay lập tức',
    'Task này sẽ được xử lý ngay khi worker rảnh',
    'facebook_post',
    'facebook_autoposter',
    'PENDING',
    10,
    json.dumps({'content': '🎉 Hệ thống DYT_01 đang hoạt động tốt! Bài đăng được xử lý ngay lập tức.'}),
    datetime.now().isoformat()
))

task_id = cursor.lastrowid
conn.commit()
conn.close()

print(f'✅ Immediate task #{task_id} created!')
print('📱 Watch Terminal 2 & 3 for processing')
