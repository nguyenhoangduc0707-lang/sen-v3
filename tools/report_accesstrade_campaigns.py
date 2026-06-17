"""
Generate report from AccessTrade campaigns
"""
import sqlite3
import csv
from datetime import datetime

conn = sqlite3.connect('sen_v3.db')
cursor = conn.cursor()

# Lấy tất cả campaigns
cursor.execute('''
    SELECT id, name, commission, category, cookie_duration, synced_at
    FROM accesstrade_campaigns
    ORDER BY id
''')

campaigns = cursor.fetchall()
conn.close()

print("=" * 60)
print("📊 AccessTrade Campaigns Report")
print("=" * 60)
print(f"\n📈 Total campaigns: {len(campaigns)}")
print(f"📅 Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# Nhóm theo commission
commission_groups = {}
for camp in campaigns:
    comm = camp[2] if camp[2] else 'N/A'
    if comm not in commission_groups:
        commission_groups[comm] = []
    commission_groups[comm].append(camp)

print("📊 Campaigns by Commission Rate:")
for comm, camps in sorted(commission_groups.items()):
    print(f"   {comm}%: {len(camps)} campaigns")

# Export to CSV
csv_file = f"accesstrade_campaigns_{datetime.now().strftime('%Y%m%d')}.csv"
with open(csv_file, 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerow(['ID', 'Campaign Name', 'Commission', 'Category', 'Cookie Duration', 'Synced At'])
    writer.writerows(campaigns)

print(f"\n✅ Exported to {csv_file}")

print("\n" + "=" * 60)
