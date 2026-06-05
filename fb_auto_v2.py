from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import json
import os

print("=" * 50)
print("🤖 FACEBOOK AUTO POSTER - V2")
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
time.sleep(3)

# Load cookie nếu có
cookie_file = "fb_cookies_selenium.json"
if os.path.exists(cookie_file):
    print("🍪 Load cookies...")
    with open(cookie_file, "r") as f:
        cookies = json.load(f)
    for cookie in cookies:
        try:
            driver.add_cookie(cookie)
        except:
            pass
    driver.refresh()
    time.sleep(3)

# Kiểm tra đăng nhập
if "login" in driver.current_url:
    print("\n📌 ĐĂNG NHẬP LẦN ĐẦU")
    print("👉 Đăng nhập THỦ CÔNG trong trình duyệt")
    input("✅ Sau khi đăng nhập xong, nhấn Enter...")
    
    # Lưu cookie
    cookies = driver.get_cookies()
    with open(cookie_file, "w") as f:
        json.dump(cookies, f)
    print(f"✅ Đã lưu {len(cookies)} cookies")

print("\n✅ Đã đăng nhập!")

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
    print("\n📝 Đang tìm ô đăng bài...")
    
    # CÁCH 1: Dùng phím tắt (nhanh nhất)
    try:
        print("   Cách 1: Dùng phím tắt 'Chrome'...")
        driver.find_element(By.TAG_NAME, 'body').send_keys('c')
        time.sleep(1)
    except:
        pass
    
    # CÁCH 2: Tìm bằng nhiều selector khác nhau
    selectors = [
        "//div[contains(@aria-label, 'Tạo bài viết')]",
        "//div[contains(@aria-label, 'Create a post')]",
        "//span[contains(text(), 'Bạn đang nghĩ gì')]",
        "//div[@role='button' and contains(@class, 'x1i10hfl')]",
        "//div[contains(@class, 'x1y1aw1k')]//div[@role='button']"
    ]
    
    post_found = False
    for selector in selectors:
        try:
            elem = driver.find_element(By.XPATH, selector)
            if elem.is_displayed() and elem.is_enabled():
                elem.click()
                print(f"   ✅ Đã click bằng selector: {selector[:50]}")
                post_found = True
                break
        except:
            continue
    
    if not post_found:
        # CÁCH 3: Tìm tất cả div button và kiểm tra text
        print("   Cách 3: Tìm trong tất cả button...")
        buttons = driver.find_elements(By.XPATH, "//div[@role='button']")
        for btn in buttons:
            try:
                text = btn.text
                if "nghĩ" in text or "What" in text or "post" in text:
                    btn.click()
                    print(f"   ✅ Đã click vào button có text: {text[:30]}")
                    post_found = True
                    break
            except:
                continue
    
    time.sleep(2)
    
    # Tìm khung nhập
    editor_selectors = [
        "//div[@role='textbox']",
        "//div[@contenteditable='true']",
        "//div[@aria-label='What\'s on your mind?']",
        "//div[@aria-label='Bạn đang nghĩ gì?']"
    ]
    
    editor_found = False
    for selector in editor_selectors:
        try:
            editor = driver.find_element(By.XPATH, selector)
            if editor.is_displayed():
                editor.click()
                editor.send_keys(message)
                print(f"   ✅ Đã nhập nội dung")
                editor_found = True
                break
        except:
            continue
    
    if not editor_found:
        print("⚠️ Không tìm thấy khung nhập, dùng Javascript")
        driver.execute_script(f"document.querySelector('[role=\"textbox\"]').innerText = '{message[:100]}'")
    
    time.sleep(2)
    
    # Tìm nút đăng
    post_btn_selectors = [
        "//div[@aria-label='Đăng']",
        "//div[@aria-label='Post']",
        "//div[@role='button' and contains(., 'Đăng')]",
        "//div[@role='button' and contains(., 'Post')]"
    ]
    
    for selector in post_btn_selectors:
        try:
            btn = driver.find_element(By.XPATH, selector)
            if btn.is_displayed():
                btn.click()
                print("   ✅ Đã click nút Đăng")
                time.sleep(3)
                print("\n✅ ĐĂNG BÀI THÀNH CÔNG!")
                break
        except:
            continue

print("\n👉 Nhấn Enter để đóng trình duyệt...")
input()
driver.quit()
