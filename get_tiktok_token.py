import requests
from urllib.parse import urlencode

CLIENT_KEY = "awa6cdjba8pizprl"
REDIRECT_URI = "https://your-domain.com/callback"
SCOPE = "user.info.basic,video.upload,video.publish"

# Tạo URL ủy quyền
params = {
    "client_key": CLIENT_KEY,
    "response_type": "code",
    "scope": SCOPE,
    "redirect_uri": REDIRECT_URI,
}
auth_url = "https://www.tiktok.com/v2/auth/authorize/?" + urlencode(params)

print("👉 Truy cập URL sau để ủy quyền:")
print(auth_url)
print("\n👉 Sau khi ủy quyền, copy mã code từ URL và chạy lệnh tiếp theo")
