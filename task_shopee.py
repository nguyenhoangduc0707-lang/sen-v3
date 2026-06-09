import sqlite3
import json
from datetime import datetime

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

affiliate_content = {
    'product': 'Tai nghe Bluetooth Sony WH-1000XM5',
    'price': '6,990,000đ',
    'commission': '8%',
    'shopee_link': 'https://shopee.vn/product/123456',
    'image_url': 'https://cf.shopee.vn/file/example.jpg',
    'description': 'Chất lượng âm thanh vượt trội, chống ồn hoàn hảo'
}

cursor.execute('''
    INSERT INTO tasks (title, description, task_type, worker_name, status, priority, payload, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
''', (
    'Affiliate - Tai nghe Sony',
    'Bài đăng affiliate Shopee',
    'affiliate_task',
    'shopee_affiliate',
    'PENDING',
    8,
    json.dumps(affiliate_content),
    datetime.now().isoformat()
))

task_id = cursor.lastrowid
conn.commit()
conn.close()

print(f'✅ Shopee Affiliate Task #{task_id} created!')
print('📱 Worker sẽ xử lý task này')
