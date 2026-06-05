"""
AFFILIATE WORKER - TẬP TRUNG KIẾM TIỀN
Hỗ trợ: Accesstrade, Shopee, Tiki, Lazada, ACFC
"""

import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class AffiliateWorker:
    def __init__(self):
        # Lấy key từ .env
        self.accesstrade_key = os.getenv("ACCESSTRADE_API_KEY", "")
        self.shopee_link = os.getenv("SHOPEE_API_KEY", "")
        self.tiki_link = os.getenv("TIKI_API_KEY", "")
        self.lazada_link = os.getenv("LAZADA_API_KEY", "")
        
        # Kiểm tra chế độ
        self.is_demo = self.accesstrade_key in ["", "your_accesstrade_key_here"]
        
    def check_keys(self):
        """Kiểm tra key thật"""
        print("\n📊 KIỂM TRA API KEY:")
        print("=" * 40)
        
        keys = [
            ("Accesstrade", self.accesstrade_key, "https://accesstrade.vn"),
            ("Shopee", self.shopee_link, "https://affiliate.shopee.vn"),
            ("Tiki", self.tiki_link, "https://tiki.vn/affiliate"),
            ("Lazada", self.lazada_link, "https://lazada.vn/affiliate")
        ]
        
        real_keys = []
        for name, key, link in keys:
            if key and key not in ["", "your_accesstrade_key_here", "your_shopee_key_here"]:
                print(f"   ✅ {name}: CÓ KEY THẬT")
                real_keys.append(name)
            else:
                print(f"   ❌ {name}: Chưa có key (đăng ký tại {link})")
        
        return real_keys
    
    def fetch_accesstrade_campaigns(self):
        """Lấy danh sách chiến dịch từ Accesstrade"""
        if self.is_demo:
            return self._get_demo_campaigns()
        
        try:
            headers = {"Authorization": f"Bearer {self.accesstrade_key}"}
            response = requests.get(
                "https://api.accesstrade.vn/v1/campaigns",
                headers=headers,
                timeout=30
            )
            if response.status_code == 200:
                return response.json()
            else:
                print(f"   ⚠️ Lỗi API: {response.status_code}")
                return self._get_demo_campaigns()
        except Exception as e:
            print(f"   ⚠️ Lỗi kết nối: {e}")
            return self._get_demo_campaigns()
    
    def _get_demo_campaigns(self):
        """Dữ liệu mẫu (DEMO)"""
        return [
            {"id": "CAMP_001", "name": "ACFC Double 5 Sale", "commission": "50%", "link": "https://www.acfc.com.vn/promotion/double-day.html"},
            {"id": "CAMP_002", "name": "Calvin Klein - Giảm 50%", "commission": "50%", "link": "https://www.acfc.com.vn/promotion/double-day.html?brand_id=47"},
            {"id": "CAMP_003", "name": "Tommy Hilfiger - Giảm 50%", "commission": "50%", "link": "https://www.acfc.com.vn/promotion/double-day.html?brand_id=14"},
            {"id": "CAMP_004", "name": "Mango - Giảm 50%", "commission": "50%", "link": "https://www.acfc.com.vn/promotion/double-day.html?brand_id=5"},
            {"id": "CAMP_005", "name": "Guess - Giảm 50%", "commission": "50%", "link": "https://www.acfc.com.vn/promotion/double-day.html?brand_id=69"},
            {"id": "CAMP_006", "name": "Cotton On Special Offer", "commission": "50%++", "link": "https://www.acfc.com.vn/promotion/cotton-on-special-offer.html"}
        ]
    
    def generate_links(self, campaigns):
        """Tạo link affiliate từ danh sách chiến dịch"""
        links = []
        affiliate_id = "YOUR_AFFILIATE_ID" if self.is_demo else self.accesstrade_key[:10]
        
        for camp in campaigns:
            base_link = camp.get("link", "")
            if "?" in base_link:
                affiliate_link = f"{base_link}&affiliate={affiliate_id}"
            else:
                affiliate_link = f"{base_link}?affiliate={affiliate_id}"
            
            links.append({
                "name": camp.get("name"),
                "link": affiliate_link,
                "commission": camp.get("commission"),
                "status": "demo" if self.is_demo else "real"
            })
        
        return links
    
    def save_links(self, links):
        """Lưu link ra file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"affiliate_links_{timestamp}.txt"
        filepath = f"E:/DYT_01/{filename}"
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("=" * 60 + "\n")
            f.write("💰 AFFILIATE LINKS - DYT_01 PROJECT\n")
            f.write(f"📅 Ngày tạo: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"🔑 Chế độ: {'DEMO' if self.is_demo else 'THẬT'}\n")
            f.write("=" * 60 + "\n\n")
            
            for link in links:
                f.write(f"📌 {link['name']}\n")
                f.write(f"   🔗 Link: {link['link']}\n")
                f.write(f"   💰 Hoa hồng: {link['commission']}\n")
                f.write(f"   📊 Trạng thái: {link['status']}\n\n")
        
        return filepath
    
    def run(self):
        """Chạy worker"""
        print("=" * 60)
        print("💰 AFFILIATE WORKER - KIẾM TIỀN TỪ AFFILIATE")
        print("=" * 60)
        print(f"⏰ Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # 1. Kiểm tra key
        real_keys = self.check_keys()
        
        # 2. Lấy chiến dịch
        print("\n📊 LẤY DANH SÁCH CHIẾN DỊCH:")
        campaigns = self.fetch_accesstrade_campaigns()
        print(f"   ✅ Tìm thấy {len(campaigns)} chiến dịch")
        
        # 3. Tạo link affiliate
        print("\n🔗 TẠO LINK AFFILIATE:")
        links = self.generate_links(campaigns)
        for link in links[:5]:
            print(f"   ✅ {link['name']}: {link['link'][:80]}...")
        
        # 4. Lưu link
        filepath = self.save_links(links)
        
        # 5. Tổng kết
        print("\n" + "=" * 60)
        print("📊 TỔNG KẾT:")
        print(f"   ✅ Tổng số link: {len(links)}")
        print(f"   🔑 Chế độ: {'DEMO (chưa có key thật)' if self.is_demo else 'THẬT (đã có key)'}")
        print(f"   💾 Link đã lưu: {filepath}")
        print("=" * 60)
        
        if self.is_demo:
            print("\n⚠️ BẠN ĐANG Ở CHẾ ĐỘ DEMO!")
            print("👉 Để kiếm tiền thật, hãy:")
            print("   1. Đăng ký Accesstrade tại https://accesstrade.vn/register")
            print("   2. Lấy API key và cập nhật vào file .env")
            print("   3. Chạy lại worker này")
        else:
            print("\n🎉 CHÚC MỪNG! BẠN ĐÃ SẴN SÀNG KIẾM TIỀN!")
            print("👉 Dùng link trong file để đăng bài kiếm hoa hồng!")

if __name__ == "__main__":
    worker = AffiliateWorker()
    worker.run()
