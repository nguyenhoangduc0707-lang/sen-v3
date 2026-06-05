import requests
import json
from datetime import datetime

print("=" * 50)
print("💰 AFFILIATE WORKER DEMO")
print("=" * 50)

# Demo campaigns
campaigns = [
    {"id": "CK_001", "name": "Calvin Klein - Double 5 Sale", "commission": "50%"},
    {"id": "TH_002", "name": "Tommy Hilfiger - Double 5 Sale", "commission": "50%"},
    {"id": "MG_003", "name": "Mango - Double 5 Sale", "commission": "50%"},
    {"id": "GS_004", "name": "Guess - Double 5 Sale", "commission": "50%"},
    {"id": "CO_005", "name": "Cotton On - Special Offer", "commission": "50%++"}
]

print(f"\n📊 Tìm thấy {len(campaigns)} chiến dịch:")
for c in campaigns:
    print(f"   - {c['name']}: {c['commission']}")

# Tạo link demo
print(f"\n🔗 Đang tạo link affiliate...")
links = []
for c in campaigns[:3]:
    link = f"https://www.acfc.com.vn/promotion/double-day.html?campaign={c['id']}"
    links.append(link)
    print(f"   ✅ {c['name']}: {link}")

# Lưu link
filename = f"affiliate_links_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
with open(f"E:/DYT_01/{filename}", "w") as f:
    for link in links:
        f.write(f"{link}\n")

print(f"\n💾 Đã lưu {len(links)} links vào: {filename}")
print(f"\n✅ WORKER DEMO CHẠY THÀNH CÔNG!")
