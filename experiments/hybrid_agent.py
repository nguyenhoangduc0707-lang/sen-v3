import time
import json
from selenium import webdriver
from dom_agent import DOMAgent
from computer_use_agent import ComputerUseAgent

class HybridFacebookAgent:
    """Kết hợp DOM Agent và Computer Use Agent để đăng bài tối ưu"""
    
    def __init__(self):
        self.dom_agent = DOMAgent()
        self.vision_agent = ComputerUseAgent()
        self.driver = None
    
    def post_to_facebook(self, content):
        print("🚀 BẮT ĐẦU QUY TRÌNH ĐĂNG BÀI THÔNG MINH")
        print("=" * 50)
        
        # Khởi tạo trình duyệt
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        self.driver = webdriver.Chrome(options=options)
        self.driver.get("https://www.facebook.com/")
        
        # Load cookie
        with open("fb_cookies_selenium.json", "r") as f:
            cookies = json.load(f)
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        self.driver.refresh()
        time.sleep(3)
        
        print("✅ Đã đăng nhập")
        
        # === TẦNG 1: DÙNG DOM AGENT ===
        print("\n🔍 TẦNG 1: DOM Agent tìm kiếm...")
        
        post_box = self.dom_agent.find_post_box_by_attributes(self.driver)
        if post_box:
            print("✅ DOM Agent tìm thấy ô đăng bài!")
            post_box.click()
            time.sleep(2)
            
            # Nhập nội dung
            editor = self.driver.find_element("xpath", "//div[@role='textbox']")
            editor.send_keys(content)
            time.sleep(1)
            
            # Tìm nút đăng
            post_btn = self.dom_agent.find_post_button_by_text(self.driver)
            if post_btn:
                print("✅ DOM Agent tìm thấy nút Đăng!")
                post_btn.click()
                print("🎉 ĐĂNG BÀI THÀNH CÔNG VỚI DOM AGENT!")
                return True
        else:
            print("⚠️ DOM Agent không tìm thấy, chuyển sang TẦNG 2...")
        
        # === TẦNG 2: DÙNG AI VISION AGENT ===
        print("\n🧠 TẦNG 2: AI Vision Agent (Computer Use)...")
        
        # Lưu nội dung vào clipboard
        import subprocess
        subprocess.run("clip", input=content.encode("utf-8"), check=True)
        
        # Dùng AI để tìm và click
        result = self.vision_agent.ask_ai_where_to_click("Tìm và click vào ô 'Bạn đang nghĩ gì?' để mở hộp thoại đăng bài")
        
        if "x" in result:
            import pyautogui
            pyautogui.click(result['x'], result['y'])
            time.sleep(2)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(1)
            
            # Tìm nút đăng
            result = self.vision_agent.ask_ai_where_to_click("Tìm và click vào nút 'Đăng' để đăng bài")
            if "x" in result:
                pyautogui.click(result['x'], result['y'])
                print("🎉 ĐĂNG BÀI THÀNH CÔNG VỚI AI VISION AGENT!")
                return True
        
        print("❌ Cả hai Agent đều không thể đăng bài")
        return False

if __name__ == "__main__":
    agent = HybridFacebookAgent()
    content = """Xin chào bạn, hôm nay chúng ta sẽ cùng nhau đi qua một hành trình nhỏ mang tên "Buông bỏ". 

thí nghiệm 7 - Hybrid Agent

Thành công!"""
    
    agent.post_to_facebook(content)
