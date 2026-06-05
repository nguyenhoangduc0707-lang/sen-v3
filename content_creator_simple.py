# content_creator_simple.py
import json
from datetime import datetime

print("=" * 60)
print("TẠO NỘI DUNG AFFILIATE - SHOPEE THÁNG 6")
print("=" * 60)

# Link affiliate từ file của bạn
affiliate_links = [
    "https://shorten.asia/3cSC6EUX",
    "https://shorten.asia/PjYek8R8",
    "https://shorten.asia/MxvRDqNg"
]

# Các chiến dịch Shopee tháng 6
campaigns = [
    {"name": "1.6 Opening Sale", "date": "1/6", "hashtag": "OpeningSale"},
    {"name": "6.6 Mid Year Mega Sale", "date": "6/6", "hashtag": "MidYearSale"},
    {"name": "15.6 Mid-month Sale", "date": "15/6", "hashtag": "MidMonthSale"},
    {"name": "25.6 Payday Sale", "date": "25/6", "hashtag": "PaydaySale"}
]

# Tạo bài viết
post_count = 0
for c in campaigns:
    for link in affiliate_links:
        post_count += 1
        content = f"""
========================================
BÀI VIẾT {post_count}: {c['name']}
========================================

🎉 {c['name'].upper()} - SIÊU ƯU ĐÃI 🎉

✨ GIẢM ĐẾN 50% + VOUCHER KHỦNG
✨ FREESHIP 0Đ TOÀN QUỐC
✨ MUA TRƯỚC TRẢ SAU 0%

📅 Ngày diễn ra: {c['date']}/2026

🛍️ ĐẶT HÀNG NGAY:
{link}

🏷️ #{c['hashtag']} #Shopee #Affiliate

"""
        # Lưu file
        filename = f"post_{c['name'].replace(' ', '_')}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Da tao: {filename}")

print(f"\nHoan tat! Da tao {post_count} bai viet")
print("Xem file: post_*.txt")