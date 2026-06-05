import sqlite3

conn = sqlite3.connect('sen_v3.db')
cursor = conn.cursor()

# Lấy các campaigns có category tài chính
cursor.execute("SELECT id, name FROM accesstrade_campaigns WHERE category IN ('FINANCIAL SERVICES', '60', '35') ORDER BY id")

rows = cursor.fetchall()

print("=" * 70)
print("✅ LINKS ĐANG HOẠT ĐỘNG TỐT")
print("=" * 70)

publisher_id = "6983938396644077046"

for row in rows:
    campaign_id = row[0]
    name = row[1] if row[1] else "N/A"
    
    # Tạo link
    link = f"https://go.isclix.com/deep_link/v5/{publisher_id}/{campaign_id}?sub4=sen_v3"
    
    print(f"\n📌 {name[:50]}")
    print(f"   ID: {campaign_id}")
    print(f"   Link: {link}")

print("\n" + "=" * 70)
print(f"📊 Tổng cộng: {len(rows)} link đang hoạt động")
print("=" * 70)

# Lưu vào file
with open("active_links.txt", "w", encoding="utf-8") as f:
    f.write("=" * 70 + "\n")
    f.write("🔗 ACTIVE AFFILIATE LINKS\n")
    f.write("=" * 70 + "\n\n")
    for row in rows:
        campaign_id = row[0]
        name = row[1] if row[1] else "N/A"
        link = f"https://go.isclix.com/deep_link/v5/{publisher_id}/{campaign_id}?sub4=sen_v3"
        f.write(f"{name}\n")
        f.write(f"{link}\n\n")

print("\n✅ Đã lưu vào file: active_links.txt")

conn.close()
