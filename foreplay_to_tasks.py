import sqlite3
import json
from foreplay_api import ForeplayAPI
import os
from dotenv import load_dotenv

load_dotenv()

def safe_str(value, default=''):
    """Chuyển đổi an toàn, trả về chuỗi rỗng nếu None"""
    return value if value is not None else default

def create_tasks_from_foreplay():
    api = ForeplayAPI()
    conn = sqlite3.connect('sen_v3.db')
    cursor = conn.cursor()
    
    print("📥 TẠO TASK TỪ FOREPLAY")
    print("="*40)
    
    # Các niche có thể mở rộng
    niches = ['fashion', 'beauty', 'technology', 'sports', 'food', 'travel', 'fitness']
    
    count = 0
    for niche in niches:
        print(f"🔍 Lấy quảng cáo niche: {niche}")
        try:
            data = api.get_top_ads(niche=niche, limit=3)
        except Exception as e:
            print(f"   ❌ Lỗi API: {e}")
            continue
        
        if not data.get('data'):
            print(f"   ⚠️ Không có dữ liệu cho niche {niche}")
            continue
        
        for ad in data['data']:
            # Lấy các trường an toàn
            title = safe_str(ad.get('headline')) or safe_str(ad.get('name')) or f'Ad {niche}'
            brand = safe_str(ad.get('brand', {}).get('name')) if isinstance(ad.get('brand'), dict) else 'Unknown'
            description = safe_str(ad.get('description'))
            foreplay_url = safe_str(ad.get('foreplay_url'), '#')
            
            # Chuẩn bị payload
            payload = json.dumps({
                'foreplay_url': foreplay_url,
                'brand': brand,
                'niche': niche,
                'ad_name': ad.get('name', ''),
                'platform': ad.get('publisher_platform', 'unknown')
            }, ensure_ascii=False)
            
            # Tạo task
            cursor.execute("""
                INSERT INTO tasks (
                    title, description, task_type, status, priority, created_at, payload
                ) VALUES (
                    ?,
                    ?,
                    'content_facebook',
                    'PENDING',
                    1,
                    CURRENT_TIMESTAMP,
                    ?
                )
            """, (
                f"{title[:80]} - {brand}" if title else f"Ad from {niche}",
                f"Nội dung tham khảo từ Foreplay ({niche}): {description[:200]}" if description else f"Quảng cáo từ niche {niche}",
                payload
            ))
            count += 1
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ Đã thêm {count} task mới từ Foreplay!")

if __name__ == "__main__":
    create_tasks_from_foreplay()
