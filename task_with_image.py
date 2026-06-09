import sqlite3
import json
from datetime import datetime

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

post_with_image = {
    'content': '🚀 SẢN PHẨM MỚI! \n\nKhám phá ngay tính năng tuyệt vời mà bạn không thể bỏ qua.\n\n✅ Chất lượng cao\n✅ Giá tốt nhất\n✅ Bảo hành 12 tháng\n\nLiên hệ ngay để được tư vấn!',
    'image_url': 'https://example.com/product-image.jpg',
    'platform': 'facebook',
    'call_to_action': 'Mua ngay'
}

cursor.execute('''
    INSERT INTO tasks (title, description, task_type, worker_name, status, priority, payload, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
''', (
    'Bài đăng có hình ảnh',
    'Facebook post with image',
    'facebook_post',
    'facebook_autoposter',
    'PENDING',
    10,
    json.dumps(post_with_image),
    datetime.now().isoformat()
))

task_id = cursor.lastrowid
conn.commit()
conn.close()

print(f'✅ Facebook task with image #{task_id} created!')
print('📸 Bài đăng sẽ kèm hình ảnh')
