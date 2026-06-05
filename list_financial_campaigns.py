"""
List all financial campaigns from database
"""
import sqlite3

conn = sqlite3.connect('sen_v3.db')
cursor = conn.cursor()

# Lấy campaigns financial
cursor.execute('''
    SELECT id, name, category 
    FROM accesstrade_campaigns 
    WHERE category = 'FINANCIAL SERVICES' OR category = '60' OR category = '35'
    ORDER BY id
''')

rows = cursor.fetchall()

print("=" * 70)
print("💰 FINANCIAL CAMPAIGNS AVAILABLE")
print("=" * 70)

for row in rows:
    print(f"\n📌 ID: {row[0]}")
    print(f"   Name: {row[1]}")
    print(f"   Category: {row[2]}")

# Thống kê
cursor.execute('''
    SELECT category, COUNT(*) 
    FROM accesstrade_campaigns 
    WHERE category = 'FINANCIAL SERVICES' OR category = '60' OR category = '35'
    GROUP BY category
''')
print("\n" + "=" * 70)
print("📊 SUMMARY:")
for cat, count in cursor.fetchall():
    print(f"   {cat}: {count} campaigns")
print("=" * 70)

conn.close()
