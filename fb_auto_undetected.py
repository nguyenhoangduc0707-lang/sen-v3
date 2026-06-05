import undetected_chromedriver as uc
import time
import json
import os

class FacebookAutoPoster:
    def __init__(self):
        self.driver = None
        self.cookie_file = "facebook_cookies.json"
    
    def start(self):
        """Khởi động trình duyệt"""
        print("🚀 Đang khởi động trình duyệt...")
        options = uc.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-infobars')
        options.add_argument('--lang=vi-VN')
        
        self.driver = uc.Chrome(options=options, version_main=None)
        return self.driver
    
    def login_with_cookie(self):
        """Đăng nhập bằng cookie đã lưu"""
        if os.path.exists(self.cookie_file):
            print("🍪 Đang load cookies...")
            self.driver.get("https://www.facebook.com/")
            time.sleep(2)
            
            with open(self.cookie_file, "r") as f:
                cookies = json.load(f)
            
            for cookie in cookies:
                try:
                    self.driver.add_cookie(cookie)
                except:
                    pass
            
            self.driver.refresh()
            time.sleep(3)
            
            # Kiểm tra đăng nhập
            if "login" not in self.driver.current_url:
                print("✅ Đã đăng nhập bằng cookie!")
                return True
        
        return self.login_manual()
    
    def login_manual(self):
        """Đăng nhập thủ công lần đầu"""
        print("📧 Vui lòng đăng nhập THỦ CÔNG...")
        print("👉 Sau khi đăng nhập xong, nhấn Enter")
        
        self.driver.get("https://www.facebook.com/")
        input()
        
        # Lưu cookie
        cookies = self.driver.get_cookies()
        with open(self.cookie_file, "w") as f:
            json.dump(cookies, f)
        print("✅ Đã lưu cookies!")
        return True
    
    def post(self, message):
        """Đăng bài lên Facebook"""
        print(f"\n📝 Đang đăng bài: {message[:50]}...")
        
        # Tìm ô tạo bài viết
        try:
            # Cách 1: Tìm bằng text
            post_box = self.driver.find_element("xpath", "//div[contains(@aria-label, 'Tạo bài viết') or contains(@aria-label, 'Create a post')]")
            post_box.click()
            time.sleep(2)
            
            # Tìm khung nhập
            editor = self.driver.find_element("xpath", "//div[@role='textbox' and @aria-label]")
            editor.click()
            editor.send_keys(message)
            time.sleep(2)
            
            # Tìm nút đăng
            post_btn = self.driver.find_element("xpath", "//div[@aria-label='Đăng' or @aria-label='Post']")
            post_btn.click()
            time.sleep(3)
            
            print("✅ Đăng bài thành công!")
            return True
            
        except Exception as e:
            print(f"❌ Lỗi: {e}")
            print("📝 Hãy đăng bài THỦ CÔNG trong trình duyệt")
            input("👉 Sau khi đăng xong, nhấn Enter...")
            return False
    
    def close(self):
        if self.driver:
            self.driver.quit()

def main():
    print("=" * 50)
    print("🤖 FACEBOOK AUTO POSTER - UNDETECTED MODE")
    print("=" * 50)
    
    bot = FacebookAutoPoster()
    driver = bot.start()
    
    if bot.login_with_cookie():
        print("\n✅ Sẵn sàng đăng bài!")
        
        # Nhập nội dung
        print("\n📝 Nhập nội dung (Enter 2 lần để kết thúc):")
        lines = []
        while True:
            line = input()
            if line == "":
                break
            lines.append(line)
        
        message = "\n".join(lines)
        if message:
            bot.post(message)
        else:
            print("⚠️ Không có nội dung, bỏ qua")
    
    input("\nNhấn Enter để đóng...")
    bot.close()

if __name__ == "__main__":
    main()
