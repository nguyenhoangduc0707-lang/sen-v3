"""
Nội dung an toàn cho affiliate marketing
"""
safe_content = """
🔥 ƯU ĐÃI HẤP DẪN TỪ SHOPEE

✅ Giảm giá đến 70%
✅ Freeship toàn quốc
✅ Voucher đến 5 triệu

👉 Xem chi tiết: https://go.isclix.com/deep_link/v6/6983938396644077046/4751584435713464237?sub4=sen_v3

#MuaSam #SaleOff #GiamGia
"""

banned_content = """
⚠️ CẤM: "Chính sách đặc biệt từ Shopee"
⚠️ CẤM: "Shopee ưu đãi chỉ dành cho bạn"
⚠️ CẤM: Dùng logo Shopee
⚠️ CẤM: Giả mạo là Shopee
"""

print("=" * 60)
print("📋 NỘI DUNG AN TOÀN (ĐƯỢC PHÉP):")
print("=" * 60)
print(safe_content)

print("\n" + "=" * 60)
print("❌ NỘI DUNG CẤM (KHÔNG ĐƯỢC DÙNG):")
print("=" * 60)
print(banned_content)

# Lưu nội dung an toàn vào file
with open("safe_post_content.txt", "w", encoding="utf-8") as f:
    f.write(safe_content)
    print("\n✅ Đã lưu nội dung an toàn vào safe_post_content.txt")
