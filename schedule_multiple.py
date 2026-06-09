import sqlite3
import json
from datetime import datetime, timedelta

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

# Danh sách bài đăng
posts = [
    ('09:00', '🌅 Chào buổi sáng! Một ngày mới tràn đầy năng lượng!'),
    ('12:00', '☕ Giờ nghỉ trưa, thư giãn cùng chúng tôi nhé!'),
    ('15:00', '🎯 Giải pháp tối ưu cho công việc của bạn'),
    ('18:00', '🌙 Kết thúc ngày làm việc, hẹn gặp lại ngày mai!'),
    ('21:00', '🌟 Tin vui cuối ngày - Ưu đãi đặc biệt!')
]

now = datetime.now()
created_tasks = []

for title, content in posts:
    hour, minute = map(int, title.split(':'))
    scheduled = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    
    # Nếu đã qua giờ thì lên lịch cho ngày mai
    if scheduled < now:
        scheduled += timedelta(days=1)
    
    cursor.execute('''
        INSERT INTO tasks (title, description, task_type, worker_name, status, priority, payload, scheduled_at, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        f'Bài đăng lúc {title}',
        f'Tự động đăng lúc {title}',
        'facebook_post',
        'facebook_autoposter',
        'SCHEDULED',
        5,
        json.dumps({'content': content + ' 🎉', 'platform': 'facebook'}),
        scheduled.isoformat(),
        now.isoformat()
    ))
    
    task_id = cursor.lastrowid
    created_tasks.append((task_id, title, scheduled))
    print(f'✓ Task #{task_id}: {title}')

conn.commit()
conn.close()

print(f'\n✅ Created {len(created_tasks)} scheduled posts!')
for task_id, title, scheduled in created_tasks:
    print(f'   #{task_id} at {scheduled.strftime("%Y-%m-%d %H:%M:%S")}')
