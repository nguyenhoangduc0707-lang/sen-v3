"""
Combine ACFC and AccessTrade campaigns
"""
import sqlite3
import json

conn = sqlite3.connect('sen_v3.db')
cursor = conn.cursor()

# Lấy ACFC promotions
cursor.execute('SELECT name, code, brands, promotion_url FROM acfc_promotions WHERE status = "active"')
acfc = cursor.fetchall()

# Lấy AccessTrade campaigns
cursor.execute('SELECT id, name, commission FROM accesstrade_campaigns')
accesstrade = cursor.fetchall()

print("=" * 60)
print("🔄 Combined Campaigns Overview")
print("=" * 60)

print(f"\n📦 ACFC Promotions: {len(acfc)} active")
print(f"📦 AccessTrade Campaigns: {len(accesstrade)}")

# Tìm campaigns trùng
acfc_names = {p[0].lower() for p in acfc}
at_names = {c[1].lower() for c in accesstrade}
common = acfc_names & at_names

print(f"\n🔗 Overlapping campaigns: {len(common)}")
if common:
    print("   - " + "\n   - ".join(list(common)[:10]))

# Tạo report tổng hợp
combined = {
    'acfc': [{'name': p[0], 'code': p[1], 'brands': json.loads(p[2]) if p[2] else []} for p in acfc],
    'accesstrade': [{'id': c[0], 'name': c[1], 'commission': c[2]} for c in accesstrade],
    'total_acfc': len(acfc),
    'total_accesstrade': len(accesstrade)
}

with open('combined_campaigns.json', 'w', encoding='utf-8') as f:
    json.dump(combined, f, indent=2, ensure_ascii=False)

print(f"\n✅ Saved combined report to combined_campaigns.json")

conn.close()
print("\n" + "=" * 60)
