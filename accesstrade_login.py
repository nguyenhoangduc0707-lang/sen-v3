"""
AccessTrade Auto Link - Read from .env file
"""
import os
import time
import json
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Lấy thông tin từ .env
USERNAME = os.getenv("ACCESSTRADE_USERNAME")
PASSWORD = os.getenv("ACCESSTRADE_PASSWORD")

if not USERNAME:
    USERNAME = "nguyenhoangduc0707@gmail.com"  # fallback

print("=" * 60)
print("🔐 ACCESSTRADE AUTO LINK")
print("=" * 60)

if not PASSWORD:
    print("❌ Chưa có mật khẩu trong .env!")
    print("\n👉 Hãy thêm vào file .env:")
    print('   ACCESSTRADE_PASSWORD="mat_khau_cua_ban"')
    print("\nHoặc chạy lệnh:")
    print('   echo "ACCESSTRADE_PASSWORD=mat_khau_cua_ban" >> .env')
    exit(1)

print(f"✅ Username: {USERNAME}")
print(f"✅ Password: {'*' * len(PASSWORD)}")

# Thử import selenium
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service
    print("✅ Selenium loaded")
except ImportError as e:
    print(f"❌ Thiếu thư viện: {e}")
    print("\n👉 Chạy lệnh:")
    print("   pip install selenium webdriver-manager python-dotenv")
    exit(1)

# Khởi tạo driver
print("\n🚀 Khởi tạo Chrome driver...")
options = webdriver.ChromeOptions()
options.add_argument("--disable-notifications")
options.add_argument("--start-maximized")

try:
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 30)
    print("✅ Driver ready")
except Exception as e:
    print(f"❌ Lỗi driver: {e}")
    exit(1)

try:
    # Đăng nhập
    print("\n🔐 Đang đăng nhập AccessTrade...")
    driver.get("https://pub.accesstrade.vn/login")
    time.sleep(3)
    
    # Nhập email
    email_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']")))
    email_input.clear()
    email_input.send_keys(USERNAME)
    
    # Nhập password
    pwd_input = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
    pwd_input.clear()
    pwd_input.send_keys(PASSWORD)
    
    # Click login
    login_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    login_btn.click()
    
    time.sleep(5)
    
    # Kiểm tra đăng nhập thành công
    if "login" in driver.current_url.lower():
        print("❌ Đăng nhập thất bại! Kiểm tra lại mật khẩu.")
    else:
        print("✅ Đăng nhập thành công!")
        
        # Đi đến campaigns
        print("\n📂 Đang truy cập campaigns...")
        driver.get("https://pub.accesstrade.vn/campaigns")
        time.sleep(5)
        
        print("\n🎯 Đã sẵn sàng! Bạn có thể tự tay lấy link.")
        print("👉 Nhấn Enter để đóng trình duyệt...")
        input()
    
except Exception as e:
    print(f"❌ Lỗi: {e}")
finally:
    driver.quit()
    print("\n✅ Đã đóng trình duyệt")
