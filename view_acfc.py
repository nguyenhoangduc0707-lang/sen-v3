"""
View ACFC Promotions from Database
"""
import sqlite3
import json

conn = sqlite3.connect('sen_v3.db')
cur = conn.cursor()

cur.execute('SELECT name, code, brands, start_date, end_date FROM acfc_promotions WHERE status = "active"')
rows = cur.fetchall()

print("=" * 60)
print("🎯 ACFC Active Promotions")
print("=" * 60)

for idx, row in enumerate(rows, 1):
    name = row[0][:45] if row[0] else "N/A"
    code = row[1] if row[1] else "N/A"
    brands = row[2] if row[2] else "N/A"
    if brands and brands != "N/A":
        try:
            brands_list = json.loads(brands)
            brands = ", ".join(brands_list[:3])
        except:
            pass
    start = row[3] if row[3] else "N/A"
    end = row[4] if row[4] else "N/A"
    
    print(f"{idx}. {name}")
    print(f"   Code: {code} | Brands: {brands}")
    print(f"   Period: {start} → {end}")
    print()

print(f"📈 Total active promotions: {len(rows)}")
print("=" * 60)

conn.close()
