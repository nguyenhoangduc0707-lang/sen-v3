"""
View AccessTrade Campaigns from Database
"""
import sqlite3

conn = sqlite3.connect('sen_v3.db')
cur = conn.cursor()

cur.execute('SELECT id, name, commission FROM accesstrade_campaigns LIMIT 20')
rows = cur.fetchall()

print("=" * 60)
print("📊 AccessTrade Campaigns (from database)")
print("=" * 60)

for row in rows:
    campaign_id = row[0]
    name = row[1][:50] if row[1] else "N/A"
    commission = row[2] if row[2] else "N/A"
    print(f"   {campaign_id}. {name} - {commission}%")

cur.execute('SELECT COUNT(*) FROM accesstrade_campaigns')
total = cur.fetchone()[0]

print(f"\n📈 Total campaigns in database: {total}")
print("=" * 60)

conn.close()
