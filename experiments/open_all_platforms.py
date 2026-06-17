import webbrowser
import pyperclip
import time

# Nội dung bài đăng
THREADS_POST = """🔥 CK GIẢM 50% - Từ 3tr còn 1tr5!

👉 Double 5 Sale đang diễn ra:
✅ Calvin Klein giảm 50%
✅ Extra voucher 1.5tr
✅ Freeship đơn 2tr

🔗 Link: [ĐIỀN LINK AFFILIATE CỦA BẠN]

#ACFCOnline #Double5ACFC #CalvinKlein #SaleHangHieu"""

TIKTOK_POST = """CK sale 50% trên ACFC nè ae ơi! 🔥
Từ 3tr còn 1tr5
Extra voucher 1.5tr + freeship

Link: [ĐIỀN LINK AFFILIATE]

#ACFCOnline #Double5ACFC #CalvinKlein"""

FACEBOOK_POST = """🛍️ SĂN SALE CALVIN KLEIN - GIẢM 50% TRÊN ACFC!

✨ Calvin Klein giảm đến 50%
✨ Extra voucher giảm 1.5tr
✨ Freeship đơn từ 2tr

👉 Link: [ĐIỀN LINK AFFILIATE]

#ACFCOnline #Double5ACFC #CalvinKlein #SaleHangHieu"""

print("=" * 50)
print("🚀 TỰ ĐỘNG MỞ CÁC NỀN TẢNG")
print("=" * 50)

# Mở Threads
print("\n📱 Đang mở Threads...")
webbrowser.open("https://threads.net")
pyperclip.copy(THREADS_POST)
print("   ✅ Nội dung Threads đã copy (Ctrl+V để dán)")

# Mở TikTok
print("\n🎵 Đang mở TikTok...")
webbrowser.open("https://www.tiktok.com")
pyperclip.copy(TIKTOK_POST)
print("   ✅ Nội dung TikTok đã copy")

# Mở Facebook
print("\n📘 Đang mở Facebook...")
webbrowser.open("https://www.facebook.com")
pyperclip.copy(FACEBOOK_POST)
print("   ✅ Nội dung Facebook đã copy")

print("\n" + "=" * 50)
print("✅ ĐÃ MỞ TẤT CẢ NỀN TẢNG!")
print("👉 Thao tác của bạn:")
print("   1. Đăng nhập (trình duyệt sẽ tự nhớ)")
print("   2. Vào từng tab, nhấn Ctrl+V để dán nội dung")
print("   3. Kiểm tra và nhấn Đăng")
print("=" * 50)
