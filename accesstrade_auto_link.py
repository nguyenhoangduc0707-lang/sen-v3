"""
Auto Fetch AccessTrade Links using Selenium
- Tự động đăng nhập
- Lấy danh sách campaign links
- Lưu vào file JSON
"""
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os

class AccessTradeAutoLink:
    def __init__(self, username=None, password=None):
        self.username = username or os.getenv("duc070719997")
        self.password = password or os.getenv("0326014497")
        self.driver = None
        self.links = []
    
    def setup_driver(self):
        """Khởi tạo Chrome driver"""
        chrome_options = Options()
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--start-maximized")
        # chrome_options.add_argument("--headless")  # Bỏ comment để chạy ẩn
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 30)
    
    def login(self):
        """Đăng nhập AccessTrade"""
        print("🔐 Đang đăng nhập AccessTrade...")
        self.driver.get("https://pub.accesstrade.vn/login")
        time.sleep(2)
        
        # Nhập username/email
        email_input = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email'], input[name='email'], input[name='username']"))
        )
        email_input.send_keys(self.username)
        
        # Nhập password
        pwd_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        pwd_input.send_keys(self.password)
        
        # Click nút đăng nhập
        login_btn = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_btn.click()
        
        time.sleep(5)
        print("✅ Đăng nhập thành công!")
    
    def navigate_to_campaigns(self):
        """Chuyển đến trang campaigns"""
        print("📂 Đang truy cập trang campaigns...")
        
        # Thử nhiều cách để vào campaigns
        try:
            # Cách 1: Click vào menu Campaigns
            campaigns_link = self.wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Campaigns"))
            )
            campaigns_link.click()
        except:
            try:
                # Cách 2: Tìm bằng href
                campaigns_link = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='campaign']"))
                )
                campaigns_link.click()
            except:
                # Cách 3: Đi trực tiếp bằng URL
                self.driver.get("https://pub.accesstrade.vn/campaigns")
        
        time.sleep(3)
        print("✅ Đã vào trang campaigns")
    
    def get_affiliate_links(self):
        """Lấy danh sách link affiliate"""
        print("🔗 Đang lấy link affiliate...")
        
        # Tìm tất cả các nút/card campaign
        campaigns = self.driver.find_elements(By.CSS_SELECTOR, 
            ".campaign-item, .campaign-card, [class*='campaign'], tr")
        
        links_data = []
        
        for i, campaign in enumerate(campaigns[:20]):  # Lấy 20 campaign đầu
            try:
                # Lấy tên campaign
                name = campaign.find_element(By.CSS_SELECTOR, ".name, .title, h3, h4").text
                
                # Tìm nút lấy link
                get_link_btn = campaign.find_element(By.CSS_SELECTOR, 
                    "button:contains('Get Link'), a:contains('Get Link'), .get-link-btn")
                
                # Click để lấy link
                get_link_btn.click()
                time.sleep(1)
                
                # Copy link từ popup hoặc input
                link_input = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input[readonly], .link-text"))
                )
                link = link_input.get_attribute("value")
                
                links_data.append({
                    "name": name,
                    "link": link,
                    "fetched_at": time.strftime("%Y-%m-%d %H:%M:%S")
                })
                
                print(f"   ✅ Lấy link: {name[:40]}...")
                
                # Đóng popup
                close_btn = self.driver.find_element(By.CSS_SELECTOR, ".close, button[aria-label='Close']")
                close_btn.click()
                time.sleep(1)
                
            except Exception as e:
                print(f"   ⚠️ Bỏ qua campaign {i}: {e}")
                continue
        
        return links_data
    
    def save_links(self, links, filename="accesstrade_links.json"):
        """Lưu links vào file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(links, f, indent=2, ensure_ascii=False)
        print(f"✅ Đã lưu {len(links)} link vào {filename}")
    
    def run(self):
        """Chạy toàn bộ quy trình"""
        try:
            self.setup_driver()
            self.login()
            self.navigate_to_campaigns()
            links = self.get_affiliate_links()
            self.save_links(links)
            return links
        except Exception as e:
            print(f"❌ Lỗi: {e}")
            return []
        finally:
            if self.driver:
                self.driver.quit()

# Hướng dẫn cấu hình
print("=" * 60)
print("🔐 CẤU HÌNH TÀI KHOẢN ACCESSTRADE")
print("=" * 60)
print("""
1. Set environment variables:
   setx ACCESSTRADE_USERNAME "your_email@example.com"
   setx ACCESSTRADE_PASSWORD "your_password"

2. Hoặc sửa trực tiếp trong code

3. Chạy script:
   python accesstrade_auto_link.py
""")
print("=" * 60)

if __name__ == "__main__":
    # Cấu hình tài khoản (thay bằng thông tin thật)
    # Hoặc dùng environment variables
    USERNAME = "nguyenhoangduc0707@gmail.com"  # Thay bằng email thật
    PASSWORD = ""  # Thay bằng mật khẩu thật
    
    if PASSWORD:
        bot = AccessTradeAutoLink(USERNAME, PASSWORD)
        links = bot.run()
        print(f"\n🎯 Lấy được {len(links)} link affiliate!")
    else:
        print("⚠️ Vui lòng cập nhật USERNAME và PASSWORD trong script!")
