"""
Add campaigns with numeric IDs
"""
import sqlite3
from datetime import datetime

conn = sqlite3.connect('sen_v3.db')
cursor = conn.cursor()

# Lấy ID lớn nhất hiện tại
cursor.execute('SELECT MAX(id) FROM accesstrade_campaigns')
max_id = cursor.fetchone()[0] or 0
print(f"📊 Current max ID: {max_id}")

# Thêm campaigns với ID số
campaigns = [
    (max_id + 1, 'Shopee Việt Nam - Tiếp thị liên kết', 'N/A', 'E-COMMERCE', 'active'),
    (max_id + 2, 'VPBank SenID - Mở thẻ tín dụng online 10 phút', 'N/A', 'FINANCIAL SERVICES', 'active'),
    (max_id + 3, 'TPBank - Mở thẻ tín dụng', 'N/A', 'FINANCIAL SERVICES', 'active'),
]

for camp in campaigns:
    try:
        cursor.execute('''
            INSERT OR IGNORE INTO accesstrade_campaigns 
            (id, name, commission, category, status, synced_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (camp[0], camp[1], camp[2], camp[3], camp[4], datetime.now().isoformat()))
        print(f"✅ Added ID {camp[0]}: {camp[1][:40]}")
    except Exception as e:
        print(f"❌ Error: {e}")

conn.commit()

# Kiểm tra
cursor.execute('SELECT COUNT(*) FROM accesstrade_campaigns')
count = cursor.fetchone()[0]
print(f"\n📊 Total campaigns: {count}")

conn.close()
