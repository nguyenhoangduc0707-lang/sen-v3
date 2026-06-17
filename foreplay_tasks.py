import sqlite3
import json
from foreplay_client import ForeplayClient
import os
from dotenv import load_dotenv

load_dotenv()

def create_tasks_from_foreplay():
    # Kết nối Foreplay
    api_key = os.getenv('FOREPLAY_API_KEY')
    if not api_key:
        print("❌ Chưa có FOREPLAY_API_KEY")
        return
    
    client = ForeplayClient(api_key)
    
    # Lấy quảng cáo hot
    print("🔍 Đang lấy quảng cáo hot từ Foreplay...")
    data = client.get_top_ads(limit=10)
    
    if not data.get('data'):
        print("❌ Không có dữ liệu")
        return
    
    # Kết nối database
    conn = sqlite3.connect('sen_v3.db')
    cursor = conn.cursor()
    
    count = 0
    for ad in data['data']:
        # Lấy thông tin
        title = ad.get('headline', ad.get('name', 'Quảng cáo hot'))
        description = ad.get('description', '')
        brand = ad.get('brand', {}).get('name', 'Unknown')
        
        # Tạo task
        cursor.execute("""
            INSERT INTO tasks (
                title, description, task_type, status, priority, created_at
            ) VALUES (
                ?, 
                'Lấy cảm hứng từ quảng cáo của ' || ? || ': ' || ?,
                'content_facebook',
                'PENDING',
                1,
                CURRENT_TIMESTAMP
            )
        """, (title, brand, description[:100]))
        
        count += 1
    
    conn.commit()
    conn.close()
    
    print(f"✅ Đã thêm {count} task mới từ quảng cáo hot của Foreplay!")

if __name__ == "__main__":
    create_tasks_from_foreplay()
