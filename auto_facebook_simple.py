from config_global import config
"""
Auto post Facebook - Chạy ngay!
"""
import requests
import time
import json
import os
from datetime import datetime

# ===== CẤU HÌNH =====
PAGE_ID = "YOUR_PAGE_ID"  # Sửa thành ID trang của bạn
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"  # Dán token vừa copy

# Link affiliate Shopee đang hoạt động
SHOPEE_LINK = "https://go.isclix.com/deep_link/v6/6983938396644077046/4751584435713464237?sub4=sen_v3"

# Danh sách bài đăng
POSTS = [
    {
        "content": f"""🛍️ SHOPEE SALE GIỮA THÁNG - GIẢM ĐẾN 70%

🔥 Voucher Xtra giảm đến 5 triệu đồng
🔥 Freeship 0Đ cho đơn hàng
🔥 Đồng giá từ 9.000Đ

👉 Mua sắm ngay: {SHOPEE_LINK}

#SaleShopee #GiamGia""",
        "time": "07:00"
    },
    {
        "content": f"""⚡ FLASH SALE - SĂN DEAL GIÁ SỐC

✅ Giảm đến 50% 
✅ Free ship toàn quốc
✅ Nhận voucher 200K

👉 Mua ngay: {SHOPEE_LINK}

#FlashSale #DealHot""",
        "time": "12:00"
    },
    {
        "content": f"""🌙 SALE ĐÊM - GIẢM ĐẾN 70%

🔥 Thời trang, điện tử, mỹ phẩm
🔥 Mã giảm giá đến 500K
🔥 Freeship mọi đơn

👉 Săn sale ngay: {SHOPEE_LINK}

#SaleDem #MuaSamOnline""",
        "time": "20:00"
    }
]

def post_to_facebook(content):
    """Đăng bài lên Facebook Page"""
    url = f"https://graph.facebook.com/v21.0/{PAGE_ID}/feed"
    data = {
        "message": content,
        "access_token": ACCESS_TOKEN
    }
    
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Đã đăng bài: {content[:50]}...")
            print(f"   Post ID: {result.get('id')}")
            return True
        else:
            print(f"❌ Lỗi: {response.json()}")
            return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def post_all_manually():
    """Đăng tất cả bài ngay lập tức"""
    print("=" * 50)
    print("🚀 BẮT ĐẦU ĐĂNG BÀI")
    print("=" * 50)
    
    for i, post in enumerate(POSTS, 1):
        print(f"\n📝 Bài {i}/{len(POSTS)}")
        print(f"   Nội dung: {post['content'][:80]}...")
        
        if post_to_facebook(post['content']):
            print(f"   ✅ Đã đăng bài {i}")
        else:
            print(f"   ❌ Đăng thất bại")
        
        if i < len(POSTS):
            print("   ⏰ Chờ 5 phút đến bài tiếp theo...")
            time.sleep(300)  # 5 phút
    
    print("\n" + "=" * 50)
    print("✅ ĐÃ ĐĂNG XONG TẤT CẢ BÀI!")
    print("=" * 50)

if __name__ == "__main__":
    print("=" * 50)
    print("🤖 AUTO POST FACEBOOK")
    print("=" * 50)
    print(f"📊 Số bài: {len(POSTS)}")
    print(f"📅 Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔗 Link Shopee: {SHOPEE_LINK[:60]}...")
    print("=" * 50)
    
    if PAGE_ID == "YOUR_PAGE_ID" or ACCESS_TOKEN == "YOUR_ACCESS_TOKEN":
        print("\n❌ CHƯA CẤU HÌNH!")
        print("👉 Sửa PAGE_ID và ACCESS_TOKEN trong file")
    else:
        post_all_manually()


