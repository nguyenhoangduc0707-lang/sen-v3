"""
Auto Post Facebook - Tự động đăng bài lên Facebook
Cần có Facebook Access Token
"""
import requests
import json
import time
import random
from datetime import datetime

class FacebookAutoPost:
    def __init__(self):
        # Hướng dẫn lấy token: https://developers.facebook.com/tools/explorer/
        self.access_token = None  # Điền token của bạn vào đây
        self.page_id = None  # Điền Page ID nếu đăng lên Page
        self.group_id = None  # Điền Group ID nếu đăng lên Group
    
    def set_token(self, token):
        self.access_token = token
        print(f"✅ Đã set Facebook Token")
    
    def post_to_timeline(self, message, link=None):
        """Đăng lên timeline cá nhân"""
        if not self.access_token:
            print("❌ Chưa có access_token!")
            return False
        
        url = "https://graph.facebook.com/v18.0/me/feed"
        data = {
            "message": message,
            "access_token": self.access_token
        }
        if link:
            data["link"] = link
        
        try:
            response = requests.post(url, data=data)
            if response.status_code == 200:
                print(f"✅ Đã đăng lên timeline: {message[:50]}...")
                return True
            else:
                print(f"❌ Lỗi: {response.json()}")
                return False
        except Exception as e:
            print(f"❌ Lỗi: {e}")
            return False

class AutoPostScheduler:
    def __init__(self):
        self.facebook = FacebookAutoPost()
        self.posts = []
    
    def load_posts(self):
        """Load bài đăng từ file"""
        with open('bulk_posts.json', 'r', encoding='utf-8') as f:
            self.posts = json.load(f)
        print(f"📋 Đã tải {len(self.posts)} bài đăng")
        return self.posts
    
    def auto_post_all(self, delay_minutes=10):
        """Tự động đăng tất cả bài"""
        if not self.facebook.access_token:
            print("❌ Cần set Facebook Token trước!")
            print("💡 Lấy token tại: https://developers.facebook.com/tools/explorer/")
            return
        
        print("=" * 60)
        print("🚀 BẮT ĐẦU AUTO POST")
        print(f"📊 Tổng số bài: {len(self.posts)}")
        print(f"⏰ Delay: {delay_minutes} phút/bài")
        print("=" * 60)
        
        for i, post in enumerate(self.posts, 1):
            print(f"\n📝 Đang đăng bài {i}/{len(self.posts)}: {post['name']}")
            
            # Đăng lên Facebook
            success = self.facebook.post_to_timeline(
                message=post['content'],
                link=post['link']
            )
            
            if success:
                print(f"   ✅ Đã đăng bài {i}")
            else:
                print(f"   ❌ Đăng thất bại")
            
            # Chờ giữa các bài
            if i < len(self.posts):
                print(f"   ⏰ Chờ {delay_minutes} phút đến bài tiếp theo...")
                time.sleep(delay_minutes * 60)
        
        print("\n" + "=" * 60)
        print("✅ AUTO POST HOÀN TẤT!")
        print("=" * 60)

# Hướng dẫn lấy token
print("=" * 70)
print("🔐 HƯỚNG DẪN LẤY FACEBOOK ACCESS TOKEN:")
print("=" * 70)
print("""
1. Truy cập: https://developers.facebook.com/tools/explorer/
2. Chọn App > Nhấn 'Get Access Token'
3. Chọn quyền: 'publish_to_groups', 'pages_manage_posts'
4. Copy token và chạy lệnh:
   python -c "from auto_post_facebook import FacebookAutoPost; f=FacebookAutoPost(); f.set_token('YOUR_TOKEN'); f.post_to_timeline('Test bài đăng')"
""")
print("=" * 70)

if __name__ == "__main__":
    scheduler = AutoPostScheduler()
    scheduler.load_posts()
    
    # Nếu có token, bỏ comment dòng dưới và điền token
    # scheduler.facebook.set_token("YOUR_ACCESS_TOKEN_HERE")
    # scheduler.auto_post_all(delay_minutes=5)
