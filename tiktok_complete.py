"""
TikTok Complete Integration - Lấy token và đăng ảnh
"""
import requests
import webbrowser
from urllib.parse import urlencode
from dotenv import set_key
import os

# === CẤU HÌNH TIKTOK APP ===
CLIENT_KEY = "awa6cdjba8pizprl"
CLIENT_SECRET = "hGLKRm0zJyQx9fMObmIP22MTk5JiMH86"
REDIRECT_URI = "https://your-domain.com/callback"

# === BƯỚC 1: LẤY MÃ CODE ===
def get_auth_code():
    """Tạo URL và mở trình duyệt để lấy mã code"""
    params = {
        "client_key": CLIENT_KEY,
        "response_type": "code",
        "scope": "user.info.basic,video.upload,video.publish",
        "redirect_uri": REDIRECT_URI,
    }
    auth_url = "https://www.tiktok.com/v2/auth/authorize/?" + urlencode(params)
    
    print("\n" + "=" * 60)
    print("🔐 BƯỚC 1: LẤY MÃ ỦY QUYỀN (CODE)")
    print("=" * 60)
    print("\n👉 Truy cập URL sau và đăng nhập TikTok:")
    print(auth_url)
    print("\n👉 Sau khi ủy quyền, copy mã 'code' từ URL")
    print("   Ví dụ: https://your-domain.com/callback?code=abc123...")
    print("\n⚠️ Mã code chỉ có hiệu lực trong 5 phút!")
    print("=" * 60)
    
    webbrowser.open(auth_url)
    return input("\n📝 Dán mã code vào đây: ").strip()

# === BƯỚC 2: ĐỔI CODE LẤY ACCESS TOKEN ===
def exchange_code_for_token(auth_code):
    """Đổi mã code lấy access token"""
    print("\n" + "=" * 60)
    print("🔐 BƯỚC 2: ĐỔI CODE LẤY ACCESS TOKEN")
    print("=" * 60)
    
    url = "https://open.tiktokapis.com/v2/oauth/token/"
    data = {
        "client_key": CLIENT_KEY,
        "client_secret": CLIENT_SECRET,
        "code": auth_code,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    
    try:
        response = requests.post(url, data=data, headers=headers, timeout=30)
        result = response.json()
        
        if "access_token" in result:
            access_token = result["access_token"]
            open_id = result.get("open_id")
            
            print(f"\n✅ THÀNH CÔNG!")
            print(f"   Access Token: {access_token[:50]}...")
            print(f"   Open ID: {open_id}")
            print(f"   Expires in: {result.get('expires_in')} giây")
            
            # Lưu vào .env
            set_key(".env", "TIKTOK_ACCESS_TOKEN", access_token)
            set_key(".env", "TIKTOK_OPEN_ID", open_id)
            print("\n✅ Đã lưu token vào .env")
            
            return access_token, open_id
        else:
            print(f"\n❌ LỖI: {result.get('error')}")
            print(f"   {result.get('error_description', '')}")
            return None, None
    except Exception as e:
        print(f"\n❌ Exception: {e}")
        return None, None

# === BƯỚC 3: LẤY THÔNG TIN NGƯỜI TẠO ===
def get_creator_info(access_token):
    """Lấy thông tin người tạo (privacy level options)"""
    print("\n" + "=" * 60)
    print("👤 BƯỚC 3: LẤY THÔNG TIN NGƯỜI TẠO")
    print("=" * 60)
    
    url = "https://open.tiktokapis.com/v2/post/publish/creator_info/query/"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, headers=headers, timeout=30)
        result = response.json()
        
        if result.get("error", {}).get("code") == "ok":
            data = result.get("data", {})
            print(f"\n✅ Thông tin người tạo:")
            print(f"   Username: {data.get('creator_username')}")
            print(f"   Nickname: {data.get('creator_nickname')}")
            print(f"   Privacy options: {data.get('privacy_level_options')}")
            print(f"   Comment disabled: {data.get('comment_disabled')}")
            return data
        else:
            print(f"\n❌ Lỗi: {result.get('error', {}).get('code')}")
            return None
    except Exception as e:
        print(f"\n❌ Exception: {e}")
        return None

