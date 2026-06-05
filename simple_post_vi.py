# -*- coding: utf-8 -*-
print("Bắt đầu tạo bài viết...")

links = ["https://shorten.asia/3cSC6EUX", "https://shorten.asia/PjYek8R8", "https://shorten.asia/MxvRDqNg"]

for i, link in enumerate(links, 1):
    post = f"""
========================================
BÀI VIẾT {i}
========================================

SHOPEE SIÊU SALE 6.6

- Giảm giá đến 50%
- Freeship 0Đ
- Voucher lên đến 6 triệu
- Mua trước trả sau 0%

ĐẶT HÀNG NGAY:
{link}

#Shopee6_6 #MegaSale #Affiliate

"""
    with open(f"post_{i}.txt", "w", encoding="utf-8") as f:
        f.write(post)
    print(f"Đã tạo: post_{i}.txt")

print(f"\nHoàn tất! Đã tạo {len(links)} bài viết")