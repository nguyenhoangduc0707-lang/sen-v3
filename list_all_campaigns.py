"""
List all campaigns in database
"""
import sqlite3

conn = sqlite3.connect('sen_v3.db')
cursor = conn.cursor()

# Kiểm tra bảng tồn tại
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='accesstrade_campaigns'")
if not cursor.fetchone():
    print("❌ Table 'accesstrade_campaigns' not found!")
    print("   Run 'python fix_table_schema.py' first")
    conn.close()
    exit(1)

# Lấy tất cả campaigns
cursor.execute('SELECT id, name, category FROM accesstrade_campaigns ORDER BY id')
rows = cursor.fetchall()

print("=" * 60)
print("📊 CAMPAIGNS IN DATABASE")
print("=" * 60)

for row in rows:
    campaign_id = row[0]
    name = row[1][:45] if row[1] else "N/A"
    category = row[2] if row[2] else "N/A"
    print(f"   ID: {campaign_id}")
    print(f"   Name: {name}")
    print(f"   Category: {category}")
    print()

# Đếm tổng số
cursor.execute('SELECT COUNT(*) FROM accesstrade_campaigns')
total = cursor.fetchone()[0]
print(f"📈 Total campaigns: {total}")
print("=" * 60)

conn.close()
