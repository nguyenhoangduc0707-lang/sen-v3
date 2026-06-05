"""
TikTok Real Poster - Đăng video thật
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()

class TikTokReal:
    def __init__(self):
        self.client_key = os.getenv("TIKTOK_CLIENT_KEY")
        self.client_secret = os.getenv("TIKTOK_CLIENT_SECRET")
        self.access_token = None
    
    def get_access_token(self):
        """Lấy access token thật"""
        url = "https://open-api.tiktok.com/oauth/access_token/"
        data = {
            "client_key": self.client_key,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials"
        }
        response = requests.post(url, data=data)
        if response.status_code == 200:
            self.access_token = response.json().get('access_token')
            print(f"✅ Access token: {self.access_token[:20]}...")
            return True
        return False
    
    def upload_video(self, video_path, description):
        """Upload video thật lên TikTok"""
        if not self.access_token:
            if not self.get_access_token():
                print("❌ Không thể lấy access token")
                return
        
        url = "https://open-api.tiktok.com/share/video/upload/"
        headers = {"access-token": self.access_token}
        
        with open(video_path, 'rb') as f:
            files = {'video': f}
            data = {'description': description}
            
            response = requests.post(url, headers=headers, data=data, files=files)
            
            if response.status_code == 200:
                print(f"✅ Video đã được đăng!")
                return response.json()
            else:
                print(f"❌ Lỗi: {response.json()}")
                return None

if __name__ == "__main__":
    tiktok = TikTokReal()
    # tiktok.upload_video("video.mp4", "🔥 Shopee Sale Giữa Tháng!")
