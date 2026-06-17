import sqlite3
import json
import random
from datetime import datetime

def add_affiliate_links():
    conn = sqlite3.connect('sen_v3.db')
    cursor = conn.cursor()
    
    print("🔗 THÊM LINK AFFILIATE VÀO TASK")
    print("="*50)
    
    # Lấy các task từ Foreplay chưa có link
    cursor.execute("""
        SELECT id, title, description, payload, created_at
        FROM tasks 
        WHERE task_type = 'content_facebook' 
        AND payload LIKE '%foreplay_url%'
        AND status = 'COMPLETED'
        AND (description NOT LIKE '%http%' OR description IS NULL)
        ORDER BY id DESC
        LIMIT 20
    """)
    tasks = cursor.fetchall()
    
    if not tasks:
        print("⚠️ Không tìm thấy task nào cần thêm link")
        return
    
    print(f"📋 Tìm thấy {len(tasks)} task từ Foreplay")
    
    # Link affiliate mẫu (thay bằng link thật từ AccessTrade sau)
    # Cấu trúc: https://<platform>.vn/<product>?aff=<id>
    affiliate_links = {
        'shopee': [
            'https://shopee.vn/product/12345?aff=123',
            'https://shopee.vn/product/67890?aff=456',
            'https://shopee.vn/product/11111?aff=789',
        ],
        'lazada': [
            'https://lazada.vn/products/abc123?aff=111',
            'https://lazada.vn/products/def456?aff=222',
        ],
        'tiki': [
            'https://tiki.vn/product/xyz789?aff=333',
            'https://tiki.vn/product/uvw456?aff=444',
        ]
    }
    
    all_links = []
    for platform, links in affiliate_links.items():
        all_links.extend(links)
    
    count = 0
    for task in tasks:
        task_id = task[0]
        title = task[1][:40]
        description = task[2] or ''
        payload = json.loads(task[3]) if task[3] else {}
        niche = payload.get('niche', 'general')
        
        # Chọn link ngẫu nhiên
        link = random.choice(all_links) if all_links else '#'
        
        # Tạo nội dung mới với link affiliate
        affiliate_text = f"\n\n🛒 Mua ngay tại đây: {link}\n💰 Hoa hồng hấp dẫn cho bạn!"
        
        # Cập nhật description
        new_description = description + affiliate_text
        
        cursor.execute("""
            UPDATE tasks 
            SET description = ?,
                payload = json_set(payload, '$.affiliate_link', ?)
            WHERE id = ?
        """, (new_description, link, task_id))
        
        count += 1
        print(f"   ✅ Task {task_id}: {title}... → {link[:30]}...")
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ Đã thêm link affiliate vào {count} task!")

if __name__ == "__main__":
    add_affiliate_links()
