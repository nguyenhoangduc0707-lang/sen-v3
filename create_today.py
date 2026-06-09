import sqlite3
import json
from datetime import datetime, timedelta

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

now = datetime.now()
print(f'\n📅 Creating posts for: {now.strftime("%Y-%m-%d")}')
print('=' * 50)

# Các khung giờ trong ngày
slots = [
    ('01:00', '🌙 Đã khuya rồi, ngủ ngon nhé!'),
    ('02:00', '💤 Giấc ngủ ngon cho ngày mai tràn đầy năng lượng'),
    ('06:00', '🌅 Bình minh! Chào ngày mới tràn đầy năng lượng!'),
    ('08:00', '☕ Buổi sáng làm việc hiệu quả!'),
    ('12:00', '🍱 Ăn trưa ngon miệng nhé cả nhà!'),
    ('14:00', '💡 Giải pháp tối ưu cho công việc'),
    ('17:00', '🌇 Chiều tà - Thư giãn cùng gia đình'),
    ('20:00', '📺 Chương trình đặc biệt tối nay!'),
    ('22:00', '🌙 Chúc cả nhà ngủ ngon!')
]

created = 0
for time_str, content in slots:
    hour, minute = map(int, time_str.split(':'))
    scheduled = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    
    if scheduled < now:
        print(f'⏭️  Skip {time_str} (đã qua)')
        continue
    
    cursor.execute('''
        INSERT INTO tasks (title, description, task_type, worker_name, status, priority, payload, scheduled_at, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        f'TODAY {time_str}',
        f'Bài đăng tự động lúc {time_str}',
        'facebook_post',
        'facebook_autoposter',
        'SCHEDULED',
        5,
        json.dumps({'content': content, 'platform': 'facebook'}),
        scheduled.isoformat(),
        now.isoformat()
    ))
    created += 1
    print(f'✅ {time_str} - {content[:30]}...')

conn.commit()
conn.close()
print(f'\n✨ Đã tạo {created} bài đăng cho hôm nay!')
