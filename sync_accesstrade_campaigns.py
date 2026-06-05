"""
Sync AccessTrade campaigns to database
"""
import requests
import sqlite3
import json
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

access_key = os.getenv("ACCESSTRADE_ACCESS_KEY")
headers = {"Authorization": f"Token {access_key}"}

print("=" * 60)
print("🔄 Syncing AccessTrade Campaigns to Database")
print("=" * 60)

# Lấy campaigns từ API
response = requests.get(
    "https://api.accesstrade.vn/v1/campaigns",
    headers=headers,
    params={"limit": 50}
)

if response.status_code != 200:
    print(f"❌ Failed to fetch campaigns: {response.status_code}")
    exit(1)

data = response.json()
campaigns = data.get('data', [])

print(f"\n✅ Fetched {len(campaigns)} campaigns from API")

# Kết nối database
conn = sqlite3.connect('sen_v3.db')
cursor = conn.cursor()

# Tạo bảng campaigns nếu chưa có
cursor.execute('''
    CREATE TABLE IF NOT EXISTS accesstrade_campaigns (
        id INTEGER PRIMARY KEY,
        name TEXT,
        commission TEXT,
        category TEXT,
        approval TEXT,
        cookie_duration INTEGER,
        status TEXT DEFAULT 'active',
        synced_at TIMESTAMP
    )
''')

# Insert/Update campaigns
for camp in campaigns:
    cursor.execute('''
        INSERT OR REPLACE INTO accesstrade_campaigns 
        (id, name, commission, category, approval, cookie_duration, synced_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        camp.get('id'),
        camp.get('name'),
        camp.get('commission'),
        camp.get('category'),
        camp.get('approval'),
        camp.get('cookie_duration'),
        datetime.now().isoformat()
    ))

conn.commit()

# Thống kê
cursor.execute('SELECT COUNT(*) FROM accesstrade_campaigns')
count = cursor.fetchone()[0]

print(f"✅ Saved {count} campaigns to database")

# Hiển thị danh sách campaigns đã lưu
cursor.execute('''
    SELECT id, name, commission, synced_at 
    FROM accesstrade_campaigns 
    ORDER BY id 
    LIMIT 15
''')

print("\n📋 Campaigns in Database:")
for row in cursor.fetchall():
    print(f"   {row[0]}. {row[1][:50]} - Commission: {row[2] or 'N/A'}%")

conn.close()

print("\n" + "=" * 60)
print("✅ Sync completed!")
