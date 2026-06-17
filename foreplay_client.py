import requests
import json
import os
from datetime import datetime, timedelta

class ForeplayClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://public.api.foreplay.co"
        self.headers = {"Authorization": api_key}
    
    def get_top_ads(self, niche=None, days=7, limit=10):
        """Lấy quảng cáo hot nhất trong niche"""
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
        
        response = requests.get(
            f"{self.base_url}/api/discovery/ads",
            headers=self.headers,
            params=params
        )
        
        return response.json()
    
    def get_brand_ads(self, brand_name, limit=10):
        """Lấy quảng cáo của một thương hiệu"""
        params = {'limit': limit}
        
        response = requests.get(
            f"{self.base_url}/api/discovery/brands",
            headers=self.headers,
            params=params
        )
        
        # Tìm brand
        brands = response.json().get('data', [])
        for brand in brands:
            if brand_name.lower() in brand.get('name', '').lower():
                # Lấy ads của brand này
                brand_ads = requests.get(
                    f"{self.base_url}/api/spyder/brand/ads",
                    headers=self.headers,
                    params={'brand_id': brand['id'], 'limit': limit}
                )
                return brand_ads.json()
        
        return None

# Sử dụng
def main():
    api_key = os.getenv('FOREPLAY_API_KEY')
    if not api_key:
        print("❌ Chưa set FOREPLAY_API_KEY trong .env")
        return
    
    client = ForeplayClient(api_key)
    
    # Lấy quảng cáo hot trong niche fashion
    print("🔥 Quảng cáo hot trong niche fashion:")
    data = client.get_top_ads(niche='fashion', limit=5)
    
    if data.get('data'):
        for ad in data['data']:
            print(f"\n📋 {ad.get('name', 'No name')}")
            print(f"   Brand: {ad.get('brand', {}).get('name', 'Unknown')}")
            print(f"   Description: {ad.get('description', '')[:100]}...")
            print(f"   Link: {ad.get('foreplay_url', '#')}")
            print("-" * 40)
    
    # Lưu vào database để phân tích
    with open('top_ads.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("\n✅ Đã lưu vào top_ads.json")

if __name__ == "__main__":
    main()
