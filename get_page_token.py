from config_global import config
import requests

# Dùng token cũ hoặc lấy token mới từ Graph Explorer
TOKEN = "YOUR_USER_ACCESS_TOKEN"  # Thay bằng token của bạn

url = f"https://graph.facebook.com/v21.0/61589228527389?fields=access_token&access_token={TOKEN}"
response = requests.get(url)
data = response.json()

print("Kết quả:")
print(data)

if 'access_token' in data:
    print(f"\n✅ Page Access Token: {data['access_token'][:50]}...")
    print("\n👉 Hãy copy token này vào .env")
else:
    print("\n❌ Không thể lấy token. Cần cấp quyền pages_manage_posts")


