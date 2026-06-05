import sqlite3

conn = sqlite3.connect('sen_v3.db')
cursor = conn.cursor()

# Financial campaigns
cursor.execute("SELECT id, name, category FROM accesstrade_campaigns WHERE category IN ('FINANCIAL SERVICES', '60', '35') ORDER BY id")

rows = cursor.fetchall()

print("=" * 70)
print("💰 FINANCIAL CAMPAIGNS AVAILABLE")
print("=" * 70)

for row in rows:
    print(f"\nID: {row[0]}")
    print(f"Name: {row[1][:60]}")
    print(f"Category: {row[2]}")

print("\n" + "=" * 70)
print(f"Total: {len(rows)} campaigns")
print("=" * 70)

conn.close()
