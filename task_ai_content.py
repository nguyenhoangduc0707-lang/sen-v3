import sqlite3
import json
from datetime import datetime

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

content_task = {
    'topic': 'Lợi ích của AI trong Marketing',
    'tone': 'chuyên nghiệp',
    'keywords': ['AI', 'Marketing', 'Tự động hóa', 'Facebook'],
    'target_length': 300
}

cursor.execute('''
    INSERT INTO tasks (title, description, task_type, worker_name, status, priority, payload, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
''', (
    'Tạo nội dung AI - Marketing',
    'Sinh bài viết về AI Marketing',
    'content_generation',
    'content_creator',
    'PENDING',
    8,
    json.dumps(content_task),
    datetime.now().isoformat()
))

task_id = cursor.lastrowid
conn.commit()
conn.close()

print(f'✅ AI Content Task #{task_id} created!')
print('🤖 Content creator worker sẽ tạo nội dung')
