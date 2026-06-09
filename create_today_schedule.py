import sqlite3
import json
from datetime import datetime, timedelta

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

now = datetime.now()
today = now.strftime('%Y-%m-%d')

# Các khung giờ trong ngày
time_slots = [
    ('08:00', '☕ Chào buổi sáng! Một ngày làm việc hiệu quả nhé!'),
    ('10:00', '💡 Mẹo vặt hữu ích cho công việc hàng ngày'),
    ('12:00', '🍱 Ăn trưa ngon miệng cùng gia đình!'),
    ('14:00', '📈 Cập nhật xu hướng mới nhất'),
    ('16:00', '🎯 Giải pháp tối ưu cho doanh nghiệp của bạn'),
    ('18:00', '🌇 Kết thúc ngày làm việc, thư giãn nào!'),
    ('20:00', '📺 Chương trình đặc biệt tối nay'),
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
            f'Tự động đăng lúc {time_str} ngày {today}',
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
print(f'\n📅 Created {created} posts for today ({today})')
