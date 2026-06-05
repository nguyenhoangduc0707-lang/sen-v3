import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class FixedFacebookAgent:
    """Phiên bản xử lý popup và overlay"""
    
    def __init__(self):
        self.driver = None
    
    def close_popups(self):
        """Đóng các popup có thể xuất hiện"""
        
        popup_selectors = [
            "//div[@aria-label='Đóng']",
            "//div[@aria-label='Close']",
            "//div[contains(@class, 'x1i10hfl')][contains(text(), 'Đóng')]",
            "//div[@role='button'][contains(., 'Bỏ qua')]",
            "//div[@role='button'][contains(., 'Skip')]",
            "//div[@role='button'][contains(., 'Not Now')]",
            "//div[@role='button'][contains(., 'Không phải bây giờ')]"
        ]
        
        for selector in popup_selectors:
            try:
                popup = self.driver.find_element(By.XPATH, selector)
                if popup.is_displayed():
                    popup.click()
                    print("   ✅ Đã đóng popup")
                    time.sleep(1)
            except:
                continue
    
    def click_by_js(self, element):
        """Click bằng JavaScript (vượt qua mọi overlay)"""
        self.driver.execute_script("arguments[0].click();", element)
        return True
    
    def find_and_click_post_box(self):
        """Tìm và click vào ô đăng bài bằng nhiều cách"""
        
        selectors = [
            "//div[contains(@aria-label, 'Tạo bài viết')]",
            "//div[contains(@aria-label, 'Create a post')]",
            "//div[contains(text(), 'Bạn đang nghĩ gì')]",
            "//div[contains(text(), \"What's on your mind\")]",
            "//div[@role='button'][contains(@class, 'x1i10hfl')]//span[contains(text(), 'Bạn đang nghĩ gì')]"
        ]
        
        for selector in selectors:
            try:
                elem = self.driver.find_element(By.XPATH, selector)
                if elem.is_displayed():
                    # Thử click thường
                    try:
                        elem.click()
                    except:
                        # Nếu bị chặn, dùng JavaScript
                        self.click_by_js(elem)
                    print(f"   ✅ Đã click vào ô đăng bài")
                    return True
            except:
                continue
        
        # Cách cuối: Dùng phím tắt 'c' để mở hộp thoại
        try:
            from selenium.webdriver.common.action_chains import ActionChains
            actions = ActionChains(self.driver)
            actions.send_keys('c').perform()
            print("   ✅ Đã dùng phím tắt 'c' để mở hộp thoại")
            return True
        except:
            pass
        
        return False
    
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
        time.sleep(3)
        
        # Đóng popup nếu có
        self.close_popups()
        
        try:
            with open("fb_cookies_selenium.json", "r") as f:
                cookies = json.load(f)
            for cookie in cookies:
                try:
                    self.driver.add_cookie(cookie)
                except:
                    pass
            self.driver.refresh()
            time.sleep(4)
            print("✅ Đã đăng nhập bằng cookie")
            
            # Đóng popup sau khi refresh
            self.close_popups()
            return True
        except Exception as e:
            print(f"⚠️ Không load được cookie: {e}")
            return False
    
    def post(self, content):
        """Đăng bài lên Facebook"""
        
        print("\n📝 Bắt đầu đăng bài...")
        
        # Đóng popup trước khi tìm ô đăng bài
        self.close_popups()
        
        # Tìm và click vào ô đăng bài
        if not self.find_and_click_post_box():
            print("❌ Không tìm thấy ô đăng bài")
            return False
        
        time.sleep(2)
        
        # Tìm khung nhập nội dung
        editor_selectors = [
            "//div[@role='textbox']",
            "//div[@contenteditable='true']",
            "//div[@aria-label='What\'s on your mind?']",
            "//div[@aria-label='Bạn đang nghĩ gì?']"
        ]
        
        editor = None
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
                self.click_by_js(editor)
            editor.send_keys(content)
            time.sleep(1)
            print("✅ Đã nhập nội dung")
        else:
            print("❌ Không tìm thấy khung nhập")
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
                post_btn = self.driver.find_element(By.XPATH, selector)
                if post_btn.is_displayed():
                    try:
                        post_btn.click()
                    except:
                        self.click_by_js(post_btn)
                    time.sleep(3)
                    print("🎉 ĐĂNG BÀI THÀNH CÔNG!")
                    return True
            except:
                continue
        
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
    print("📱 FACEBOOK POSTER - FIXED AGENT")
    print("=" * 50)
    
    content = """Xin chào bạn, hôm nay chúng ta sẽ cùng nhau đi qua một hành trình nhỏ mang tên "Buông bỏ". 

Có những điều trong cuộc sống khiến ta nặng lòng, nhưng đôi khi, việc giữ chặt lại chỉ làm ta thêm mệt mỏi. 

Hãy thử hít một hơi thật sâu… và thở ra thật chậm… để cảm nhận sự nhẹ nhõm. 

Bạn xứng đáng được bình an, ngay trong khoảnh khắc này.

#BuongBo #BinhAn #TamLy

thí nghiệm 11 - Fixed Agent

Thành công!"""
    
    agent = FixedFacebookAgent()
    
    if agent.login():
        agent.post(content)
    else:
        print("❌ Không thể đăng nhập")
    
    input("\n👉 Nhấn Enter để đóng trình duyệt...")
    agent.close()

if __name__ == "__main__":
    main()
