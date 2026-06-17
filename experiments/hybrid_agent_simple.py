import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class SimpleFacebookAgent:
    """Phiên bản đơn giản không cần BeautifulSoup và không cần API key"""
    
    def __init__(self):
        self.driver = None
    
    def find_post_box(self):
        """Tìm ô đăng bài bằng nhiều cách"""
        
        selectors = [
            "//div[contains(@aria-label, 'Tạo bài viết')]",
            "//div[contains(@aria-label, 'Create a post')]",
            "//div[contains(text(), 'Bạn đang nghĩ gì')]",
            "//div[contains(text(), \"What's on your mind\")]"
        ]
        
        for selector in selectors:
            try:
                elem = self.driver.find_element(By.XPATH, selector)
                if elem.is_displayed():
                    return elem
            except:
                continue
        return None
    
    def find_post_button(self):
        """Tìm nút đăng bằng nhiều cách"""
        
        selectors = [
            "//div[@aria-label='Đăng']",
            "//div[@aria-label='Post']",
            "//div[contains(text(), 'Đăng')]",
            "//div[contains(text(), 'Post')]"
        ]
        
        for selector in selectors:
            try:
                btn = self.driver.find_element(By.XPATH, selector)
                if btn.is_displayed() and btn.is_enabled():
                    return btn
            except:
                continue
        return None
    
    def login(self):
        """Đăng nhập bằng cookie"""
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-infobars')
        options.add_argument('--lang=vi-VN')
        
        self.driver = webdriver.Chrome(options=options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        self.driver.get("https://www.facebook.com/")
        time.sleep(2)
        
        try:
            with open("fb_cookies_selenium.json", "r") as f:
                cookies = json.load(f)
            for cookie in cookies:
                try:
                    self.driver.add_cookie(cookie)
                except:
                    pass
            self.driver.refresh()
            time.sleep(3)
            print("✅ Đã đăng nhập bằng cookie")
            return True
        except Exception as e:
            print(f"⚠️ Không load được cookie: {e}")
            return False
    
    def post(self, content):
        """Đăng bài lên Facebook"""
        
        print("\n📝 Bắt đầu đăng bài...")
        
        # Tìm và click vào ô đăng bài
        post_box = self.find_post_box()
        if post_box:
            post_box.click()
            time.sleep(2)
            print("✅ Đã click vào ô đăng bài")
        else:
            print("❌ Không tìm thấy ô đăng bài")
            return False
        
        # Tìm khung nhập nội dung
        try:
            editor = self.driver.find_element(By.XPATH, "//div[@role='textbox']")
            editor.click()
            editor.send_keys(content)
            time.sleep(1)
            print("✅ Đã nhập nội dung")
        except Exception as e:
            print(f"❌ Không tìm thấy khung nhập: {e}")
            return False
        
        # Tìm và click nút đăng
        post_btn = self.find_post_button()
        if post_btn:
            post_btn.click()
            time.sleep(3)
            print("🎉 ĐĂNG BÀI THÀNH CÔNG!")
            return True
        else:
            # Thử dùng phím tắt Ctrl+Enter
            try:
                editor.send_keys(Keys.CONTROL, Keys.ENTER)
                time.sleep(3)
                print("✅ Đã dùng Ctrl+Enter để đăng bài")
                return True
            except:
                print("❌ Không tìm thấy nút đăng")
                return False
    
    def close(self):
        if self.driver:
            self.driver.quit()
            print("🔒 Đã đóng trình duyệt")

def main():
    print("=" * 50)
    print("📱 FACEBOOK POSTER - SIMPLE AGENT")
    print("=" * 50)
    
    # Nội dung bài đăng
    content = """Xin chào bạn, hôm nay chúng ta sẽ cùng nhau đi qua một hành trình nhỏ mang tên "Buông bỏ". 

Có những điều trong cuộc sống khiến ta nặng lòng, nhưng đôi khi, việc giữ chặt lại chỉ làm ta thêm mệt mỏi. 

Hãy thử hít một hơi thật sâu… và thở ra thật chậm… để cảm nhận sự nhẹ nhõm. 

Bạn xứng đáng được bình an, ngay trong khoảnh khắc này.

#BuongBo #BinhAn #TamLy

thí nghiệm 10 - Simple Agent

Thành công!"""
    
    agent = SimpleFacebookAgent()
    
    if agent.login():
        agent.post(content)
    else:
        print("❌ Không thể đăng nhập")
        print("👉 Hãy chạy python save_cookie_manual.py trước để lưu cookie")
    
    input("\n👉 Nhấn Enter để đóng trình duyệt...")
    agent.close()

if __name__ == "__main__":
    main()
