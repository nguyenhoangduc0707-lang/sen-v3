import requests
import webbrowser
from urllib.parse import urlencode
from dotenv import set_key

CLIENT_KEY = "awa6cdjba8pizprl"
CLIENT_SECRET = "hGLKRm0zJyQx9fMObmIP22MTk5JiMH86"
REDIRECT_URI = "https://your-domain.com/callback"

# Tạo URL ủy quyền
params = {
    "client_key": CLIENT_KEY,
    "response_type": "code",
    "scope": "user.info.basic,video.upload,video.publish",
    "redirect_uri": REDIRECT_URI,
}
auth_url = "https://www.tiktok.com/v2/auth/authorize/?" + urlencode(params)

print("=" * 60)
print("🔐 LẤY MÃ CODE TIKTOK")
print("=" * 60)
print("\n👉 Truy cập URL sau:")
print(auth_url)
print("\n👉 Sau khi ủy quyền, copy mã 'code' từ URL")
print("=" * 60)

webbrowser.open(auth_url)

# Nhập mã code
auth_code = input("\n📝 Dán mã code vào đây: ").strip()

if not auth_code:
    print("❌ Chưa nhập mã code!")
    exit()

# Đổi code lấy token
url = "https://open.tiktokapis.com/v2/oauth/token/"
data = {
    "client_key": CLIENT_KEY,
    "client_secret": CLIENT_SECRET,
    "code": auth_code,
    "grant_type": "authorization_code",
    "redirect_uri": REDIRECT_URI,
}
headers = {"Content-Type": "application/x-www-form-urlencoded"}

response = requests.post(url, data=data, headers=headers)
result = response.json()

print("\n" + "=" * 60)
if "access_token" in result:
    print("✅ THÀNH CÔNG!")
    print(f"   Access Token: {result['access_token'][:50]}...")
    print(f"   Open ID: {result.get('open_id')}")
    
    # Lưu vào .env
    set_key(".env", "TIKTOK_ACCESS_TOKEN", result['access_token'])
    set_key(".env", "TIKTOK_OPEN_ID", result.get('open_id', ''))
    print("\n✅ Đã lưu token mới vào .env")
else:
    print(f"❌ LỖI: {result.get('error')}")
    print(f"   {result.get('error_description', '')}")
print("=" * 60)
