# create_posts_with_new_link.py
import time
from datetime import datetime

# Đọc tất cả link
with open("affiliate_links.txt", "r") as f:
    links = [line.strip() for line in f if line.strip() and 'shorten.asia' in line]

print(f"Đã tìm thấy {len(links)} affiliate links:")
for i, link in enumerate(links, 1):
    print(f"{i}. {link}")

# Tạo bài viết cho từng link
for i, link in enumerate(links, 1):
    content = f"""
{'='*50}
BÀI VIẾT AFFILIATE {i} - SHOPEE 6.6 MEGA SALE
{'='*50}

🔥 SIÊU SALE 6.6 - GIẢM ĐẾN 50% 🔥

✨ ƯU ĐÃI ĐẶC BIỆT:
• Giảm giá lên đến 50%
• Freeship 0Đ toàn quốc
• Voucher Xtra 6 triệu đồng
• Mua trước trả sau 0%

🛍️ ĐẶT HÀNG NGAY:
{link}

🏷️ #Shopee6_6 #MegaSale #Affiliate #Freeship

📅 Đăng ngày: {datetime.now().strftime('%d/%m/%Y')}
"""
    filename = f"affiliate_post_{i}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Đã tạo: {filename}")

print(f"\n✅ Hoàn thành! Đã tạo {len(links)} bài viết")