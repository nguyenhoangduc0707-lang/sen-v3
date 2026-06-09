import sqlite3
import json
from datetime import datetime, timedelta

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

tomorrow = datetime.now() + timedelta(days=1)

# Bài đăng cho ngày mai
posts = [
    ('08:30', '☕ Buổi sáng làm việc hiệu quả! Bắt đầu ngày mới nào!'),
    ('10:30', '💡 Mẹo vặt hữu ích cho công việc hàng ngày'),
    ('13:30', '🍵 Giải lao chiều - Thư giãn cùng chúng tôi'),
    ('16:30', '📈 Cập nhật xu hướng mới nhất'),
    ('20:00', '🎬 Video hấp dẫn trong ngày')
]

for time_str, content in posts:
    hour, minute = map(int, time_str.split(':'))
    scheduled = tomorrow.replace(hour=hour, minute=minute, second=0, microsecond=0)
    
    cursor.execute('''
        INSERT INTO tasks (title, description, task_type, worker_name, status, priority, payload, scheduled_at, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        f'Bài đăng {tomorrow.strftime("%d/%m")} lúc {time_str}',
        f'Tự động đăng ngày {tomorrow.strftime("%d/%m/%Y")}',
        'facebook_post',
        'facebook_autoposter',
        'SCHEDULED',
        5,
        json.dumps({'content': content, 'platform': 'facebook'}),
        scheduled.isoformat(),
        datetime.now().isoformat()
    ))
    print(f'✓ Scheduled: {time_str} - {content[:30]}...')

conn.commit()
conn.close()
print(f'\n✅ Created {len(posts)} posts for {tomorrow.strftime("%Y-%m-%d")}')
