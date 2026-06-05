from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import json
import os

print("=" * 50)
print("🤖 FACEBOOK AUTO POSTER - SELENIUM")
print("=" * 50)

# Cấu hình Chrome
options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--no-sandbox')
options.add_argument('--disable-infobars')
options.add_argument('--lang=vi-VN')
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)

# Tự động tải ChromeDriver
service = Service(ChromeDriverManager().install())

print("🚀 Đang khởi động Chrome...")
driver = webdriver.Chrome(service=service, options=options)

# Ẩn webdriver
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

driver.get("https://www.facebook.com/")
print("✅ Đã mở Facebook!")

# Kiểm tra cookie
cookie_file = "fb_cookies_selenium.json"
if os.path.exists(cookie_file):
    print("🍪 Load cookies...")
    with open(cookie_file, "r") as f:
        cookies = json.load(f)
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.refresh()
    time.sleep(3)

if "login" in driver.current_url:
    print("\n📌 ĐĂNG NHẬP LẦN ĐẦU")
    print("👉 Vui lòng đăng nhập THỦ CÔNG trong trình duyệt")
    input("✅ Sau khi đăng nhập xong, nhấn Enter...")
    
    # Lưu cookie
    cookies = driver.get_cookies()
    with open(cookie_file, "w") as f:
        json.dump(cookies, f)
    print(f"✅ Đã lưu {len(cookies)} cookies")

print("\n✅ Sẵn sàng đăng bài!")

# Nhập nội dung
print("\n📝 Nhập nội dung bài đăng (Enter 2 lần để kết thúc):")
lines = []
while True:
    line = input()
    if line == "":
        break
    lines.append(line)

message = "\n".join(lines)

if message:
    try:
        # Tìm ô đăng bài
        post_box = driver.find_element(By.XPATH, "//div[contains(@aria-label, 'Tạo bài viết')]")
        post_box.click()
        time.sleep(2)
        
        editor = driver.find_element(By.XPATH, "//div[@role='textbox']")
        editor.click()
        editor.send_keys(message)
        time.sleep(2)
        
        post_btn = driver.find_element(By.XPATH, "//div[@aria-label='Đăng']")
        post_btn.click()
        time.sleep(3)
        print("✅ Đã đăng bài!")
    except Exception as e:
        print(f"⚠️ Lỗi: {e}")
        print("👉 Hãy đăng bài THỦ CÔNG trong trình duyệt")
        input("✅ Sau khi đăng xong, nhấn Enter...")

input("\n👉 Nhấn Enter để đóng...")
driver.quit()
