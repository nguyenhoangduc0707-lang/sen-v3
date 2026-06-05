import webbrowser
from urllib.parse import urlencode

CLIENT_KEY = "awa6cdjba8pizprl"
REDIRECT_URI = "https://your-domain.com/callback"
SCOPE = "user.info.basic,video.upload,video.publish"

params = {
    "client_key": CLIENT_KEY,
    "response_type": "code",
    "scope": SCOPE,
    "redirect_uri": REDIRECT_URI,
}
auth_url = "https://www.tiktok.com/v2/auth/authorize/?" + urlencode(params)

print("=" * 60)
print("🔐 TIKTOK OAUTH - LẤY MÃ CODE MỚI")
print("=" * 60)
print("\n👉 Truy cập URL sau và đăng nhập TikTok:")
print(auth_url)
print("\n👉 Sau khi ủy quyền, copy mã 'code' từ URL")
print("   Ví dụ: https://your-domain.com/callback?code=NEW_CODE")
print("\n⚠️ Mã code chỉ có hiệu lực trong 5 phút!")
print("=" * 60)

# Mở trình duyệt
webbrowser.open(auth_url)
