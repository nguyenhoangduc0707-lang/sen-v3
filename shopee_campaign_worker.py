# shopee_campaign_worker.py
import csv
import os
from datetime import datetime, timedelta
import requests
import json
from pathlib import Path

class ShopeeCampaignWorker:
    def __init__(self):
        self.campaigns = []
        self.daily_themes = []
        self.load_campaign_data()
        
    def load_campaign_data(self):
        """Đọc dữ liệu từ file CSV"""
        csv_path = "E:\\DYT_01\\[SHOPEE]  ✨ JUNE 2026 ✨ - 1) 😀Overall-Jun.csv"
        
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            data = list(reader)
            
        # Parse CAMPAIGN OVERALL section
        in_campaign = False
        for row in data:
            if 'CAMPAIGN OVERALL' in str(row):
                in_campaign = True
                continue
            if in_campaign and len(row) > 2 and row[0] == 'Campaign':
                # Lấy thông tin các chiến dịch
                campaigns_row = row
                break
                
        # Parse Daily Theme section  
        in_daily = False
        for row in data:
            if 'DAILY THEME' in str(row):
                in_daily = True
                continue
            if in_daily and len(row) > 2 and row[0] and row[0].isdigit():
                self.daily_themes.append({
                    'date': row[0],
                    'weekday': row[1],
                    'theme': row[2],
                    'vietnamese': row[3],
                    'sub_title': row[4]
                })
                
    def generate_affiliate_content(self, campaign_name, date):
        """Tạo nội dung affiliate cho chiến dịch"""
        content_templates = {
            '6.6': f"""
🎉 SIÊU SALE 6.6 - GIỮA NĂM RỰC RỠ 🎉

✨ Shopee Mall giảm đến 50%
✨ Voucher Xtra lên đến 6 triệu đồng
✨ Cơ hội trúng 66 tivi 65 inch
✨ Freeship 0Đ cho đơn hàng đủ điều kiện
✨ SPayLater mua trước trả sau 0%

🔗 Mua sắm ngay: https://shopee.vn/m/6-6
#Shopee6_6 #SaleGiuaNam #Affiliate
            """,
            '15.6': f"""
📣 SALE GIỮA THÁNG 15.6 - RẺ BẤT NGỜ 📣

🔥 Voucher Xtra giảm đến 6 triệu đồng
🔥 SVIP giảm đến 20% mỗi ngày
🔥 Freeship 0Đ toàn quốc
🔥 Mua sắm thả ga cùng ShopeePay

🎯 Săn sale ngay: https://shopee.vn/m/15-sale-giua-thang
#Shopee15_6 #SaleGiuaThang
            """,
            '25.6': f"""
💥 LƯƠNG VỀ - SALE TO 25.6 💥

🎁 ShopeeVIP 1st Birthday - Giảm 20% mỗi ngày
🎁 SPayLater 0% đến 6 kỳ
🎁 Siêu voucher freeship 0Đ
🎁 Hàng ngàn sản phẩm giảm sốc

🛍️ Đặt mua ngay: https://shopee.vn/m/sale-cuoi-thang-don-luong-ve
#Shopee25_6 #LuongVeSaleTo
            """
        }
        
        for key, template in content_templates.items():
            if key in campaign_name:
                return template.format(date=date)
        
        return f"""
🛒 SALE LỚN TẠI SHOPEE - NGÀY {date} 🛒

⭐ Ưu đãi đặc biệt cho ngày hôm nay
⭐ Giảm giá sốc lên đến 50%
⭐ Voucher freeship toàn quốc
⭐ Thanh toán qua ShopeePay ưu đãi thêm

👉 Xem ngay: https://shopee.vn/
"""
    
    def get_daily_theme_content(self, theme_data):
        """Tạo nội dung theo chủ đề hàng ngày"""
        theme = theme_data['theme']
        vietnamese = theme_data['vietnamese']
        sub_title = theme_data['sub_title']
        
        theme_content = {
            'Dress up & Make up': f"""
✨ {vietnamese} - {sub_title} ✨

💄 Mỹ phẩm chính hãng giảm đến 50%
👗 Thời trang mới nhất từ các thương hiệu nổi tiếng
💋 Set quà tặng độc quyền chỉ hôm nay
🎁 Mua 1 tặng 1 cho đơn hàng đầu tiên

🛍️ Khám phá ngay: https://shopee.vn/
            """,
            'Low Price Day': f"""
⚡ {vietnamese} - {sub_title} ⚡

🔥 Săn deal chỉ từ 1.000Đ
🔥 Số lượng có hạn - Nhanh tay kẻo lỡ
🔥 Hàng ngàn sản phẩm giá tốt nhất ngày
🔥 Freeship 0Đ cho đơn 0Đ

🎯 Tham gia ngay: https://shopee.vn/
            """,
            'Entertainment Weekend': f"""
🎪 {vietnamese} - {sub_title} 🎪

🎬 Siêu deal cuối tuần giảm đến 50%
🎮 Gaming & giải trí giá rẻ bất ngờ
📱 Điện thoại, tablet khuyến mãi sốc
🎁 Live sale độc quyền 20-22h

🛒 Mua sắm ngay: https://shopee.vn/
            """
        }
        
        return theme_content.get(theme, f"""
📢 {vietnamese} 📢

{'-' * 40}
{sub_title}
{'-' * 40}

🎉 Ưu đãi đặc biệt chỉ hôm nay
🎉 Mua sắm thông minh - Tiết kiệm tối đa

👉 Nhận ngay ưu đãi: https://shopee.vn/
        """)
    
    def post_to_platforms(self, content, platform='all'):
        """Đăng nội dung lên các nền tảng"""
        # Import các hàm từ workers hiện có
        try:
            from auto_post_facebook import post_to_facebook
            from auto_post_telegram import post_to_telegram
            from auto_post_zalo import post_to_zalo
        except ImportError as e:
            print(f"⚠️ Không thể import module post: {e}")
            print(f"📝 Nội dung sẽ được lưu vào file thay vì đăng trực tiếp")
            self.save_content_to_file(content)
            return
            
        if platform in ['all', 'facebook']:
            try:
                post_to_facebook(content)
                print("✓ Đã đăng lên Facebook")
            except Exception as e:
                print(f"✗ Lỗi Facebook: {e}")
                
        if platform in ['all', 'telegram']:
            try:
                post_to_telegram(content)
                print("✓ Đã đăng lên Telegram")
            except Exception as e:
                print(f"✗ Lỗi Telegram: {e}")
                
        if platform in ['all', 'zalo']:
            try:
                post_to_zalo(content)
                print("✓ Đã đăng lên Zalo")
            except Exception as e:
                print(f"✗ Lỗi Zalo: {e}")
    
    def save_content_to_file(self, content):
        """Lưu nội dung vào file để kiểm tra"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"campaign_content_{timestamp}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"📁 Đã lưu nội dung vào file: {filename}")
    
    def run_daily_schedule(self, days_ahead=0):
        """Chạy worker cho ngày cụ thể"""
        today = datetime.now()
        target_date = today + timedelta(days=days_ahead)
        date_str = target_date.strftime("%-d/%-m")  # Format: D/M
        
        print(f"\n{'='*60}")
        print(f"📅 CHẠY CAMPAIGN WORKER - NGÀY {target_date.strftime('%d/%m/%Y')}")
        print(f"{'='*60}\n")
        
        # Tìm chủ đề trong ngày
        theme_for_date = None
        for theme in self.daily_themes:
            if theme['date'] == date_str:
                theme_for_date = theme
                break
        
        # Kiểm tra xem có phải ngày campaign spike không
        campaign_for_date = None
        spike_dates = {
            '1/6': '1.6 Opening Sale',
            '6/6': '6.6 Shopee Mid Year Mega Sale', 
            '15/6': '15.6 Mid-month',
            '25/6': '25.6 Payday'
        }
        
        if date_str in spike_dates:
            campaign_for_date = spike_dates[date_str]
        
        # Tạo nội dung
        contents = []
        
        if campaign_for_date:
            print(f"🎯 Hôm nay là ngày {campaign_for_date}")
            content = self.generate_affiliate_content(campaign_for_date, date_str)
            contents.append(content)
        
        if theme_for_date:
            print(f"📌 Chủ đề hôm nay: {theme_for_date['vietnamese']}")
            daily_content = self.get_daily_theme_content(theme_for_date)
            contents.append(daily_content)
        
        if not contents:
            print("⚠️ Không có sự kiện đặc biệt hôm nay")
            return
        
        # Gộp nội dung
        final_content = "\n\n".join(contents)
        
        # Đăng bài
        print("\n📤 Đang đăng nội dung lên các nền tảng...")
        self.post_to_platforms(final_content)
        
        return final_content

def main():
    """Main function để chạy worker"""
    worker = ShopeeCampaignWorker()
    
    print("""
    ╔═══════════════════════════════════════╗
    ║   SHOPEE CAMPAIGN AFFILIATE WORKER    ║
    ║   TỰ ĐỘNG TẠO NỘI DUNG THEO LỊCH      ║
    ╚═══════════════════════════════════════╝
    """)
    
    print("Chọn chế độ chạy:")
    print("1. Chạy cho hôm nay")
    print("2. Chạy cho ngày mai")
    print("3. Chạy cho tất cả các ngày trong tháng (pre-schedule)")
    print("4. Xem lịch campaign")
    
    choice = input("\nLựa chọn (1-4): ").strip()
    
    if choice == '1':
        worker.run_daily_schedule(0)
    elif choice == '2':
        worker.run_daily_schedule(1)
    elif choice == '3':
        print("\n📅 Đang tạo content cho tất cả các ngày campaign...")
        spike_dates = ['1/6', '6/6', '15/6', '25/6']
        for date in spike_dates:
            # Parse date string to datetime
            day, month = map(int, date.split('/'))
            target_date = datetime(2026, month, day)
            days_ahead = (target_date - datetime.now()).days
            if days_ahead >= 0:
                print(f"\n--- Ngày {date} ---")
                worker.run_daily_schedule(days_ahead)
    elif choice == '4':
        print("\n📆 LỊCH CAMPAIGN THÁNG 6/2026:")
        print("-" * 50)
        for theme in worker.daily_themes[:20]:  # Show first 20 days
            print(f"{theme['date']}: {theme['vietnamese']}")
        print("\n🎯 Các ngày Spike quan trọng:")
        print("1/6: Opening Sale")
        print("6/6: Mid Year Mega Sale")
        print("15/6: Mid-month Sale")
        print("25/6: Payday Sale")
    else:
        print("❌ Lựa chọn không hợp lệ")

if __name__ == "__main__":
    main()