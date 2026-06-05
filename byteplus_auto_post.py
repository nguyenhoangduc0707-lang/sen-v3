"""
BytePlus SDK - Auto Post to TikTok/BytePlus
"""
from byteplus import client
from byteplus.models import *
import os
from dotenv import load_dotenv

load_dotenv()

class BytePlusAutoPost:
    def __init__(self):
        # Cấu hình từ .env
        self.app_id = os.getenv("BYTEPLUS_APP_ID")
        self.app_secret = os.getenv("BYTEPLUS_APP_SECRET")
        self.access_token = os.getenv("BYTEPLUS_ACCESS_TOKEN")
        
        # Khởi tạo client
        self.client = client.Client(
            app_id=self.app_id,
            app_secret=self.app_secret,
            access_token=self.access_token
        )
    
    def post_video(self, video_path, title, hashtags=[]):
        """Đăng video lên TikTok/BytePlus"""
        try:
            # Upload video
            video_url = self.client.upload_video(video_path)
            
            # Tạo nội dung bài đăng
            content = title
            if hashtags:
                content += " " + " ".join([f"#{tag}" for tag in hashtags])
            
            # Đăng video
            result = self.client.create_post(
                video_url=video_url,
                content=content
            )
            
            print(f"✅ Đã đăng video: {title}")
            return result
        except Exception as e:
            print(f"❌ Lỗi: {e}")
            return None
    
    def post_image(self, image_path, caption):
        """Đăng ảnh lên TikTok/BytePlus"""
        try:
            result = self.client.create_image_post(
                image_path=image_path,
                caption=caption
            )
            print(f"✅ Đã đăng ảnh: {caption[:50]}...")
            return result
        except Exception as e:
            print(f"❌ Lỗi: {e}")
            return None

# Thông tin cấu hình cần thêm vào .env
print("=" * 50)
print("📋 CẤU HÌNH CẦN THÊM VÀO .ENV")
print("=" * 50)
print("""
BYTEPLUS_APP_ID=your_app_id
BYTEPLUS_APP_SECRET=your_app_secret
BYTEPLUS_ACCESS_TOKEN=your_access_token
""")

# Link Shopee để quảng bá
SHOPEE_LINK = "https://go.isclix.com/deep_link/v6/6983938396644077046/4751584435713464237?sub4=sen_v3"

# Tạo nội dung cho TikTok
tiktok_content = f"""🛍️ SHOPEE SALE GIỮA THÁNG - GIẢM ĐẾN 70%

🔥 Voucher Xtra giảm đến 5 triệu đồng
🔥 Freeship 0Đ cho đơn hàng

👉 Mua sắm ngay: {SHOPEE_LINK}

#ShopeeSale #GiamGia #SaleOff
"""

print("\n📢 NỘI DUNG MẪU CHO TIKTOK:")
print("-" * 40)
print(tiktok_content)
print("-" * 40)
