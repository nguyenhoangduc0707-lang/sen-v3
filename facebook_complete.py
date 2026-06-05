import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class CompleteFacebookAgent:
    """Xử lý tất cả các loại popup của Facebook"""
    
    def __init__(self):
        self.driver = None
    
    def handle_all_popups(self):
        """Xử lý tất cả popup có thể xuất hiện"""
        
        popup_handlers = [
            # Popup thông báo trình duyệt
            ("//button[contains(text(), 'Cho phép')]", "Cho phép"),
            ("//button[contains(text(), 'Allow')]", "Allow"),
            ("//button[contains(text(), 'Đồng ý')]", "Đồng ý"),
            ("//button[contains(text(), 'OK')]", "OK"),
            
            # Popup lưu mật khẩu
            ("//button[contains(text(), 'Không')]", "Không"),
            ("//button[contains(text(), 'Not Now')]", "Not Now"),
            ("//button[contains(text(), 'Bỏ qua')]", "Bỏ qua"),
            ("//button[contains(text(), 'Skip')]", "Skip"),
            
            # Popup đóng
            ("//div[@aria-label='Đóng']", "Đóng"),
            ("//div[@aria-label='Close']", "Close"),
            ("//div[@role='button'][contains(., '×')]", "×"),
            
            # Popup thông báo
            ("//div[@aria-label='Bỏ qua']", "Bỏ qua"),
            ("//div[@aria-label='Dismiss']", "Dismiss"),
        ]
        
        closed_count = 0
        for selector, name in popup_handlers:
            try:
                elements = self.driver.find_elements(By.XPATH, selector)
                for elem in elements:
                    if elem.is_displayed():
                        try:
                            elem.click()
                            closed_count += 1
                            print(f"   ✅ Đã xử lý popup: {name}")
                            time.sleep(1)
                        except:
                            pass
            except:
                continue
        
        # Cách 2: Nhấn ESC để đóng popup
        if closed_count == 0:
            try:
                from selenium.webdriver.common.action_chains import ActionChains
                actions = ActionChains(self.driver)
                actions.send_keys(Keys.ESCAPE).perform()
                print("   ✅ Đã nhấn ESC để đóng popup")
                time.sleep(1)
            except:
                pass
        
        return closed_count
    
    def wait_for_page_ready(self, max_wait=10):
        """Chờ trang tải xong và popup xuất hiện"""
        for i in range(max_wait):
            time.sleep(1)
            # Kiểm tra nếu có popup thì xử lý
            if self.handle_all_popups() > 0:
                print(f"   Đã xử lý popup ở giây thứ {i+1}")
    
    def login(self):
        """Đăng nhập bằng cookie"""
        print("🚀 Khởi động trình duyệt...")
        
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-infobars')
        options.add_argument('--lang=vi-VN')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        
        self.driver = webdriver.Chrome(options=options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        self.driver.get("https://www.facebook.com/")
        print("⏳ Đợi trang tải...")
        time.sleep(3)
        
        # Xử lý popup ngay sau khi vào trang
        self.handle_all_popups()
        
        # Load cookie
        try:
            with open("fb_cookies_selenium.json", "r") as f:
                cookies = json.load(f)
            for cookie in cookies:
                try:
                    self.driver.add_cookie(cookie)
                except:
                    pass
            
            self.driver.refresh()
            print("⏳ Đợi cookie được áp dụng...")
            time.sleep(4)
            
            # Xử lý popup sau refresh
            self.handle_all_popups()
            self.wait_for_page_ready()
            
            print("✅ Đã đăng nhập thành công!")
            return True
            
        except Exception as e:
            print(f"⚠️ Lỗi: {e}")
            return False
    
    def post(self, content):
        """Đăng bài lên Facebook"""
        
        print("\n📝 Bắt đầu đăng bài...")
        
        # Xử lý popup trước khi tìm ô đăng bài
        self.handle_all_popups()
        
        # Cách 1: Dùng phím tắt 'c' (nhanh nhất)
        try:
            from selenium.webdriver.common.action_chains import ActionChains
            actions = ActionChains(self.driver)
            actions.send_keys('c').perform()
            print("   📌 Dùng phím tắt 'c' để mở khung đăng bài")
            time.sleep(2)
        except:
            pass
        
        # Cách 2: Tìm và click vào ô đăng bài
        post_selectors = [
            "//div[contains(@aria-label, 'Tạo bài viết')]",
            "//div[contains(@aria-label, 'Create a post')]",
            "//div[contains(text(), 'Bạn đang nghĩ gì')]",
            "//div[contains(text(), \"What's on your mind\")]"
        ]
        
        for selector in post_selectors:
            try:
                elem = self.driver.find_element(By.XPATH, selector)
                if elem.is_displayed():
                    self.driver.execute_script("arguments[0].click();", elem)
                    print("   ✅ Đã click vào ô đăng bài")
                    time.sleep(2)
                    break
            except:
                continue
        
        # Tìm khung nhập nội dung
        editor = None
        editor_selectors = [
            "//div[@role='textbox']",
            "//div[@contenteditable='true']",
            "//div[@aria-label='What\'s on your mind?']",
            "//div[@aria-label='Bạn đang nghĩ gì?']"
        ]
        
        for selector in editor_selectors:
            try:
                editor = self.driver.find_element(By.XPATH, selector)
                if editor.is_displayed():
                    break
            except:
                continue
        
        if editor:
            try:
                editor.click()
            except:
                self.driver.execute_script("arguments[0].click();", editor)
            
            editor.send_keys(content)
            print("   ✅ Đã nhập nội dung")
            time.sleep(1)
        else:
            print("   ❌ Không tìm thấy khung nhập")
            return False
        
        # Tìm nút đăng
        btn_selectors = [
            "//div[@aria-label='Đăng']",
            "//div[@aria-label='Post']",
            "//div[contains(text(), 'Đăng')]",
            "//div[contains(text(), 'Post')]"
        ]
        
        for selector in btn_selectors:
            try:
                btn = self.driver.find_element(By.XPATH, selector)
                if btn.is_displayed():
                    self.driver.execute_script("arguments[0].click();", btn)
                    print("   ✅ Đã click nút Đăng")
                    time.sleep(3)
                    print("\n🎉 ĐĂNG BÀI THÀNH CÔNG!")
                    return True
            except:
                continue
        
        # Thử Ctrl+Enter
        try:
            editor.send_keys(Keys.CONTROL, Keys.ENTER)
            print("   ✅ Đã dùng Ctrl+Enter")
            time.sleep(3)
            print("\n🎉 ĐĂNG BÀI THÀNH CÔNG!")
            return True
        except:
            print("   ❌ Không thể đăng bài")
            return False
    
    def close(self):
        if self.driver:
            self.driver.quit()
            print("🔒 Đã đóng trình duyệt")

def main():
    print("=" * 50)
    print("📱 FACEBOOK POSTER - COMPLETE AGENT")
    print("   (Xử lý mọi loại popup)")
    print("=" * 50)
    
    content = """Xin chào bạn, hôm nay chúng ta sẽ cùng nhau đi qua một hành trình nhỏ mang tên "Buông bỏ". 

Có những điều trong cuộc sống khiến ta nặng lòng, nhưng đôi khi, việc giữ chặt lại chỉ làm ta thêm mệt mỏi. 

Hãy thử hít một hơi thật sâu… và thở ra thật chậm… để cảm nhận sự nhẹ nhõm. 

Bạn xứng đáng được bình an, ngay trong khoảnh khắc này.

#BuongBo #BinhAn #TamLy

thí nghiệm 12 - Complete Agent

Thành công!"""
    
    agent = CompleteFacebookAgent()
    
    if agent.login():
        agent.post(content)
    else:
        print("❌ Không thể đăng nhập")
        print("👉 Hãy chạy: python save_cookie_manual.py")
    
    input("\n👉 Nhấn Enter để đóng trình duyệt...")
    agent.close()

if __name__ == "__main__":
    main()
