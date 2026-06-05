"""
WORKER TỔNG HỢP TỐI ƯU - CHẠY TẤT CẢ TRONG 1 LẦN
Kết hợp: ACFC Affiliate + Content + Link Aggregator
"""

import os
import json
import subprocess
import sys
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# ============================================
# CẤU HÌNH AFFILIATE
# ============================================

# THAY LINK AFFILIATE CÁ NHÂN CỦA BẠN VÀO ĐÂY
AFFILIATE_LINKS = {
    "double5_general": os.getenv("ACFC_DOUBLE5_LINK", "https://www.acfc.com.vn/promotion/double-day.html?ref=YOUR_ID"),
    "calvin_klein": os.getenv("ACFC_CK_LINK", "https://www.acfc.com.vn/promotion/double-day.html?brand_id=47&ref=YOUR_ID"),
    "tommy": os.getenv("ACFC_TOMMY_LINK", "https://www.acfc.com.vn/promotion/double-day.html?brand_id=14&ref=YOUR_ID"),
    "mango": os.getenv("ACFC_MANGO_LINK", "https://www.acfc.com.vn/promotion/double-day.html?brand_id=5&ref=YOUR_ID"),
    "guess": os.getenv("ACFC_GUESS_LINK", "https://www.acfc.com.vn/promotion/double-day.html?brand_id=69&ref=YOUR_ID"),
    "cotton_on": os.getenv("ACFC_COTTON_LINK", "https://www.acfc.com.vn/promotion/cotton-on-special-offer.html?ref=YOUR_ID"),
    "voucher": os.getenv("ACFC_VOUCHER_LINK", "https://www.acfc.com.vn/promotion.html?code=ACFCNEWU200&ref=YOUR_ID")
}

# ============================================
# BÀI ĐĂNG TỐI ƯU CHUYỂN ĐỔI CAO
# ============================================

POST_TEMPLATES = {
    "calvin_klein": [
        "🔥 CK GIẢM 50% - Từ 3tr còn 1tr5!\n\n👉 Double 5 Sale:\n✅ Calvin Klein giảm 50%\n✅ Extra voucher 1.5tr\n✅ Freeship đơn 2tr\n\n🔗 {link}\n\n#ACFCOnline #Double5ACFC #CalvinKlein",
        "CK sale 50%, túi xách từ 4tr còn 2tr! 🔥\n\nMua ngay kẻo hết!\n🔗 {link}\n\n#ACFCOnline #CalvinKlein #Sale"
    ],
    "tommy": [
        "👕 TOMMY GIẢM 50% - Áo polo từ 2tr còn 1tr!\n\n🔗 {link}\n\n#ACFCOnline #TommyHilfiger #Double5ACFC",
        "Tommy Hilfiger giảm 50%, áo thun chỉ từ 800k! 👕\n🔗 {link}\n\n#ACFCOnline #TommyHilfiger"
    ],
    "mango": [
        "💃 MANGO GIẢM 50% - Đầm công sở từ 1.8tr còn 900k!\n\n🔗 {link}\n\n#ACFCOnline #Mango #Double5ACFC"
    ],
    "guess": [
        "👜 GUESS GIẢM 50% - Túi xách từ 4tr còn 2tr!\n\n🔗 {link}\n\n#ACFCOnline #Guess #Double5ACFC"
    ],
    "cotton_on": [
        "🍃 COTTON ON GIẢM 50% - Mua cả set hè chỉ 500k!\n\n🔗 {link}\n\n#ACFCOnline #CottonOn #CottonOnSale"
    ],
    "general": [
        "🔥 DOUBLE 5 SALE - GIẢM ĐẾN 50% + VOUCHER 1.5TR!\n\n👉 Calvin Klein, Tommy, Mango, Guess giảm 50%\n👉 Cotton On giảm 50%++\n👉 Freeship toàn quốc\n\n🔗 {link}\n\n#ACFCOnline #Double5ACFC #SaleHangHieu",
        "💰 SĂN SALE HÀNG HIỆU GIÁ HỜI!\n\n🔗 {link}\n\n#ACFCOnline #Double5ACFC",
        "🎫 VOUCHER 200K CHO KHÁCH MỚI!\nNhập mã ACFCNEWU200 giảm 200K\n\n🔗 {link}\n\n#ACFCOnline #VoucherACFC"
    ]
}

# ============================================
# HÀM CHÍNH
# ============================================

