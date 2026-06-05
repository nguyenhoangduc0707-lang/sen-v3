"""
WORKER ACFC - PHIÊN BẢN THẬT
Chạy với link tiếp thị cá nhân của bạn
"""

import json
from datetime import datetime

# ============================================
# 🔑 NHẬP LINK AFFILIATE CÁ NHÂN CỦA BẠN VÀO ĐÂY
# ============================================
YOUR_AFFILIATE_LINKS = {
    "double5_general": "https://www.acfc.com.vn/promotion/double-day.html?ref=YOUR_ID",
    "calvin_klein": "https://www.acfc.com.vn/promotion/double-day.html?brand_id=47&ref=YOUR_ID",
    "tommy": "https://www.acfc.com.vn/promotion/double-day.html?brand_id=14&ref=YOUR_ID",
    "mango": "https://www.acfc.com.vn/promotion/double-day.html?brand_id=5&ref=YOUR_ID",
    "guess": "https://www.acfc.com.vn/promotion/double-day.html?brand_id=69&ref=YOUR_ID",
    "cotton_on": "https://www.acfc.com.vn/promotion/cotton-on-special-offer.html?ref=YOUR_ID",
    "voucher": "https://www.acfc.com.vn/promotion.html?code=ACFCNEWU200&ref=YOUR_ID"
}

CAMPAIGNS = [
    {"name": "🛍️ Double 5 - Giảm 50% + Voucher 1.5tr", "key": "double5_general"},
    {"name": "👕 Calvin Klein - Giảm 50%", "key": "calvin_klein"},
    {"name": "👔 Tommy Hilfiger - Giảm 50%", "key": "tommy"},
    {"name": "💃 Mango - Giảm 50%", "key": "mango"},
    {"name": "👜 Guess - Giảm 50%", "key": "guess"},
    {"name": "🍃 Cotton On - Giảm 50%++", "key": "cotton_on"},
    {"name": "🎫 Voucher 200K - Mã ACFCNEWU200", "key": "voucher"}
]

print("=" * 60)
print("💰 ACFC AFFILIATE WORKER - BẢN THẬT")
print("=" * 60)
print(f"⏰ {datetime.now().strftime('%H:%M:%S %d/%m/%Y')}")
print("=" * 60)

# Kiểm tra link đã được cập nhật chưa
has_real_link = any("YOUR_ID" not in link for link in YOUR_AFFILIATE_LINKS.values())

if not has_real_link:
    print("\n⚠️ BẠN ĐANG Ở CHẾ ĐỘ DEMO!")
    print("👉 Để chạy THẬT, hãy:")
    print("   1. Đăng nhập ACFC/Accesstrade")
    print("   2. Lấy link tiếp thị cá nhân")
    print("   3. Thay 'YOUR_ID' trong code bằng ID thật")
    print("   4. Chạy lại worker này")
    print("=" * 60)
    exit()

print("\n📌 LINK AFFILIATE CÁ NHÂN (THẬT):\n")
for camp in CAMPAIGNS:
    link = YOUR_AFFILIATE_LINKS[camp["key"]]
    print(f"✅ {camp['name']}")
    print(f"   🔗 {link}\n")

# Lưu link ra file
filename = f"acfc_real_links_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
filepath = f"E:/DYT_01/{filename}"

with open(filepath, "w", encoding="utf-8") as f:
    f.write("=" * 60 + "\n")
    f.write("💰 AFFILIATE LINKS THẬT - ACFC\n")
    f.write(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write("=" * 60 + "\n\n")
    for camp in CAMPAIGNS:
        link = YOUR_AFFILIATE_LINKS[camp["key"]]
        f.write(f"📌 {camp['name']}\n")
        f.write(f"   🔗 {link}\n\n")

print("=" * 60)
print(f"✅ ĐÃ TẠO {len(CAMPAIGNS)} LINK AFFILIATE THẬT")
print(f"💾 Lưu tại: {filepath}")
print("=" * 60)
