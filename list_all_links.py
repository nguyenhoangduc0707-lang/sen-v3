"""
Tổng hợp tất cả link affiliate đang hoạt động
"""
import sqlite3

conn = sqlite3.connect('sen_v3.db')
cursor = conn.cursor()

# Lấy tất cả financial campaigns
cursor.execute("SELECT id, name, category FROM accesstrade_campaigns WHERE category IN ('FINANCIAL SERVICES', '60', '35') ORDER BY id")

rows = cursor.fetchall()

publisher_id = "6983938396644077046"

print("=" * 80)
print("🔗 DANH SÁCH LINK AFFILIATE ĐANG HOẠT ĐỘNG")
print("=" * 80)

links = []

for row in rows:
    campaign_id = row[0]
    name = row[1] if row[1] else "N/A"
    category = row[2] if row[2] else "N/A"
    
    deep_link = f"https://go.isclix.com/deep_link/v5/{publisher_id}/{campaign_id}?sub4=sen_v3"
    links.append(deep_link)
    
    print(f"\n📌 {name}")
    print(f"   ID: {campaign_id}")
    print(f"   Category: {category}")
    print(f"   Link: {deep_link}")

# Lưu vào file
with open("all_active_links.txt", "w", encoding="utf-8") as f:
    f.write("=" * 80 + "\n")
    f.write("🔗 ALL ACTIVE AFFILIATE LINKS\n")
    f.write("=" * 80 + "\n\n")
    for i, link in enumerate(links, 1):
        f.write(f"{i}. {link}\n")

print("\n" + "=" * 80)
print(f"✅ Tổng cộng: {len(links)} link đang hoạt động")
print(f"📁 Đã lưu vào file: all_active_links.txt")
print("=" * 80)

conn.close()