def check_affiliate_links():
    """Kiểm tra link affiliate đã được cập nhật chưa"""
    has_real = any("YOUR_ID" not in link for link in AFFILIATE_LINKS.values())
    return has_real

def generate_all_posts():
    """Tạo tất cả bài đăng với link đã được thay thế"""
    all_posts = []
    
    # Bài theo từng brand
    for brand, templates in POST_TEMPLATES.items():
        if brand == "general":
            continue
        link = AFFILIATE_LINKS.get(brand, AFFILIATE_LINKS["double5_general"])
        for template in templates:
            content = template.format(link=link)
            all_posts.append({"brand": brand, "content": content})
    
    # Bài tổng hợp
    general_link = AFFILIATE_LINKS["double5_general"]
    for template in POST_TEMPLATES["general"]:
        content = template.format(link=general_link)
        all_posts.append({"brand": "general", "content": content})
    
    return all_posts

def save_links():
    """Lưu link affiliate ra file"""
    filename = f"affiliate_links_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    filepath = f"E:/DYT_01/{filename}"
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write("💰 AFFILIATE LINKS - DYT_01\n")
        f.write(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 60 + "\n\n")
        for name, link in AFFILIATE_LINKS.items():
            f.write(f"📌 {name.upper()}\n")
            f.write(f"   🔗 {link}\n\n")
    
    return filepath

def save_posts(posts):
    """Lưu bài đăng ra file"""
    filename = f"threads_posts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    filepath = f"E:/DYT_01/{filename}"
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write("📝 BÀI ĐĂNG THREADS - DYT_01\n")
        f.write(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 60 + "\n\n")
        
        for idx, post in enumerate(posts, 1):
            f.write(f"【BÀI {idx} - {post['brand'].upper()}】\n")
            f.write("-" * 40 + "\n")
            f.write(post['content'] + "\n")
            f.write("-" * 40 + "\n\n")
    
    return filepath

def run_acfc_worker():
    """Chạy worker ACFC riêng (nếu cần)"""
    try:
        result = subprocess.run(
            [sys.executable, "E:/DYT_01/workers/worker_acfc_real.py"],
            capture_output=True,
            text=True,
            timeout=60
        )
        return result.returncode == 0
    except:
        return False

# ============================================
# MAIN
# ============================================

print("=" * 60)
print("🚀 WORKER TỔNG HỢP TỐI ƯU - DYT_01")
print("=" * 60)
print(f"⏰ {datetime.now().strftime('%H:%M:%S %d/%m/%Y')}")
print("=" * 60)

# Kiểm tra link
has_real = check_affiliate_links()

if not has_real:
    print("\n⚠️ BẠN ĐANG Ở CHẾ ĐỘ DEMO!")
    print("=" * 60)
    print("🔧 HƯỚNG DẪN CHUYỂN SANG THẬT:")
    print("   1. Đăng nhập ACFC/Accesstrade")
    print("   2. Lấy link tiếp thị cá nhân")
    print("   3. Thay 'YOUR_ID' trong AFFILIATE_LINKS")
    print("   4. Hoặc set biến môi trường:")
    print("      - ACFC_DOUBLE5_LINK=link_của_bạn")
    print("      - ACFC_CK_LINK=link_của_bạn")
    print("=" * 60)

# Tạo link và bài đăng
print("\n📌 BƯỚC 1: TẠO LINK AFFILIATE...")
link_file = save_links()
print(f"   ✅ Đã lưu link: {link_file}")

print("\n📌 BƯỚC 2: TẠO BÀI ĐĂNG TỐI ƯU...")
posts = generate_all_posts()
post_file = save_posts(posts)
print(f"   ✅ Đã tạo {len(posts)} bài đăng")
print(f"   💾 Lưu tại: {post_file}")

print("\n📌 BƯỚC 3: HIỂN THỊ MẪU BÀI ĐĂNG...")
print("-" * 60)
for i, post in enumerate(posts[:3], 1):
    print(f"\n【MẪU {i} - {post['brand'].upper()}】")
    print(post['content'])
    print("-" * 40)

print("\n" + "=" * 60)
print("✅ HOÀN TẤT! ĐÃ SẴN SÀNG KIẾM TIỀN")
print("=" * 60)
print("\n💰 THU NHẬP TIỀM NĂNG:")
print("   Mỗi bài đăng được duyệt: 150.000đ")
print("   Tối đa 30 bài/tháng = 4.500.000đ")
print("   Cả chiến dịch (đến 31/08) ≈ 20.000.000đ")
print("=" * 60)
