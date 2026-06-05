import os
import time
import base64
import json
import pyautogui
from io import BytesIO
from PIL import Image
from google import genai
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class ComputerUseAgent:
    """AI Agent có khả năng nhìn và thao tác trên web bằng Gemini"""
    
    def __init__(self):
        # Khởi tạo Gemini Client
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
        self.driver = None
    
    def ask_ai_where_to_click(self, prompt_text):
        """Sử dụng Gemini nhìn màn hình và trả về tọa độ"""
        print(f"🤖 AI đang phân tích: {prompt_text}...")
        screenshot = pyautogui.screenshot()
        
        # Gửi ảnh và yêu cầu tọa độ
        response = self.client.models.generate_content(
            model='gemini-2.0-flash',
            contents=[
                f"Bạn là trợ lý điều khiển máy tính. {prompt_text}. Hãy trả về tọa độ (x, y) để click. Trả về đúng 1 dòng JSON duy nhất dạng: {{'x': 123, 'y': 456}}",
                screenshot
            ]
        )
        
        # Làm sạch kết quả trả về để thành JSON
        clean_text = response.text.replace("```json", "").replace("```", "").strip()
        try:
            coords = json.loads(clean_text)
            return coords
        except Exception as e:
            print(f"❌ Lỗi parse tọa độ: {response.text}")
            return {"error": str(e)}
    
    def click_at(self, x, y):
        pyautogui.moveTo(x, y, duration=0.5)
        time.sleep(0.5)
        pyautogui.click()
        return True
    
    def type_text(self, text):
        pyautogui.write(text, interval=0.01)
    
    def post_to_facebook(self, content):
        print("🚀 Bắt đầu quy trình đăng bài...")
        
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.get("https://www.facebook.com/")
        
        # Đăng nhập bằng cookie
        try:
            with open("fb_cookies_selenium.json", "r") as f:
                cookies = json.load(f)
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            self.driver.refresh()
            time.sleep(5)
            print("✅ Đã đăng nhập")
        except Exception as e:
            print(f"❌ Lỗi cookie: {e}")
            return False
        
        # Bước 1: AI tìm ô đăng bài
        print("🔍 AI đang tìm ô 'Bạn đang nghĩ gì?'...")
        result = self.ask_ai_where_to_click("Tìm và click vào ô 'Bạn đang nghĩ gì?' trên Facebook")
        
        if "error" in result:
            print(f"❌ AI không tìm thấy: {result['error']}")
            return False
        
        self.click_at(result['x'], result['y'])
        time.sleep(2)
        
        # Bước 2: Dán nội dung
        print("📝 Đang dán nội dung...")
        self.type_text(content)
        time.sleep(2)
        
        # Bước 3: AI tìm nút Đăng
        print("🔍 AI đang tìm nút 'Đăng'...")
        result = self.ask_ai_where_to_click("Tìm và click vào nút 'Đăng' hoặc 'Post' trên Facebook")
        
        if "error" not in result:
            self.click_at(result['x'], result['y'])
        else:
            pyautogui.hotkey('ctrl', 'enter')
            print("⚠️ Đã dùng Ctrl+Enter để đăng")
        
        print("✅ Quy trình hoàn tất!")
        return True

def main():
    agent = ComputerUseAgent()
    content = "Xin chào, đây là bài viết được đăng bởi AI Computer Use Agent. Thành công!"
    agent.post_to_facebook(content)

if __name__ == "__main__":
    main()