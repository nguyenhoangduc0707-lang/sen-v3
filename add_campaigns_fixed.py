"""
Add campaigns to database correctly
"""
import sqlite3
from datetime import datetime

conn = sqlite3.connect('sen_v3.db')
cursor = conn.cursor()

# Kiểm tra cấu trúc bảng
cursor.execute("PRAGMA table_info(accesstrade_campaigns)")
columns = cursor.fetchall()
print("📋 Table structure:")
for col in columns:
    print(f"   {col[1]}: {col[2]}")

# Thêm campaigns (dùng text/id phù hợp)
campaigns = [
    ('shopee_affiliate', 'Shopee Việt Nam - Tiếp thị liên kết', 'N/A', 'E-COMMERCE', 'active'),
    ('vpbank_senid', 'VPBank SenID - Mở thẻ tín dụng online 10 phút', 'N/A', 'FINANCIAL SERVICES', 'active'),
    ('tpbank_creator', 'TPBank - Mở thẻ tín dụng', 'N/A', 'FINANCIAL SERVICES', 'active'),
]

for camp in campaigns:
    try:
        cursor.execute('''
            INSERT OR REPLACE INTO accesstrade_campaigns 
            (id, name, commission, category, status, synced_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (camp[0], camp[1], camp[2], camp[3], camp[4], datetime.now().isoformat()))
        print(f"✅ Added: {camp[1][:40]}")
    except Exception as e:
        print(f"❌ Error adding {camp[0]}: {e}")

conn.commit()
conn.close()

print("\n✅ Done!")
