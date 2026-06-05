import undetected_chromedriver as uc
import time
import json

driver = uc.Chrome(headless=False)
driver.get('https://www.facebook.com/')

# Đăng nhập thủ công lần đầu
input("👉 Đăng nhập xong thì nhấn Enter...")

# Lưu cookies
cookies = driver.get_cookies()
with open('facebook_cookies.json', 'w') as f:
    json.dump(cookies, f)

# Lần sau load cookies
# for cookie in cookies:
#     driver.add_cookie(cookie)

print("✅ Thành công!")
