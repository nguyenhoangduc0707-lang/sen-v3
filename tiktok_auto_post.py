"""
TikTok Auto Post - Tự động đăng video quảng bá link affiliate
"""
import os
import time
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class TikTokAutoPost:
    def __init__(self):
        self.app_id = os.getenv("BYTEPLUS_APP_ID")
        self.app_secret = os.getenv("BYTEPLUS_APP_SECRET")
        self.access_token = os.getenv("BYTEPLUS_ACCESS_TOKEN")
        self.business_id = os.getenv("TIKTOK_BUSINESS_ID")
        
        # Link Shopee affiliate
        self.shopee_link = "https://go.isclix.com/deep_link/v6/6983938396644077046/4751584435713464237?sub4=tiktok"
    
    def generate_video_script(self, campaign_name):
        """Tạo kịch bản video từ campaign"""
        scripts = {
            "shopee": f"""🔥 SHOPEE SALE GIỮA THÁNG!
🎁 Giảm đến 70% + Freeship
💰 Voucher Xtra 5 triệu đồng
👉 Mua ngay: {self.shopee_link}
#ShopeeSale #GiamGia #MuaSam""",
            
            "vpbank": f"""💰 VPBank - VAY TÍN CHẤP 500 TRIỆU
✅ Lãi suất từ 0.8%/tháng
✅ Giải ngân 24h
👉 Đăng ký: {self.shopee_link}
#VayVon #VPBank #TaiChinh""",
            
            "hdbank": f"""💳 HDBank - THẺ TÍN DỤNG HOÀN TIỀN 5%
✅ Mở thẻ online 100%
✅ Nhận thẻ sau 3 ngày
👉 Đăng ký: {self.shopee_link}
#TheTinDung #HDBank #HoanTien"""
        }
        return scripts.get(campaign_name, scripts["shopee"])
    
    def post_video(self, video_path, caption, hashtags=None):
        """Đăng video lên TikTok"""
        try:
            # Giả lập API call (thay bằng real API khi có credentials)
            print(f"📹 Đang đăng video lên TikTok...")
            print(f"   Caption: {caption[:100]}...")
            print(f"   Hashtags: {hashtags}")
            
            # TODO: Thay bằng API thật
            # result = self.client.upload_video(video_path, caption)
            
            print(f"✅ Đã đăng video thành công!")
            return {"success": True, "post_id": "mock_123"}
        except Exception as e:
            print(f"❌ Lỗi: {e}")
            return {"success": False}
    
    def auto_post_all(self):
        """Tự động đăng tất cả video"""
        campaigns = ["shopee", "vpbank", "hdbank"]
        
        print("=" * 50)
        print("🚀 AUTO POST TIKTOK")
        print("=" * 50)
        
        for i, campaign in enumerate(campaigns, 1):
            script = self.generate_video_script(campaign)
            print(f"\n📝 Bài {i}: {campaign.upper()}")
            print(f"   Script: {script[:80]}...")
            
            # Giả lập đăng video (cần video thật hoặc tạo video từ script)
            result = self.post_video(f"videos/{campaign}.mp4", script, ["Sale", "Affiliate"])
            
            if i < len(campaigns):
                print("   ⏰ Chờ 30 phút đến bài tiếp theo...")
                time.sleep(1800)  # 30 phút
        
        print("\n✅ Đã đăng xong tất cả video!")

if __name__ == "__main__":
    bot = TikTokAutoPost()
    bot.auto_post_all()
