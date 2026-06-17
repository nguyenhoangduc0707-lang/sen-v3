import webbrowser
import subprocess
import sys

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

print("=" * 60)
print("🚀 TỰ ĐỘNG MỞ CÁC NỀN TẢNG + HIỂN THỊ NỘI DUNG")
print("=" * 60)

# Mở các nền tảng
print("\n📱 ĐANG MỞ THREADS...")
webbrowser.open("https://threads.net")

print("\n🎵 ĐANG MỞ TIKTOK...")
webbrowser.open("https://www.tiktok.com")

print("\n📘 ĐANG MỞ FACEBOOK...")
webbrowser.open("https://www.facebook.com")

# Hiển thị nội dung để copy
print("\n" + "=" * 60)
print("📋 NỘI DUNG BÀI ĐĂNG - COPY BÊN DƯỚI:")
print("=" * 60)

print("\n🔵 THREADS:")
print("-" * 40)
print(THREADS_POST)
print("-" * 40)

print("\n🎵 TIKTOK:")
print("-" * 40)
print(TIKTOK_POST)
print("-" * 40)

print("\n🔵 FACEBOOK:")
print("-" * 40)
print(FACEBOOK_POST)
print("-" * 40)

# Hỗ trợ copy trên Windows (không cần thư viện)
if sys.platform == "win32":
    try:
        # Tạo file tạm chứa nội dung
        with open("E:\\DYT_01\\temp_post.txt", "w", encoding="utf-8") as f:
            f.write(THREADS_POST)
        # Dùng lệnh cmd để copy
        subprocess.run("clip < E:\\DYT_01\\temp_post.txt", shell=True)
        print("\n✅ Nội dung THREADS đã được copy vào clipboard (Ctrl+V để dán)!")
    except:
        print("\n⚠️ Không thể copy tự động, hãy copy thủ công nội dung bên trên.")

print("\n" + "=" * 60)
print("📝 HƯỚNG DẪN:")
print("1. Đăng nhập vào các tab đã mở (chỉ cần 1 lần)")
print("2. Copy nội dung tương ứng từ bên trên")
print("3. Dán (Ctrl+V) và đăng bài")
print("=" * 60)

# Giữ cửa sổ mở
input("\n👉 Nhấn Enter để đóng...")
