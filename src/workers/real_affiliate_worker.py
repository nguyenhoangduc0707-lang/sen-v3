"""
REAL AFFILIATE WORKER - Chỉ chạy khi có key thật
"""
import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class RealAffiliateWorker:
    def __init__(self):
        self.api_keys = {
            "accesstrade": os.getenv("ACCESSTRADE_API_KEY", ""),
            "tiki": os.getenv("TIKI_API_KEY", ""),
            "shopee": os.getenv("SHOPEE_API_KEY", ""),
            "lazada": os.getenv("LAZADA_API_KEY", "")
        }
        
        # Chỉ lấy key thật (không phải placeholder)
        self.real_keys = {}
        for platform, key in self.api_keys.items():
            if key and key not in ["your_accesstrade_key_here", "your_tiki_key_here", "", "your_xxx_key_here"]:
                self.real_keys[platform] = key
        
    def run(self):
        print("=" * 60)
        print("💰 REAL AFFILIATE WORKER")
        print("=" * 60)
        
        if not self.real_keys:
            print("❌ Không có key thật nào! Hãy cập nhật .env")
            print("\n📝 Các key cần có:")
            print("   - ACCESSTRADE_API_KEY")
            print("   - TIKI_API_KEY")
            print("   - SHOPEE_API_KEY")
            print("   - LAZADA_API_KEY")
            return {"status": "no_keys"}
        
        print(f"\n✅ Phát hiện {len(self.real_keys)} key thật:")
        for platform in self.real_keys.keys():
            print(f"   - {platform}")
        
        print("\n🚀 Đã sẵn sàng chạy worker với key thật!")
        print("📝 TODO: Gọi API thật từ các nền tảng")
        
        return {"status": "ready", "platforms": list(self.real_keys.keys())}

if __name__ == "__main__":
    worker = RealAffiliateWorker()
    result = worker.run()
