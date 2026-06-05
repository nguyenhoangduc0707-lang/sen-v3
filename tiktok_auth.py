import webbrowser
from urllib.parse import urlencode

CLIENT_KEY = "awa6cdjba8pizprl"
REDIRECT_URI = "https://your-domain.com/callback"  # Thay bằng URL thật
SCOPE = "user.info.basic,video.upload,video.publish"

params = {
    "client_key": CLIENT_KEY,
    "response_type": "code",
    "scope": SCOPE,
    "redirect_uri": REDIRECT_URI,
}
auth_url = "https://www.tiktok.com/v2/auth/authorize/?" + urlencode(params)

print("=" * 60)
print("🔐 TIKTOK OAUTH - LẤY ACCESS TOKEN")
print("=" * 60)
print("\n👉 Bước 1: Truy cập URL sau và đăng nhập TikTok:")
print(auth_url)
print("\n👉 Bước 2: Sau khi ủy quyền, copy mã 'code' từ URL")
print("   Ví dụ: https://your-domain.com/callback?code=abc123...")
print("\n👉 Bước 3: Dán mã code vào đây để lấy token")
print("=" * 60)

# Mở trình duyệt
webbrowser.open(auth_url)
