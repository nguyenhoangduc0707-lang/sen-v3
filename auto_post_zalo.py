"""
Auto Post Zalo - Tự động mở Zalo Web và copy bài đăng
"""
import webbrowser
import time
import pyautogui
import json
from datetime import datetime

class ZaloAutoPost:
    def __init__(self):
        self.posts = []
    
    def load_posts(self):
        with open('bulk_posts.json', 'r', encoding='utf-8') as f:
            self.posts = json.load(f)
        return self.posts
    
    def open_zalo(self):
        """Mở Zalo Web"""
        webbrowser.open("https://chat.zalo.me")
        print("✅ Đã mở Zalo Web")
        time.sleep(3)
    
    def auto_post_with_guide(self):
        """Hướng dẫn đăng bài từng bước"""
        print("=" * 60)
        print("🚀 AUTO POST ZALO - CHẾ ĐỘ HƯỚNG DẪN")
        print("=" * 60)
        
        self.open_zalo()
        
        for i, post in enumerate(self.posts[:10], 1):  # 10 bài đầu
            print(f"\n📝 BÀI {i}: {post['name']}")
            print("-" * 40)
            print(post['content'])
            print(f"\n🔗 Link: {post['link']}")
            print("-" * 40)
            print("\n👉 Đã copy nội dung vào clipboard!")
            
            # Copy vào clipboard
            import pyperclip
            full_text = f"{post['content']}\n\n{post['link']}"
            pyperclip.copy(full_text)
            
            input("✅ Sau khi dán xong, nhấn Enter để sang bài tiếp theo...")
        
        print("\n✅ Đã hoàn thành 10 bài đăng Zalo!")

# Cài đặt thư viện cần thiết
try:
    import pyperclip
except:
    print("📦 Đang cài đặt pyperclip...")
    import subprocess
    subprocess.run(["pip", "install", "pyperclip"])

if __name__ == "__main__":
    zalo = ZaloAutoPost()
    zalo.load_posts()
    zalo.auto_post_with_guide()
