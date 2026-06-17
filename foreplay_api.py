import requests
import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

class ForeplayAPI:
    def __init__(self):
        self.api_key = os.getenv('FOREPLAY_API_KEY')
        if not self.api_key:
            raise ValueError("❌ Chưa có FOREPLAY_API_KEY trong .env")
        
        self.base_url = "https://public.api.foreplay.co"
        self.headers = {"Authorization": self.api_key}
        self.credit_remaining = None
    
    def get_top_ads(self, niche=None, days=7, limit=10):
        """
        Lấy quảng cáo hot nhất trong niche
        """
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d 00:00:00')
        end_date = datetime.now().strftime('%Y-%m-%d 23:59:59')
        
        params = {
            'start_date': start_date,
            'end_date': end_date,
            'live': 'true',
            'limit': limit,
            'order': 'most_relevant'
        }
        
        if niche:
            params['niches'] = niche
        
        # Dùng endpoint discovery/ads để tìm quảng cáo hot
        response = requests.get(
            f"{self.base_url}/api/discovery/ads",
            headers=self.headers,
            params=params
        )
        
        # Lưu credit còn lại
        self.credit_remaining = response.headers.get('X-Credits-Remaining')
        
        return response.json()
    
    def get_brand_ads(self, brand_name, limit=10):
        """
        Tìm thương hiệu và lấy quảng cáo của họ
        """
        # Tìm brand
        response = requests.get(
            f"{self.base_url}/api/discovery/brands",
            headers=self.headers,
            params={'limit': 20, 'offset': 0}
        )
        
        data = response.json()
        brands = data.get('data', [])
        
        # Tìm brand khớp tên
        target_brand = None
        for brand in brands:
            if brand_name.lower() in brand.get('name', '').lower():
                target_brand = brand
                break
        
        if not target_brand:
            return {'error': f'Không tìm thấy brand: {brand_name}'}
        
        # Lấy ads của brand
        brand_id = target_brand['id']
        response = requests.get(
            f"{self.base_url}/api/spyder/brand/ads",
            headers=self.headers,
            params={'brand_id': brand_id, 'limit': limit}
        )
        
        return response.json()
    
    def get_swipefile_ads(self, limit=10):
        """
        Lấy quảng cáo đã lưu trong SwipeFile
        """
        response = requests.get(
            f"{self.base_url}/api/swipefile/ads",
            headers=self.headers,
            params={'limit': limit, 'order': 'saved_newest'}
        )
        return response.json()

def main():
    try:
        api = ForeplayAPI()
        
        print("🔍 FOREPLAY API - LẤY DỮ LIỆU QUẢNG CÁO")
        print("="*60)
        
        # 1. Lấy quảng cáo hot trong niche fashion
        print("\n1️⃣ QUẢNG CÁO HOT TRONG NICHE FASHION:")
        data = api.get_top_ads(niche='fashion', limit=5)
        
        if data.get('data'):
            for i, ad in enumerate(data['data'], 1):
                print(f"\n📋 Ad {i}: {ad.get('name', 'No name')}")
                print(f"   Brand: {ad.get('brand', {}).get('name', 'Unknown')}")
                print(f"   Headline: {ad.get('headline', '')[:100]}...")
                print(f"   Foreplay URL: {ad.get('foreplay_url', '#')}")
        else:
            print("   Không có dữ liệu")
        
        # 2. Lấy quảng cáo của một thương hiệu cụ thể
        print("\n2️⃣ QUẢNG CÁO CỦA THƯƠNG HIỆU 'Nike':")
        brand_data = api.get_brand_ads('Nike', limit=3)
        
        if 'error' not in brand_data and brand_data.get('data'):
            for ad in brand_data['data'][:3]:
                print(f"\n   📋 {ad.get('name', 'No name')}")
                print(f"      {ad.get('headline', '')[:80]}...")
        else:
            print(f"   {brand_data.get('error', 'Không có dữ liệu')}")
        
        # 3. Lấy SwipeFile
        print("\n3️⃣ QUẢNG CÁO ĐÃ LƯU TRONG SWIPEFILE:")
        swipe = api.get_swipefile_ads(limit=3)
        
        if swipe.get('data'):
            for ad in swipe['data'][:3]:
                print(f"\n   📋 {ad.get('name', 'No name')}")
                print(f"      {ad.get('headline', '')[:80]}...")
        
        # 4. Hiển thị credit
        if api.credit_remaining:
            print(f"\n💳 Credits còn lại: {api.credit_remaining}")
        
        # Lưu dữ liệu ra file
        with open('foreplay_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("\n✅ Đã lưu dữ liệu vào foreplay_data.json")
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")

if __name__ == "__main__":
    main()
