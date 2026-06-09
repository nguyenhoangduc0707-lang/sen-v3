import sqlite3
import json
from datetime import datetime

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

# Tạo task cho content_creator worker
cursor.execute('''
    INSERT INTO tasks (title, description, task_type, worker_name, status, priority, payload, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
''', (
    'Tạo nội dung AI - Marketing',
    'Sinh bài viết marketing bằng AI',
    'content_generation',
    'content_creator',
    'PENDING',
    8,
    json.dumps({
        'topic': 'Lợi ích của AI trong Marketing',
        'tone': 'chuyên nghiệp',
        'length': 300,
        'keywords': ['AI', 'Marketing', 'Tự động hóa']
    }),
    datetime.now().isoformat()
))

task_id = cursor.lastrowid
conn.commit()
conn.close()

print(f'✅ AI Content Task #{task_id} created!')
print('🤖 Content creator worker sẽ xử lý task này')
