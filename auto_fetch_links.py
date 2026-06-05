"""
Auto fetch AccessTrade links using API
"""
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ACCESSTRADE_ACCESS_KEY")
HEADERS = {"Authorization": f"Token {API_KEY}"}

def auto_fetch_links():
    print("🔗 Auto fetching AccessTrade links...")
    
    # Lấy campaigns
    response = requests.get(
        "https://api.accesstrade.vn/v1/campaigns",
        headers=HEADERS,
        params={"limit": 50}
    )
    
    if response.status_code == 200:
        campaigns = response.json().get('data', [])
        
        links = []
        for camp in campaigns[:20]:
            link = f"https://go.isclix.com/deep_link/v5/{os.getenv('PUBLISHER_ID')}/{camp['id']}?sub4=auto"
            links.append({
                'name': camp['name'],
                'id': camp['id'],
                'link': link,
                'fetched_at': __import__('datetime').datetime.now().isoformat()
            })
        
        # Lưu vào file
        with open('auto_links.json', 'w', encoding='utf-8') as f:
            json.dump(links, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Fetched {len(links)} links automatically")
        return links
    else:
        print(f"❌ Failed: {response.status_code}")
        return []

if __name__ == "__main__":
    auto_fetch_links()
