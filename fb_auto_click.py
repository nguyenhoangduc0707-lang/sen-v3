import time
import pyautogui
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json
import os

print("=" * 50)
print("🤖 FACEBOOK AUTO POSTER - PYAutoGUI")
print("=" * 50)

# Nội dung bài đăng
content = '''Xin chào bạn, hôm nay chúng ta sẽ cùng nhau đi qua một hành trình nhỏ mang tên "Buông bỏ". 

Có những điều trong cuộc sống khiến ta nặng lòng, nhưng đôi khi, việc giữ chặt lại chỉ làm ta thêm mệt mỏi. 

Hãy thử hít một hơi thật sâu… và thở ra thật chậm… để cảm nhận sự nhẹ nhõm. 

Bạn xứng đáng được bình an, ngay trong khoảnh khắc này.

#BuongBo #BinhAn #TamLy

thí nghiệm 5 - Tự động hoàn toàn'''

# Copy nội dung
import subprocess
subprocess.run("clip", input=content.encode("utf-8"), check=True)
print("✅ Nội dung đã copy vào clipboard")

# Mở trình duyệt
print("🚀 Đang khởi động Chrome...")
options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--no-sandbox')
options.add_argument('--disable-infobars')
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

driver.get("https://www.facebook.com/")
time.sleep(3)

# Load cookie
cookie_file = "fb_cookies_selenium.json"
if os.path.exists(cookie_file):
    with open(cookie_file, "r") as f:
        cookies = json.load(f)
    for cookie in cookies:
        try:
            driver.add_cookie(cookie)
        except:
            pass
    driver.refresh()
    time.sleep(5)
    print("✅ Đã đăng nhập!")

print("\n🎯 BẮT ĐẦU TỰ ĐỘNG ĐĂNG BÀI...")

# Chờ 3 giây để bạn chuyển chuột vào vị trí an toàn
for i in range(3, 0, -1):
    print(f"   Bắt đầu sau {i} giây...")
    time.sleep(1)

# Bước 1: Tìm và click vào ô đăng bài bằng tọa độ (có thể cần điều chỉnh)
print("📌 Bước 1: Click vào ô 'Bạn đang nghĩ gì?'...")
# Tọa độ mặc định - Bạn cần chạy lấy tọa độ thực tế
# Nếu không click được, thay bằng tọa độ phù hợp với màn hình của bạn
post_box_coords = (960, 250)  # (x, y) - CẦN ĐIỀU CHỈNH
pyautogui.click(post_box_coords[0], post_box_coords[1])
time.sleep(2)

# Bước 2: Dán nội dung
print("📌 Bước 2: Dán nội dung...")
pyautogui.hotkey('ctrl', 'v')
time.sleep(2)

# Bước 3: Click nút Đăng
print("📌 Bước 3: Click nút Đăng...")
post_btn_coords = (960, 500)  # CẦN ĐIỀU CHỈNH
pyautogui.click(post_btn_coords[0], post_btn_coords[1])
time.sleep(3)

print("\n✅ ĐÃ ĐĂNG BÀI THÀNH CÔNG!")
input("\n👉 Nhấn Enter để đóng...")
driver.quit()
