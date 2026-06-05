import requests

# === MÃ CODE BẠN CUNG CẤP ===
AUTH_CODE = "20260602164641CDD6D89AD7BDE00298E0"

# Thông tin App TikTok
CLIENT_KEY = "awa6cdjba8pizprl"
CLIENT_SECRET = "hGLKRm0zJyQx9fMObmIP22MTk5JiMH86"
REDIRECT_URI = "https://your-domain.com/callback"

print("=" * 60)
print("🔐 ĐỔI MÃ CODE LẤY ACCESS TOKEN")
print("=" * 60)

url = "https://open.tiktokapis.com/v2/oauth/token/"
data = {
    "client_key": CLIENT_KEY,
    "client_secret": CLIENT_SECRET,
    "code": AUTH_CODE,
    "grant_type": "authorization_code",
    "redirect_uri": REDIRECT_URI,
}
headers = {"Content-Type": "application/x-www-form-urlencoded"}

try:
    response = requests.post(url, data=data, headers=headers, timeout=30)
    result = response.json()
    
    print(f"\n📡 Response Status: {response.status_code}")
    
    if "access_token" in result:
        print("\n✅ THÀNH CÔNG! ĐÃ LẤY ĐƯỢC TOKEN:")
        print(f"   Access Token: {result['access_token'][:50]}...")
        print(f"   Open ID: {result.get('open_id')}")
        print(f"   Refresh Token: {result.get('refresh_token', 'N/A')[:50]}...")
        print(f"   Expires In: {result.get('expires_in')} giây")
        
        # Lưu vào .env
        import os
        from dotenv import set_key
        
        set_key(".env", "TIKTOK_ACCESS_TOKEN", result['access_token'])
        set_key(".env", "TIKTOK_OPEN_ID", result.get('open_id', ''))
        
        print("\n✅ Đã lưu token vào file .env")
        print("\n🚀 Bây giờ bạn có thể đăng ảnh/video lên TikTok!")
        
    elif "error" in result:
        print(f"\n❌ LỖI: {result.get('error')}")
        print(f"   Mô tả: {result.get('error_description', 'N/A')}")
        
        if "redirect_uri" in str(result):
            print("\n⚠️ Lưu ý: Redirect URI không khớp!")
            print("   Cần cập nhật đúng URI trong TikTok Developer Console")
            
except Exception as e:
    print(f"\n❌ Exception: {e}")

print("\n" + "=" * 60)
