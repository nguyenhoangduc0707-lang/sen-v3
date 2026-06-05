"""
WORKER CONTENT - TẠO BÀI ĐĂNG CHUYỂN ĐỔI CAO
Tối ưu cho ACFC Double 5 Sale
"""

import random
from datetime import datetime

# ============================================
# NỘI DUNG ĐÃ TỐI ƯU THEO TỪNG BRAND
# ============================================

OPTIMIZED_POSTS = {
    "calvin_klein": [
        "🔥 CK GIẢM 50% - Đôi giày mình thích từ 3tr còn 1tr5!\n\n👉 Double 5 đang diễn ra:\n✅ Calvin Klein giảm đến 50%\n✅ Extra voucher 1.5tr\n✅ Freeship đơn từ 2tr\n\n🔗 Link mua: [THAY LINK AFFILIATE]\n\n#ACFCOnline #Double5ACFC #CalvinKlein #SaleHangHieu",
        
        "CK sale 50%, túi xách từ 4tr còn 2tr! 🔥\n\nMua ngay kẻo hết size!\n🔗 [THAY LINK AFFILIATE]\n\n#ACFCOnline #CalvinKlein #Double5ACFC"
    ],
    
    "tommy": [
        "👕 TOMMY HILFIGER GIẢM 50% - Áo polo từ 2tr còn 1tr!\n\n👉 Sale Double 5:\n✅ Tommy giảm 50%\n✅ Extra voucher 1.5tr\n✅ Freeship toàn quốc\n\n🔗 [THAY LINK AFFILIATE]\n\n#ACFCOnline #TommyHilfiger #Double5ACFC",
        
        "Tommy Hilfiger giảm 50%, áo thun chỉ từ 800k! 👕\nSăn ngay kẻo hết!\n🔗 [THAY LINK AFFILIATE]\n\n#ACFCOnline #TommyHilfiger"
    ],
    
    "mango": [
        "💃 MANGO GIẢM 50% - Đầm công sở từ 1.8tr còn 900k!\n\n👉 Sale Double 5:\n✅ Mango giảm 50%\n✅ Extra voucher 1.5tr\n✅ Freeship đơn 2tr\n\n🔗 [THAY LINK AFFILIATE]\n\n#ACFCOnline #Mango #Double5ACFC"
    ],
    
    "guess": [
        "👜 GUESS GIẢM 50% - Túi xách từ 4tr còn 2tr!\n\n👉 Sale Double 5:\n✅ Guess giảm 50%\n✅ Extra voucher 1.5tr\n✅ Freeship toàn quốc\n\n🔗 [THAY LINK AFFILIATE]\n\n#ACFCOnline #Guess #Double5ACFC"
    ],
    
    "cotton_on": [
        "🍃 COTTON ON GIẢM 50% - Mua cả set hè chỉ 500k!\n\n👉 Special Offer:\n✅ Áo thun từ 150k\n✅ Quần short từ 200k\n✅ Freeship đơn 600k\n\n🔗 [THAY LINK AFFILIATE]\n\n#ACFCOnline #CottonOn #CottonOnSale"
    ]
}

# ============================================
# BÀI ĐĂNG TỔNG HỢP (CHẠY NHANH)
# ============================================

QUICK_POSTS = [
    "🔥 DOUBLE 5 SALE - GIẢM ĐẾN 50% + VOUCHER 1.5TR!\n\n👉 Calvin Klein, Tommy, Mango, Guess giảm 50%\n👉 Cotton On giảm 50%++\n👉 Freeship toàn quốc\n\n🔗 [THAY LINK AFFILIATE]\n\n#ACFCOnline #Double5ACFC #SaleHangHieu",
    
    "💰 SĂN SALE HÀNG HIỆU GIÁ HỜI!\n\nGiảm đến 50% các thương hiệu:\n✅ Calvin Klein\n✅ Tommy Hilfiger\n✅ Mango\n✅ Guess\n✅ Cotton On\n\n🔗 [THAY LINK AFFILIATE]\n\n#ACFCOnline #Double5ACFC",
    
    "🎫 VOUCHER 200K CHO KHÁCH MỚI!\n\nNhập mã ACFCNEWU200 giảm 200K cho đơn từ 1.5tr\n\n🔗 [THAY LINK AFFILIATE]\n\n#ACFCOnline #VoucherACFC"
]

def get_post_by_brand(brand):
    """Lấy bài đăng theo brand cụ thể"""
    if brand in OPTIMIZED_POSTS:
        return random.choice(OPTIMIZED_POSTS[brand])
    return random.choice(QUICK_POSTS)

def get_all_posts():
    """Lấy tất cả bài đăng tối ưu"""
    posts = []
    for brand, contents in OPTIMIZED_POSTS.items():
        for content in contents:
            posts.append({"brand": brand, "content": content})
    for content in QUICK_POSTS:
        posts.append({"brand": "general", "content": content})
    return posts

print("=" * 60)
print("📝 WORKER CONTENT - BÀI ĐĂNG TỐI ƯU")
print("=" * 60)
print(f"⏰ {datetime.now().strftime('%H:%M:%S %d/%m/%Y')}")
print("=" * 60)

# Tạo danh sách bài đăng
all_posts = get_all_posts()

print("\n📌 DANH SÁCH BÀI ĐĂNG (COPY - PASTE):\n")

for idx, post in enumerate(all_posts[:8], 1):  # Chỉ hiển thị 8 bài
    print(f"{idx}. 【{post['brand'].upper()}】")
    print("-" * 50)
    print(post['content'])
    print("-" * 50)
    print()

# Lưu ra file
filename = f"optimized_posts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
filepath = f"E:/DYT_01/{filename}"

with open(filepath, "w", encoding="utf-8") as f:
    f.write("=" * 60 + "\n")
    f.write("📝 BÀI ĐĂNG TỐI ƯU - DYT_01 AFFILIATE\n")
    f.write(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write("=" * 60 + "\n\n")
    
    for idx, post in enumerate(all_posts, 1):
        f.write(f"【BÀI {idx} - {post['brand'].upper()}】\n")
        f.write("-" * 40 + "\n")
        f.write(post['content'] + "\n")
        f.write("-" * 40 + "\n\n")

print("=" * 60)
print(f"✅ ĐÃ TẠO {len(all_posts)} BÀI ĐĂNG TỐI ƯU")
print(f"💾 Lưu tại: {filepath}")
print("=" * 60)
print("\n📋 HƯỚNG DẪN ĐĂNG BÀI KIẾM TIỀN:")
print("   1. Mở file threads_posts_*.txt")
print("   2. Copy bài đăng")
print("   3. Dán lên Threads")
print("   4. Thay [THAY LINK AFFILIATE] = link từ worker_acfc_real.py")
print("   5. Thêm ảnh/video đẹp (chụp tại VinWonders hoặc ảnh sản phẩm)")
print("   6. Đăng bài -> Gửi link lên Green Creator")
print("   7. Mỗi bài = 150.000đ, 30 bài/tháng = 4.500.000đ")
print("=" * 60)
