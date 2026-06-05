import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class StepByStepFacebookAgent:
    """Chạy từng bước, chờ xác nhận của người dùng"""
    
    def __init__(self):
        self.driver = None
    
    def wait_for_user(self, step_name, instruction):
        """Chờ người dùng xác nhận trước khi tiếp tục"""
        print("\n" + "=" * 60)
        print(f"📌 BƯỚC: {step_name}")
        print(f"📝 HƯỚNG DẪN: {instruction}")
        print("=" * 60)
        response = input("👉 Đã sẵn sàng? (y/n/yes để tiếp tục, hoặc nhấn Enter để tiếp): ")
        return response.lower() in ['y', 'yes', '']
    
    def login(self):
        """Đăng nhập bằng cookie - từng bước"""
        
        if not self.wait_for_user("MỞ TRÌNH DUYỆT", "Script sẽ mở Chrome và vào Facebook"):
            return False
        
        print("🚀 Đang khởi động Chrome...")
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-infobars')
        options.add_argument('--lang=vi-VN')
        
        self.driver = webdriver.Chrome(options=options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        self.driver.get("https://www.facebook.com/")
        print("✅ Đã mở Facebook")
        time.sleep(3)
        
        if not self.wait_for_user("TẢI COOKIE", "Script sẽ load cookie để đăng nhập tự động"):
            return False
        
        try:
            with open("fb_cookies_selenium.json", "r") as f:
                cookies = json.load(f)
            for cookie in cookies:
                try:
                    self.driver.add_cookie(cookie)
                except:
                    pass
            self.driver.refresh()
            print("✅ Đã load cookie và refresh trang")
            time.sleep(4)
            
            if not self.wait_for_user("KIỂM TRA ĐĂNG NHẬP", "Hãy nhìn trình duyệt xem đã đăng nhập thành công chưa?"):
                return False
            
            print("✅ Đăng nhập thành công!")
            return True
            
        except Exception as e:
            print(f"❌ Lỗi: {e}")
            return False
    
    def handle_popups(self):
        """Xử lý popup - từng bước"""
        
        if not self.wait_for_user("XỬ LÝ POPUP", "Script sẽ tìm và đóng các popup (thông báo, cho phép...)"):
            return
        
        popup_selectors = [
            ("//button[contains(text(), 'Cho phép')]", "Cho phép"),
            ("//button[contains(text(), 'Allow')]", "Allow"),
            ("//button[contains(text(), 'Không')]", "Không"),
            ("//button[contains(text(), 'Not Now')]", "Not Now"),
            ("//div[@aria-label='Đóng']", "Đóng"),
        ]
        
        closed = 0
        for selector, name in popup_selectors:
            try:
                elements = self.driver.find_elements(By.XPATH, selector)
                for elem in elements:
                    if elem.is_displayed():
                        elem.click()
                        closed += 1
                        print(f"   ✅ Đã đóng popup: {name}")
                        time.sleep(1)
            except:
                continue
        
        if closed == 0:
            print("   ℹ️ Không thấy popup nào")
        
        self.wait_for_user("XÁC NHẬN POPUP", "Hãy nhìn trình duyệt, popup đã được xử lý chưa?")
    
    def find_post_box(self):
        """Tìm ô đăng bài - từng bước"""
        
        if not self.wait_for_user("TÌM Ô ĐĂNG BÀI", "Script sẽ tìm và click vào ô 'Bạn đang nghĩ gì?'"):
            return False
        
        # Thử phím tắt 'c'
        try:
            from selenium.webdriver.common.action_chains import ActionChains
            actions = ActionChains(self.driver)
            actions.send_keys('c').perform()
            print("   ✅ Đã dùng phím tắt 'c'")
            time.sleep(2)
            return True
        except:
            pass
        
        # Tìm bằng selector
        selectors = [
            "//div[contains(@aria-label, 'Tạo bài viết')]",
            "//div[contains(@aria-label, 'Create a post')]",
            "//div[contains(text(), 'Bạn đang nghĩ gì')]",
        ]
        
        for selector in selectors:
            try:
                elem = self.driver.find_element(By.XPATH, selector)
                if elem.is_displayed():
                    self.driver.execute_script("arguments[0].click();", elem)
                    print(f"   ✅ Đã click vào ô đăng bài")
                    time.sleep(2)
                    return True
            except:
                continue
        
        print("   ❌ Không tìm thấy ô đăng bài")
        return False
    
    def enter_content(self, content):
        """Nhập nội dung - từng bước"""
        
        print("\n📝 NỘI DUNG SẼ ĐĂNG:")
        print("-" * 40)
        print(content)
        print("-" * 40)
        
        if not self.wait_for_user("NHẬP NỘI DUNG", "Script sẽ tự động nhập nội dung trên vào khung soạn bài"):
            return False
        
        editor_selectors = [
            "//div[@role='textbox']",
            "//div[@contenteditable='true']",
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
                self.driver.execute_script("arguments[0].click();", editor)
            
            editor.send_keys(content)
            print("   ✅ Đã nhập nội dung")
            time.sleep(2)
            
            self.wait_for_user("KIỂM TRA NỘI DUNG", "Hãy nhìn trình duyệt xem nội dung đã đúng chưa?")
            return True
        else:
            print("   ❌ Không tìm thấy khung nhập")
            return False
    
    def post(self):
        """Đăng bài - từng bước"""
        
        if not self.wait_for_user("ĐĂNG BÀI", "Script sẽ tìm và click nút Đăng"):
            return False
        
        btn_selectors = [
            "//div[@aria-label='Đăng']",
            "//div[@aria-label='Post']",
            "//div[contains(text(), 'Đăng')]",
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
            editor = self.driver.find_element(By.XPATH, "//div[@role='textbox']")
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
    print("=" * 60)
    print("🤖 FACEBOOK POSTER - CHẾ ĐỘ TỪNG BƯỚC")
    print("   Bạn sẽ xác nhận từng thao tác trước khi thực hiện")
    print("=" * 60)
    
    content = """Xin chào bạn, hôm nay chúng ta sẽ cùng nhau đi qua một hành trình nhỏ mang tên "Buông bỏ". 

Có những điều trong cuộc sống khiến ta nặng lòng, nhưng đôi khi, việc giữ chặt lại chỉ làm ta thêm mệt mỏi. 

Hãy thử hít một hơi thật sâu… và thở ra thật chậm… để cảm nhận sự nhẹ nhõm. 

Bạn xứng đáng được bình an, ngay trong khoảnh khắc này.

#BuongBo #BinhAn #TamLy

thí nghiệm 13 - Step by Step

Thành công!"""
    
    agent = StepByStepFacebookAgent()
    
    # Từng bước có xác nhận
    if not agent.login():
        print("❌ Dừng lại do lỗi đăng nhập")
        agent.close()
        return
    
    agent.handle_popups()
    
    if not agent.find_post_box():
        print("❌ Không tìm thấy ô đăng bài")
        agent.close()
        return
    
    if not agent.enter_content(content):
        print("❌ Không thể nhập nội dung")
        agent.close()
        return
    
    agent.post()
    
    input("\n✅ HOÀN TẤT! Nhấn Enter để đóng trình duyệt...")
    agent.close()

if __name__ == "__main__":
    main()
