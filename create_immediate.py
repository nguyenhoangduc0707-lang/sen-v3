import sqlite3
import json
from datetime import datetime

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

cursor.execute('''
    INSERT INTO tasks (title, description, task_type, worker_name, status, priority, payload, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
''', (
    'Bài đăng ngay lập tức',
    'Task sẽ được xử lý ngay',
    'facebook_post',
    'facebook_autoposter',
    'PENDING',
    10,
    json.dumps({'content': '🎉 Bài đăng được tạo và xử lý ngay lập tức!', 'platform': 'facebook'}),
    datetime.now().isoformat()
))

task_id = cursor.lastrowid
conn.commit()
conn.close()

print(f'✅ Task #{task_id} created - will run immediately!')
print('📱 Watch Terminal 2 & 3 for processing')
