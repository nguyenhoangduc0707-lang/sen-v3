from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json
import os
import time
import subprocess

print("=" * 50)
print("📱 FACEBOOK POSTER - THÍ NGHIỆM 4")
print("=" * 50)

# Nội dung bài đăng mới
content = '''Xin chào bạn, hôm nay chúng ta sẽ cùng nhau đi qua một hành trình nhỏ mang tên "Buông bỏ". 

Có những điều trong cuộc sống khiến ta nặng lòng, nhưng đôi khi, việc giữ chặt lại chỉ làm ta thêm mệt mỏi. 

Hãy thử hít một hơi thật sâu… và thở ra thật chậm… để cảm nhận sự nhẹ nhõm. 

Bạn xứng đáng được bình an, ngay trong khoảnh khắc này.

#BuongBo #BinhAn #TamLy

thí nghiệm 4

Thành công'''

# Copy nội dung vào clipboard
print("\n📝 Đang copy nội dung vào clipboard...")
subprocess.run("clip", input=content.encode("utf-8"), check=True)
print("✅ Nội dung đã được copy (Ctrl+V để dán)")
print("\n📄 NỘI DUNG:")
print("-" * 40)
print(content)
print("-" * 40)

# Mở trình duyệt
print("\n🚀 Đang khởi động Chrome...")
options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--no-sandbox')
options.add_argument('--disable-infobars')
options.add_argument('--lang=vi-VN')
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

driver.get("https://www.facebook.com/")
time.sleep(2)

# Load cookie
cookie_file = "fb_cookies_selenium.json"
if os.path.exists(cookie_file):
    print("🍪 Đang load cookies...")
    with open(cookie_file, "r") as f:
        cookies = json.load(f)
    for cookie in cookies:
        try:
            driver.add_cookie(cookie)
        except:
            pass
    driver.refresh()
    time.sleep(3)
    print("✅ Đã đăng nhập!")

print("\n" + "=" * 50)
print("📌 HƯỚNG DẪN:")
print("   1. Click vào ô 'Bạn đang nghĩ gì?'")
print("   2. Nhấn Ctrl+V để dán nội dung")
print("   3. Thêm ảnh (nếu muốn)")
print("   4. Nhấn nút 'Đăng'")
print("=" * 50)

input("\n👉 Sau khi đăng bài xong, nhấn Enter để đóng...")
driver.quit()
print("✅ Hoàn tất! Bài đăng 'thí nghiệm 4' đã được đăng!")
