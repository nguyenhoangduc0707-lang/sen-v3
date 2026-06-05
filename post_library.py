# ============================================
# KHO BÀI ĐĂNG AFFILIATE - COPY & PASTE
# ============================================

# 📌 BÀI 1: Calvin Klein - Double 5 Sale
CK_POST = """🔥 CK GIẢM 50% - Từ 3tr còn 1tr5!

👉 Double 5 Sale:
✅ Calvin Klein giảm 50%
✅ Extra voucher 1.5tr
✅ Freeship đơn 2tr

🔗 [ĐIỀN LINK AFFILIATE]

#ACFCOnline #Double5ACFC #CalvinKlein"""

# 📌 BÀI 2: Tommy Hilfiger - Double 5 Sale
TOMMY_POST = """👕 TOMMY GIẢM 50% - Áo polo từ 2tr còn 1tr!

👉 Double 5 Sale:
✅ Tommy Hilfiger giảm 50%
✅ Extra voucher 1.5tr
✅ Freeship đơn 2tr

🔗 [ĐIỀN LINK AFFILIATE]

#ACFCOnline #Double5ACFC #TommyHilfiger"""

# 📌 BÀI 3: Cotton On - Special Offer
COTTON_POST = """🍃 COTTON ON GIẢM 50% - Mua cả set hè chỉ 500k!

👉 Special Offer:
✅ Áo thun từ 150k
✅ Quần short từ 200k
✅ Freeship đơn 600k

🔗 [ĐIỀN LINK AFFILIATE]

#ACFCOnline #CottonOn #CottonOnSale"""

# 📌 BÀI 4: Voucher 200K cho khách mới
VOUCHER_POST = """🎫 VOUCHER 200K CHO KHÁCH MỚI ACFC!

Nhập mã ACFCNEWU200 giảm 200K cho đơn từ 1.5tr

🔗 [ĐIỀN LINK AFFILIATE]

#ACFCOnline #VoucherACFC #SaleHangHieu"""

# 📌 BÀI 5: Tổng hợp Double 5 Sale
GENERAL_POST = """🔥 DOUBLE 5 SALE - GIẢM ĐẾN 50% + VOUCHER 1.5TR!

👉 Thương hiệu tham gia:
✅ Calvin Klein
✅ Tommy Hilfiger
✅ Mango
✅ Guess
✅ Cotton On

🔗 [ĐIỀN LINK AFFILIATE]

#ACFCOnline #Double5ACFC #SaleHangHieu"""

print("=" * 50)
print("📋 KHO BÀI ĐĂNG AFFILIATE")
print("=" * 50)
print("\n1. Calvin Klein (Double 5)")
print("2. Tommy Hilfiger (Double 5)")
print("3. Cotton On (Special Offer)")
print("4. Voucher 200K")
print("5. Tổng hợp Double 5")
print("=" * 50)

choice = input("\n👉 Chọn bài muốn copy (1-5): ")

posts = {"1": CK_POST, "2": TOMMY_POST, "3": COTTON_POST, "4": VOUCHER_POST, "5": GENERAL_POST}
selected = posts.get(choice, CK_POST)

# Copy vào clipboard
import pyperclip
pyperclip.copy(selected)
print("\n✅ Đã copy nội dung vào clipboard!")
print("👉 Mở Threads/Facebook/TikTok, nhấn Ctrl+V để dán")
