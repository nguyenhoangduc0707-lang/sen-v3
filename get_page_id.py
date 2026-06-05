import requests
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('FACEBOOK_ACCESS_TOKEN')

if not token or 'your_' in token:
    print("❌ Token chưa được cấu hình đúng trong .env")
    exit(1)

print("=" * 50)
print("📋 DANH SÁCH TRANG CỦA BẠN")
print("=" * 50)

url = f'https://graph.facebook.com/v21.0/me/accounts?access_token={token}'

try:
    response = requests.get(url)
    data = response.json()
    
    if 'data' in data:
        for page in data['data']:
            print(f"\n📄 Tên trang: {page.get('name')}")
            print(f"🆔 Page ID: {page.get('id')}")
            print(f"🔑 Token: {page.get('access_token')[:50]}...")
            print("-" * 40)
        
        if data['data']:
            print(f"\n✅ Tìm thấy {len(data['data'])} trang")
            print("\n👉 COPY Page ID và thêm vào .env:")
            print('   FACEBOOK_PAGE_ID=' + data['data'][0]['id'])
        else:
            print("❌ Không tìm thấy trang nào. Hãy tạo Fanpage trước.")
    else:
        print(f"❌ Lỗi: {data.get('error', {}).get('message', 'Unknown error')}")
        
except Exception as e:
    print(f"❌ Lỗi kết nối: {e}")
