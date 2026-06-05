"""
Auto Post Scheduler - Tự động đăng bài theo lịch
"""
import json
import time
import random
import webbrowser
from datetime import datetime, timedelta
import threading

class AutoScheduler:
    def __init__(self):
        self.posts = []
        self.running = False
    
    def load_campaigns(self):
        """Load campaigns từ database"""
        import sqlite3
        conn = sqlite3.connect('sen_v3.db')
        cursor = conn.cursor()
        
        # Lấy financial campaigns ưu tiên
        cursor.execute("SELECT id, name FROM accesstrade_campaigns WHERE category IN ('FINANCIAL SERVICES', '60', '35') LIMIT 20")
        campaigns = cursor.fetchall()
        conn.close()
        
        return campaigns
    
    def generate_post_content(self, name, campaign_id):
        """Tạo nội dung bài đăng"""
        publisher_id = "6983938396644077046"
        link = f"https://go.isclix.com/deep_link/v5/{publisher_id}/{campaign_id}?sub4=facebook_auto"
        
        templates = [
            f"🔥 HOT: {name}\n\n💰 Nhận ưu đãi đặc biệt ngay hôm nay!\n\n✅ Đăng ký nhanh trong 5 phút\n✅ Ưu đãi đến 50%\n\n👉 Link đăng ký: {link}\n\n#UuDai #KhuyenMai #TaiChinh",
            
            f"📢 {name}\n\n⚡ Siêu ưu đãi dành riêng cho bạn!\n🎁 Nhận ngay quà tặng hấp dẫn\n\n👉 Đăng ký: {link}\n\n#Sale #GiamGia #HotDeal",
            
            f"💥 BẤT NGỜ: {name}\n\n✅ Duy nhất trong tháng này\n✅ Tiết kiệm đến 1 triệu đồng\n\n👉 Nhận ngay ưu đãi: {link}\n\n#UuDaiSoc #FlashSale",
        ]
        
        return random.choice(templates), link
    
    def auto_post_sequence(self, campaigns, delay_minutes=30):
        """Tự động đăng bài theo trình tự"""
        print("=" * 70)
        print("🚀 AUTO POST SCHEDULER STARTED")
        print(f"📅 Total posts: {len(campaigns)}")
        print(f"⏰ Delay: {delay_minutes} minutes/post")
        print("=" * 70)
        
        for i, campaign in enumerate(campaigns, 1):
            campaign_id = campaign[0]
            name = campaign[1]
            
            content, link = self.generate_post_content(name, campaign_id)
            
            print(f"\n📝 Post #{i}: {name}")
            print(f"   Content: {content[:80]}...")
            print(f"   Link: {link}")
            
            # Lưu bài đăng để đăng sau
            with open('pending_posts.txt', 'a', encoding='utf-8') as f:
                f.write(f"\n{'='*60}")
                f.write(f"\n📝 POST #{i} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                f.write(f"\n📌 Campaign: {name}")
                f.write(f"\n📋 Content: {content}")
                f.write(f"\n🔗 Link: {link}")
                f.write(f"\n{'='*60}\n")
            
            # Mở trình duyệt để đăng thủ công (hoặc có thể tích hợp API)
            webbrowser.open(link)
            
            if i < len(campaigns):
                print(f"⏰ Chờ {delay_minutes} phút đến bài tiếp theo...")
                time.sleep(delay_minutes * 60)
        
        print("\n" + "=" * 70)
        print("✅ AUTO POST COMPLETED!")
        print(f"📊 Đã tạo {len(campaigns)} bài đăng")
        print("📁 Xem nội dung tại: pending_posts.txt")
        print("=" * 70)
    
    def generate_bulk_posts(self, campaigns):
        """Tạo nội dung bài đăng hàng loạt"""
        all_posts = []
        
        for campaign in campaigns:
            campaign_id = campaign[0]
            name = campaign[1]
            content, link = self.generate_post_content(name, campaign_id)
            
            all_posts.append({
                'campaign_id': campaign_id,
                'name': name,
                'content': content,
                'link': link,
                'generated_at': datetime.now().isoformat()
            })
        
        # Lưu vào file
        with open('bulk_posts.json', 'w', encoding='utf-8') as f:
            json.dump(all_posts, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Đã tạo {len(all_posts)} bài đăng trong bulk_posts.json")
        return all_posts

def main():
    scheduler = AutoScheduler()
    
    # Load campaigns
    print("📡 Đang tải campaigns...")
    campaigns = scheduler.load_campaigns()
    
    if not campaigns:
        print("❌ Không có campaigns nào!")
        return
    
    print(f"📊 Tìm thấy {len(campaigns)} campaigns")
    
    # Chọn số lượng bài đăng
    num_posts = min(20, len(campaigns))
    selected = campaigns[:num_posts]
    
    print("\n🎯 CHỌN CHẾ ĐỘ:")
    print("1. Tạo nội dung bài đăng (không tự động đăng)")
    print("2. Auto post (mở link để đăng thủ công)")
    print("3. Tạo file hàng loạt")
    
    choice = input("\nNhập lựa chọn (1/2/3): ")
    
    if choice == '1':
        # Chỉ tạo nội dung
        posts = scheduler.generate_bulk_posts(selected)
        print(f"\n✅ Đã tạo {len(posts)} bài đăng!")
        print("📁 Mở bulk_posts.json để xem nội dung")
        
    elif choice == '2':
        # Auto post
        scheduler.auto_post_sequence(selected, delay_minutes=5)
        
    elif choice == '3':
        # Tạo file hàng loạt
        scheduler.generate_bulk_posts(selected)
        print("\n✅ Đã tạo file bulk_posts.json")
        print("💡 Bạn có thể copy nội dung từ file này để đăng thủ công")
    
    else:
        print("❌ Lựa chọn không hợp lệ!")

if __name__ == "__main__":
    main()
