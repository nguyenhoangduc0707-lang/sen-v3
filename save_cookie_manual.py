from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json
import os
import time

print("=" * 50)
print("🍪 LƯU COOKIE FACEBOOK")
print("=" * 50)

options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
service = Service(ChromeDriverManager().install())

driver = webdriver.Chrome(service=service, options=options)
driver.get("https://www.facebook.com/")
time.sleep(2)

print("\n👉 Đăng nhập THỦ CÔNG trong trình duyệt")
input("✅ Sau khi đăng nhập xong, nhấn Enter...")

# Lưu cookie
cookies = driver.get_cookies()
with open("fb_cookies_selenium.json", "w") as f:
    json.dump(cookies, f)

print(f"\n✅ Đã lưu {len(cookies)} cookies vào fb_cookies_selenium.json")
print("🎉 Lần sau chạy sẽ tự động đăng nhập!")

input("\n👉 Nhấn Enter để đóng...")
driver.quit()
