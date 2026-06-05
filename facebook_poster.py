"""
Facebook Auto Poster - Chạy riêng, có xử lý lỗi token
"""
import requests
import time
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class FacebookPoster:
    def __init__(self):
        self.page_id = os.getenv("FACEBOOK_PAGE_ID")
        self.access_token = os.getenv("FACEBOOK_ACCESS_TOKEN")
        self.posts_file = "safe_post.txt"
    
    def check_token(self):
        """Kiểm tra token có hợp lệ không"""
        if not self.access_token or 'your_' in self.access_token:
            print("❌ Token chưa được cấu hình!")
            return False
        
        url = f"https://graph.facebook.com/v21.0/{self.page_id}?access_token={self.access_token}"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"✅ Token hợp lệ! Page: {response.json().get('name')}")
                return True
            else:
                print(f"❌ Token không hợp lệ: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Lỗi kết nối: {e}")
            return False
    
    def post_to_facebook(self, message):
        """Đăng bài lên Facebook"""
        url = f"https://graph.facebook.com/v21.0/{self.page_id}/feed"
        data = {
            "message": message,
            "access_token": self.access_token
        }
        
        try:
            response = requests.post(url, data=data, timeout=30)
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Đã đăng bài: {message[:50]}...")
                print(f"   Post ID: {result.get('id')}")
                return True
            else:
                error = response.json()
                print(f"❌ Lỗi {response.status_code}: {error.get('error', {}).get('message', 'Unknown')}")
                return False
        except Exception as e:
            print(f"❌ Lỗi: {e}")
            return False
    
    def load_post_content(self):
        """Tải nội dung bài đăng từ file"""
        try:
            with open(self.posts_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            if content:
                return content
        except:
            pass
        
        # Nội dung mặc định
        return """🔥 ƯU ĐÃI HẤP DẪN TỪ SHOPEE

✅ Giảm giá đến 70%
✅ Freeship toàn quốc
✅ Voucher đến 5 triệu

👉 Xem chi tiết: https://go.isclix.com/deep_link/v6/6983938396644077046/4751584435713464237?sub4=sen_v3

#MuaSam #SaleOff #GiamGia"""
    
    def run_once(self):
        """Chạy đăng bài 1 lần"""
        print("=" * 60)
        print("📘 FACEBOOK AUTO POSTER")
        print("=" * 60)
        
        if not self.check_token():
            print("🔴 Vui lòng cập nhật FACEBOOK_ACCESS_TOKEN trong .env")
            print("   Hướng dẫn: https://developers.facebook.com/tools/explorer/")
            return
        
        content = self.load_post_content()
        print(f"\n📝 Nội dung sẽ đăng:\n{content}\n")
        
        result = self.post_to_facebook(content)
        if result:
            print("\n✅ Đăng bài thành công!")
        else:
            print("\n❌ Đăng bài thất bại. Kiểm tra token và quyền.")
    
    def run_loop(self, interval_minutes=60):
        """Chạy lặp lại mỗi interval phút"""
        print(f"🔄 Sẽ đăng bài mỗi {interval_minutes} phút")
        
        while True:
            self.run_once()
            print(f"\n⏰ Chờ {interval_minutes} phút đến lần đăng tiếp theo...")
            time.sleep(interval_minutes * 60)

if __name__ == "__main__":
    poster = FacebookPoster()
    
    # Chạy 1 lần
    poster.run_once()
    
    # Hoặc chạy lặp lại (bỏ comment dòng dưới)
    # poster.run_loop(interval_minutes=60)
