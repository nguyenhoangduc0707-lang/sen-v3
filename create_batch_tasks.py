import sqlite3
import json
from datetime import datetime, timedelta

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

# Danh sách bài đăng mẫu
posts = [
    ('🌅 Buổi sáng', 'Chào buổi sáng! Một ngày mới tràn đầy năng lượng!', 5),
    ('💼 Giờ làm việc', 'Hãy làm việc hiệu quả và đạt được mục tiêu hôm nay!', 5),
    ('🍱 Giờ nghỉ trưa', 'Đừng quên ăn trưa đầy đủ dinh dưỡng nhé!', 5),
    ('🌇 Chiều tà', 'Kết thúc ngày làm việc, thời gian cho gia đình!', 5),
    ('🌙 Buổi tối', 'Chúc cả nhà một buổi tối ấm áp và hạnh phúc!', 5)
]

# Lên lịch cho ngày mai
tomorrow = datetime.now() + timedelta(days=1)
created = 0

for i, (title, content, priority) in enumerate(posts):
    scheduled = tomorrow.replace(hour=9 + i, minute=0, second=0, microsecond=0)
    
    cursor.execute('''
        INSERT INTO tasks (title, description, task_type, worker_name, status, priority, payload, scheduled_at, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        title,
        f'Bài đăng tự động lúc {scheduled.strftime("%H:%M")}',
        'facebook_post',
        'facebook_autoposter',
        'SCHEDULED',
        priority,
        json.dumps({'content': content, 'platform': 'facebook'}),
        scheduled.isoformat(),
        datetime.now().isoformat()
    ))
    created += 1
    print(f'✅ Scheduled: {title} at {scheduled.strftime("%H:%M")}')

conn.commit()
conn.close()
print(f'\n📅 Created {created} posts for tomorrow ({tomorrow.strftime("%Y-%m-%d")})')
