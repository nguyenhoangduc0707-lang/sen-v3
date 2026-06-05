"""
TikTok Real Poster - Theo tài liệu chính thức
Hỗ trợ đăng ảnh (PHOTO) lên TikTok
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()

class TikTokRealPoster:
    def __init__(self):
        self.access_token = os.getenv("TIKTOK_ACCESS_TOKEN")
        self.client_key = os.getenv("TIKTOK_CLIENT_KEY")
        self.client_secret = os.getenv("TIKTOK_CLIENT_SECRET")
    
    def post_photo(self, image_urls, title="", description="", privacy_level="PUBLIC_TO_EVERYONE"):
        """
        Đăng ảnh lên TikTok
        - image_urls: list các URL ảnh (tối đa 35 ảnh)
        - title: tiêu đề (tối đa 90 ký tự UTF-16)
        - description: mô tả (tối đa 4000 ký tự)
        - privacy_level: PUBLIC_TO_EVERYONE, SELF_ONLY,...
        """
        if not self.access_token:
            print("❌ Chưa có Access Token!")
            return False
        
        url = "https://open.tiktokapis.com/v2/post/publish/content/init/"
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        # Chuẩn bị data theo tài liệu
        data = {
            "post_info": {
                "title": title[:90],  # Giới hạn 90 ký tự
                "description": description[:4000],  # Giới hạn 4000 ký tự
                "privacy_level": privacy_level,
                "disable_comment": False,
                "auto_add_music": True
            },
            "source_info": {
                "source": "PULL_FROM_URL",
                "photo_cover_index": 0,  # Ảnh đầu tiên làm bìa
                "photo_images": image_urls[:35]  # Tối đa 35 ảnh
            },
            "post_mode": "DIRECT_POST",  # Đăng trực tiếp
            "media_type": "PHOTO"
        }
        
        print(f"📸 Đang đăng {len(image_urls)} ảnh lên TikTok...")
        print(f"📝 Title: {title[:50]}...")
        
        try:
            response = requests.post(url, headers=headers, json=data)
            result = response.json()
            
            if result.get("error", {}).get("code") == "ok":
                publish_id = result.get("data", {}).get("publish_id")
                print(f"✅ Đã đăng ảnh thành công!")
                print(f"   Publish ID: {publish_id}")
                return True
            else:
                error = result.get("error", {})
                print(f"❌ Lỗi: {error.get('code')} - {error.get('message')}")
                return False
                
        except Exception as e:
            print(f"❌ Exception: {e}")
            return False
    
    def post_shopee_photo(self):
        """Đăng ảnh quảng bá Shopee"""
        # Cần có URL ảnh công khai
        # Ví dụ upload ảnh lên Imgur hoặc hosting
        image_urls = [
            "https://example.com/shopee_sale_1.jpg",
            "https://example.com/shopee_sale_2.jpg"
        ]
        
        description = """🔥 SHOPEE SALE GIỮA THÁNG - GIẢM ĐẾN 70%

✅ Voucher Xtra giảm đến 5 triệu đồng
✅ Freeship 0Đ cho đơn hàng

👉 Mua sắm ngay: https://go.isclix.com/deep_link/v6/6983938396644077046/4751584435713464237?sub4=tiktok

#ShopeeSale #GiamGia #MuaSam
"""
        return self.post_photo(image_urls, "Shopee Sale Giữa Tháng", description)

if __name__ == "__main__":
    poster = TikTokRealPoster()
    
    # Kiểm tra token
    if poster.access_token:
        print(f"✅ Access Token: {poster.access_token[:30]}...")
        print("🚀 Sẵn sàng đăng ảnh lên TikTok!")
        
        # Cần có URL ảnh thật
        # poster.post_shopee_photo()
    else:
        print("❌ Chưa có Access Token!")
        print("👉 Cần lấy token qua OAuth trước")
