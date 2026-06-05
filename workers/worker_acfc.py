"""
WORKER ACFC - LẤY LINK AFFILIATE KIẾM TIỀN
Chạy độc lập, không cần API key
"""

import json
from datetime import datetime

# Dữ liệu chiến dịch ACFC
CAMPAIGNS = [
    {"name": "🛍️ Double 5 - Giảm 50% + Voucher 1.5tr", 
     "link": "https://www.acfc.com.vn/promotion/double-day.html",
     "commission": "50% + Voucher 1.5tr"},
    
    {"name": "👕 Calvin Klein - Giảm 50%", 
     "link": "https://www.acfc.com.vn/promotion/double-day.html?brand_id=47",
     "commission": "50%"},
    
    {"name": "👔 Tommy Hilfiger - Giảm 50%", 
     "link": "https://www.acfc.com.vn/promotion/double-day.html?brand_id=14",
     "commission": "50%"},
    
    {"name": "💃 Mango - Giảm 50%", 
     "link": "https://www.acfc.com.vn/promotion/double-day.html?brand_id=5",
     "commission": "50%"},
    
    {"name": "👜 Guess - Giảm 50%", 
     "link": "https://www.acfc.com.vn/promotion/double-day.html?brand_id=69",
     "commission": "50%"},
    
    {"name": "🍃 Cotton On - Giảm 50%++", 
     "link": "https://www.acfc.com.vn/promotion/cotton-on-special-offer.html",
     "commission": "50%++"},
    
    {"name": "🎫 Voucher 200K - Mã ACFCNEWU200", 
     "link": "https://www.acfc.com.vn/promotion.html",
     "commission": "200K (đơn từ 1.5tr)"},
]

print("=" * 60)
print("💰 WORKER ACFC - KIẾM TIỀN AFFILIATE")
print("=" * 60)
print(f"⏰ Chạy lúc: {datetime.now().strftime('%H:%M:%S %d/%m/%Y')}")
print("=" * 60)

# Tạo link affiliate (thay bằng ID thật khi có)
affiliate_id = "DYT01_AFF"  # Thay bằng ID thật của bạn
links = []

print("\n📌 DANH SÁCH LINK AFFILIATE:\n")

for idx, camp in enumerate(CAMPAIGNS, 1):
    # Thêm tham số affiliate vào link
    if "?" in camp["link"]:
        aff_link = f"{camp['link']}&ref={affiliate_id}"
    else:
        aff_link = f"{camp['link']}?ref={affiliate_id}"
    
    links.append(aff_link)
    print(f"{idx}. {camp['name']}")
    print(f"   🔗 {aff_link}")
    print(f"   💰 Hoa hồng: {camp['commission']}\n")

# Lưu link ra file
filename = f"acfc_links_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
filepath = f"E:/DYT_01/{filename}"

with open(filepath, "w", encoding="utf-8") as f:
    f.write("=" * 60 + "\n")
    f.write("💰 AFFILIATE LINKS - ACFC\n")
    f.write(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write("=" * 60 + "\n\n")
    for camp, link in zip(CAMPAIGNS, links):
        f.write(f"📌 {camp['name']}\n")
        f.write(f"   🔗 {link}\n")
        f.write(f"   💰 {camp['commission']}\n\n")

print("=" * 60)
print(f"✅ ĐÃ TẠO {len(links)} LINK AFFILIATE")
print(f"💾 Lưu tại: {filepath}")
print("=" * 60)
print("\n📝 HƯỚNG DẪN:")
print("   1. Copy link từ file trên")
print("   2. Đăng lên Threads/TikTok")
print("   3. Mỗi bài được duyệt = 150.000đ")
print("   4. Tối đa 30 bài/tháng = 4.500.000đ")
print("=" * 60)
