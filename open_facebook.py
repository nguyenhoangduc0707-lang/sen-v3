from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json
import os
import time

print("=" * 50)
print("📱 MỞ TRÌNH DUYỆT ĐÃ ĐĂNG NHẬP")
print("=" * 50)

options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--no-sandbox')
options.add_argument('--disable-infobars')
options.add_argument('--lang=vi-VN')
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)

service = Service(ChromeDriverManager().install())

print("🚀 Đang khởi động Chrome...")
driver = webdriver.Chrome(service=service, options=options)

driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

driver.get("https://www.facebook.com/")
time.sleep(2)

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
    print("✅ Đã load cookies!")
else:
    print("⚠️ Chưa có cookies, cần đăng nhập thủ công lần đầu")

print("\n✅ Bạn đã đăng nhập vào Facebook!")
print("📝 Hãy đăng bài THỦ CÔNG trong trình duyệt")
print("\n👉 Sau khi đăng bài xong, quay lại đây và nhấn Enter")

input()

print("\n🔒 Đang đóng trình duyệt...")
driver.quit()
print("✅ Hoàn tất!")
