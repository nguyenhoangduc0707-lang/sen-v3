import sqlite3

conn = sqlite3.connect('sen_v3.db')
cursor = conn.cursor()

# Lấy financial campaigns
cursor.execute("SELECT id, name FROM accesstrade_campaigns WHERE category IN ('FINANCIAL SERVICES', '60', '35') ORDER BY id LIMIT 5")

rows = cursor.fetchall()

print("=" * 70)
print("🔗 NEW AFFILIATE LINKS (Thay thế link lỗi)")
print("=" * 70)

publisher_id = "6983938396644077046"

for row in rows:
    campaign_id = row[0]
    name = row[1][:50] if row[1] else "N/A"
    
    deep_link = f"https://go.isclix.com/deep_link/v5/{publisher_id}/{campaign_id}?sub4=sen_v3"
    
    print(f"\n📌 {name}")
    print(f"   Campaign ID: {campaign_id}")
    print(f"   Link: {deep_link}")

print("\n" + "=" * 70)
print("💡 Copy link và chia sẻ để nhận hoa hồng!")
print("=" * 70)

conn.close()
