"""
Generate bulk post content for social media
"""
import json
import sqlite3
from datetime import datetime

def generate_all_posts():
    """Tạo nội dung cho tất cả campaigns"""
    
    conn = sqlite3.connect('sen_v3.db')
    cursor = conn.cursor()
    
    # Lấy top campaigns
    cursor.execute("""
        SELECT id, name, category 
        FROM accesstrade_campaigns 
        WHERE category IN ('FINANCIAL SERVICES', '60', '35', 'E-COMMERCE')
        ORDER BY id
        LIMIT 30
    """)
    
    campaigns = cursor.fetchall()
    conn.close()
    
    publisher_id = "6983938396644077046"
    all_posts = []
    
    for campaign in campaigns:
        campaign_id = campaign[0]
        name = campaign[1]
        category = campaign[2]
        
        link = f"https://go.isclix.com/deep_link/v5/{publisher_id}/{campaign_id}?sub4=social_media"
        
        # Chọn template theo category
        if 'FINANCIAL' in str(category) or '60' in str(category) or '35' in str(category):
            templates = [
                f"💰 {name} - VAY TÍN CHẤP LÊN ĐẾN 500 TRIỆU\n\n✅ Thủ tục đơn giản, giải ngân nhanh\n✅ Lãi suất ưu đãi\n\n👉 Đăng ký ngay: {link}\n\n#VayVon #TaiChinh",
                f"📢 {name}\n\n⚡ Siêu ưu đãi tài chính\n✅ Nhận ngay hạn mức cao\n✅ Lãi suất cạnh tranh\n\n👉 Đăng ký: {link}",
                f"💳 MỞ THẺ TÍN DỤNG {name}\n\n✅ 100% online, không cần chứng minh thu nhập\n✅ Nhận thẻ sau 3 ngày\n✅ Hoàn tiền đến 5%\n\n👉 Mở thẻ ngay: {link}"
            ]
        else:
            templates = [
                f"🛍️ {name} - MUA SẮM GIÁ SỐC\n\n✅ Giảm giá đến 50%\n✅ Free ship đơn từ 200K\n✅ Nhận voucher hấp dẫn\n\n👉 Mua ngay: {link}",
                f"🎉 FLASH SALE - {name}\n\n⚡ Giảm sốc đến 70%\n⏰ Số lượng có hạn\n\n👉 Săn deal ngay: {link}"
            ]
        
        import random
        content = random.choice(templates)
        
        all_posts.append({
            'id': campaign_id,
            'name': name,
            'category': category,
            'content': content,
            'link': link,
            'generated_at': datetime.now().isoformat()
        })
    
    # Lưu tất cả bài đăng
    with open('all_posts.json', 'w', encoding='utf-8') as f:
        json.dump(all_posts, f, indent=2, ensure_ascii=False)
    
    # Tạo file dễ copy
    with open('posts_to_copy.txt', 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("📢 NỘI DUNG BÀI ĐĂNG MẠNG XÃ HỘI\n")
        f.write("=" * 80 + "\n\n")
        
        for i, post in enumerate(all_posts, 1):
            f.write(f"\n📌 BÀI ĐĂNG #{i}\n")
            f.write("-" * 40 + "\n")
            f.write(f"{post['content']}\n")
            f.write("-" * 40 + "\n\n")
    
    print("=" * 70)
    print(f"✅ Đã tạo {len(all_posts)} bài đăng")
    print("📁 File đã tạo:")
    print("   - all_posts.json (dữ liệu JSON)")
    print("   - posts_to_copy.txt (nội dung để copy)")
    print("=" * 70)
    
    # Hiển thị mẫu
    print("\n📋 MẪU BÀI ĐĂNG:")
    print("-" * 70)
    for i, post in enumerate(all_posts[:3], 1):
        print(f"\nBài {i}: {post['name'][:50]}")
        print(f"   {post['content'][:100]}...")
        print(f"   Link: {post['link'][:80]}...")

if __name__ == "__main__":
    generate_all_posts()
