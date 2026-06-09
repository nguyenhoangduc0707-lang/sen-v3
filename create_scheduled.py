import sqlite3
import json
from datetime import datetime, timedelta

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

now = datetime.now()
today = now.strftime('%Y-%m-%d')

# Các khung giờ
time_slots = [
    ('09:00', '🌅 Chào buổi sáng! Bắt đầu ngày mới nào!'),
    ('12:00', '🍱 Ăn trưa ngon miệng nhé cả nhà!'),
    ('15:00', '☕ Giải lao chiều cùng một ly cà phê!'),
    ('18:00', '🌇 Kết thúc ngày làm việc, thư giãn thôi!'),
    ('21:00', '🌙 Chúc cả nhà ngủ ngon!')
]

created = 0
for time_str, content in time_slots:
    hour, minute = map(int, time_str.split(':'))
    scheduled = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    
    if scheduled > now:
        cursor.execute('''
            INSERT INTO tasks (title, description, task_type, worker_name, status, priority, payload, scheduled_at, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            f'Bài đăng {time_str}',
            f'Tự động đăng lúc {time_str}',
            'facebook_post',
            'facebook_autoposter',
            'SCHEDULED',
            5,
            json.dumps({'content': content, 'platform': 'facebook'}),
            scheduled.isoformat(),
            now.isoformat()
        ))
        created += 1
        print(f'✅ Scheduled: {time_str}')

conn.commit()
conn.close()
print(f'\n📅 Created {created} scheduled posts for today ({today})')