# === BƯỚC 4: ĐĂNG ẢNH LÊN TIKTOK ===
def post_photo(access_token, image_urls, title="", description=""):
    """Đăng ảnh lên TikTok"""
    print("\n" + "=" * 60)
    print("📸 BƯỚC 4: ĐĂNG ẢNH LÊN TIKTOK")
    print("=" * 60)
    
    url = "https://open.tiktokapis.com/v2/post/publish/content/init/"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    data = {
        "post_info": {
            "title": title[:90],
            "description": description[:4000],
            "privacy_level": "PUBLIC_TO_EVERYONE",
            "disable_comment": False,
            "auto_add_music": True
        },
        "source_info": {
            "source": "PULL_FROM_URL",
            "photo_cover_index": 0,
            "photo_images": image_urls[:35]
        },
        "post_mode": "DIRECT_POST",
        "media_type": "PHOTO"
    }
    
    print(f"\n📸 Đang đăng {len(image_urls)} ảnh...")
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=60)
        result = response.json()
        
        if result.get("error", {}).get("code") == "ok":
            publish_id = result.get("data", {}).get("publish_id")
            print(f"\n✅ ĐĂNG ẢNH THÀNH CÔNG!")
            print(f"   Publish ID: {publish_id}")
            return True
        else:
            error = result.get("error", {})
            print(f"\n❌ Lỗi: {error.get('code')} - {error.get('message')}")
            return False
    except Exception as e:
        print(f"\n❌ Exception: {e}")
        return False

# === MAIN ===
def main():
    print("=" * 60)
    print("🎯 TIKTOK API INTEGRATION - COMPLETE FLOW")
    print("=" * 60)
    
    # Kiểm tra token đã có trong .env chưa
    from dotenv import load_dotenv
    load_dotenv()
    existing_token = os.getenv("TIKTOK_ACCESS_TOKEN")
    
    if existing_token and len(existing_token) > 20:
        print("\n✅ Đã có access token trong .env")
        use_existing = input("👉 Sử dụng token cũ? (y/n): ").strip().lower()
        
        if use_existing == 'y':
            access_token = existing_token
            open_id = os.getenv("TIKTOK_OPEN_ID")
        else:
            # Lấy token mới
            auth_code = get_auth_code()
            if not auth_code:
                print("❌ Chưa nhập mã code!")
                return
            access_token, open_id = exchange_code_for_token(auth_code)
            if not access_token:
                return
    else:
        # Lấy token mới
        auth_code = get_auth_code()
        if not auth_code:
            print("❌ Chưa nhập mã code!")
            return
        access_token, open_id = exchange_code_for_token(auth_code)
        if not access_token:
            return
    
    # Lấy thông tin người tạo
    creator_info = get_creator_info(access_token)
    
    # Chuẩn bị ảnh (cần URL ảnh công khai)
    print("\n" + "=" * 60)
    print("📸 CHUẨN BỊ ĐĂNG ẢNH")
    print("=" * 60)
    
    # Link Shopee affiliate
    SHOPEE_LINK = "https://go.isclix.com/deep_link/v6/6983938396644077046/4751584435713464237?sub4=tiktok"
    
    description = f"""🔥 SHOPEE SALE GIỮA THÁNG - GIẢM ĐẾN 70%

✅ Voucher Xtra giảm đến 5 triệu đồng
✅ Freeship 0Đ cho đơn hàng

👉 Mua sắm ngay: {SHOPEE_LINK}

#ShopeeSale #GiamGia #MuaSam
"""
    
    # Cần có URL ảnh thật
    image_urls = [
        "https://your-domain.com/shopee_banner_1.jpg",
        "https://your-domain.com/shopee_banner_2.jpg"
    ]
    
    print("\n📝 Nội dung bài đăng:")
    print(f"   Title: Shopee Sale Giữa Tháng")
    print(f"   Description: {description[:100]}...")
    print(f"   Images: {len(image_urls)} ảnh")
    
    confirm = input("\n👉 Đăng ảnh lên TikTok? (y/n): ").strip().lower()
    if confirm == 'y':
        post_photo(access_token, image_urls, "Shopee Sale Giữa Tháng", description)
    else:
        print("❌ Đã hủy đăng bài")

if __name__ == "__main__":
    main()
