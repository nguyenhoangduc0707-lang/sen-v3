"""
WORKER CONTENT - TẠO NỘI DUNG THREADS TỰ ĐỘNG
Tạo bài đăng sẵn sàng để copy-paste
"""

import random
from datetime import datetime

# Mẫu nội dung theo từng brand
CONTENT_TEMPLATES = {
    "calvin_klein": [
        "🔥 CK giảm 50% – Đôi giày mình thích từ 3tr còn 1tr5!\n\nDouble 5 trên ACFC đang diễn ra:\n👉 Calvin Klein giảm đến 50%\n👉 Extra voucher 1.5tr\n👉 Freeship đơn từ 2tr\n\n#ACFCOnline #Double5ACFC #CalvinKlein",
        
        "CK sale 50% nè các bà ơi! 🔥\nTừ 3tr còn 1tr5 thôi\nExtra voucher 1.5tr + freeship\n\nLink: [ĐIỀN LINK AFFILIATE]\n\n#ACFCOnline #Double5ACFC #CalvinKlein"
    ],
    
    "tommy": [
        "👕 Tommy Hilfiger giảm 50% – Áo polo từ 2tr còn 1tr!\n\nDouble 5 đang diễn ra:\n👉 Tommy giảm đến 50%\n👉 Extra voucher 1.5tr\n👉 Freeship đơn từ 2tr\n\n#ACFCOnline #Double5ACFC #TommyHilfiger",
        
        "Tommy sale 50% kìa các bác! 👕\nÁo polo từ 2tr còn 1tr\nExtra voucher 1.5tr + freeship\n\nLink: [ĐIỀN LINK AFFILIATE]\n\n#ACFCOnline #Double5ACFC #TommyHilfiger"
    ],
    
    "mango": [
        "💃 Mango giảm 50% – Đầm công sở từ 1.8tr còn 900k!\n\nDouble 5 trên ACFC:\n👉 Mango giảm đến 50%\n👉 Extra voucher 1.5tr\n👉 Freeship đơn từ 2tr\n\n#ACFCOnline #Double5ACFC #Mango"
    ],
    
    "guess": [
        "👜 Guess giảm 50% – Túi xách từ 4tr còn 2tr!\n\nDouble 5 đang diễn ra:\n👉 Guess giảm đến 50%\n👉 Extra voucher 1.5tr\n👉 Freeship đơn từ 2tr\n\n#ACFCOnline #Double5ACFC #Guess"
    ],
    
    "cotton_on": [
        "🍃 Cotton On giảm 50% – Mua cả set hè chỉ 500k!\n\nSpecial Offer đang diễn ra:\n👉 Cotton On giảm đến 50%++\n👉 Áo thun từ 150k\n👉 Quần short từ 200k\n👉 Freeship đơn từ 600k\n\n#ACFCOnline #CottonOn #CottonOnSale"
    ],
    
    "voucher": [
        "🎫 Voucher 200K cho khách mới ACFC!\n\nNhập mã ACFCNEWU200 giảm 200K cho đơn từ 1.5tr\n\n#ACFCOnline #VoucherACFC #SaleHangHieu"
    ]
}

# Các hashtag phổ biến
HASHTAGS = [
    "#ACFCOnline", "#Double5ACFC", "#SaleHangHieu", 
    "#VoucherACFC", "#ThoiTrangHangHieu", "#Freeship"
]

def generate_post(brand=None):
    """Tạo bài đăng ngẫu nhiên hoặc theo brand"""
    if brand and brand in CONTENT_TEMPLATES:
        templates = CONTENT_TEMPLATES[brand]
    else:
        # Chọn brand ngẫu nhiên
        brand = random.choice(list(CONTENT_TEMPLATES.keys()))
        templates = CONTENT_TEMPLATES[brand]
    
    content = random.choice(templates)
    
    # Thêm hashtag nếu thiếu
    if "#ACFCOnline" not in content:
        content += "\n\n" + " ".join(random.sample(HASHTAGS, 3))
    
    return content, brand

print("=" * 60)
print("📝 WORKER CONTENT - TẠO BÀI ĐĂNG THREADS")
print("=" * 60)
print(f"⏰ Chạy lúc: {datetime.now().strftime('%H:%M:%S %d/%m/%Y')}")
print("=" * 60)

# Tạo 5 bài đăng mẫu
print("\n📌 BÀI ĐĂNG MẪU (COPY - PASTE):\n")

posts = []
for i in range(5):
    content, brand = generate_post()
    posts.append({"content": content, "brand": brand})
    print(f"{i+1}. 【{brand.upper()}】")
    print("-" * 40)
    print(content)
    print("-" * 40)
    print()

# Lưu bài đăng ra file
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

print("=" * 60)
print(f"✅ ĐÃ TẠO {len(posts)} BÀI ĐĂNG MẪU")
print(f"💾 Lưu tại: {filepath}")
print("=" * 60)
print("\n📝 CÁCH ĐĂNG BÀI:")
print("   1. Copy nội dung bài đăng")
print("   2. Dán lên Threads")
print("   3. Thay [ĐIỀN LINK AFFILIATE] bằng link từ worker 1")
print("   4. Kèm ảnh/video (nếu có)")
print("   5. Đăng bài và gửi link lên Green Creator")
print("=" * 60)
