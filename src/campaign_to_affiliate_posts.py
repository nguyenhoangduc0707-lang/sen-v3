# campaign_to_affiliate_posts.py
import pandas as pd
import csv
from datetime import datetime, timedelta
import os
import re

class CampaignToAffiliatePosts:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.campaigns = []
        self.daily_themes = []
        self.affiliate_links = [
            "https://shorten.asia/3cSC6EUX",
            "https://shorten.asia/PjYek8R8",
            "https://shorten.asia/MxvRDqNg",
            "https://shorten.asia/cBGVb2kE"
        ]
        self.load_data()
    
    def load_data(self):
        """Đọc dữ liệu từ file CSV"""
        try:
            with open(self.csv_file, 'r', encoding='utf-8-sig') as f:
                content = f.read()
                lines = content.split('\n')
            
            # Tìm và parse dữ liệu campaigns
            in_campaign_overall = False
            for i, line in enumerate(lines):
                if 'CAMPAIGN OVERALL' in line:
                    in_campaign_overall = True
                    continue
                if in_campaign_overall and 'Campaign,' in line and '1.6' in line:
                    # Parse dòng campaign
                    parts = line.split(',')
                    if len(parts) > 4:
                        campaign_names = ['1.6 Opening Sale', '6.6 Shopee Mid Year Mega Sale', 
                                         '15.6 Mid-month', '25.6 Payday']
                        campaign_urls = [
                            'https://shopee.vn/m/6-6',
                            'https://shopee.vn/m/6-6',
                            'https://shopee.vn/m/15-sale-giua-thang',
                            'https://shopee.vn/m/sale-cuoi-thang-don-luong-ve'
                        ]
                        
                        for idx, name in enumerate(campaign_names):
                            self.campaigns.append({
                                'name': name,
                                'url': campaign_urls[idx],
                                'date': self.get_campaign_date(name)
                            })
                    break
            
            # Parse daily themes
            in_daily_theme = False
            for line in lines:
                if 'DAILY THEME' in line:
                    in_daily_theme = True
                    continue
                if in_daily_theme and line.startswith(',,'):
                    parts = line.split(',')
                    if len(parts) > 4 and parts[2] and parts[2].strip():
                        self.daily_themes.append({
                            'date': parts[1].strip() if len(parts) > 1 else '',
                            'theme': parts[2].strip() if len(parts) > 2 else '',
                            'vietnamese': parts[3].strip() if len(parts) > 3 else '',
                            'sub_title': parts[4].strip() if len(parts) > 4 else ''
                        })
            
            print(f"✅ Đã tải {len(self.campaigns)} campaigns")
            print(f"✅ Đã tải {len(self.daily_themes)} chủ đề hàng ngày")
            
        except Exception as e:
            print(f"❌ Lỗi đọc file: {e}")
            self.use_default_data()
    
    def get_campaign_date(self, campaign_name):
        """Lấy ngày diễn ra campaign"""
        dates = {
            '1.6': '01/06/2026',
            '6.6': '06/06/2026',
            '15.6': '15/06/2026',
            '25.6': '25/06/2026'
        }
        for key, date in dates.items():
            if key in campaign_name:
                return date
        return '06/2026'
    
    def use_default_data(self):
        """Dữ liệu mặc định nếu không đọc được file"""
        self.campaigns = [
            {'name': '1.6 Opening Sale', 'url': 'https://shopee.vn/m/6-6', 'date': '01/06/2026'},
            {'name': '6.6 Mid Year Mega Sale', 'url': 'https://shopee.vn/m/6-6', 'date': '06/06/2026'},
            {'name': '15.6 Mid-month Sale', 'url': 'https://shopee.vn/m/15-sale-giua-thang', 'date': '15/06/2026'},
            {'name': '25.6 Payday Sale', 'url': 'https://shopee.vn/m/sale-cuoi-thang-don-luong-ve', 'date': '25/06/2026'}
        ]
        
        self.daily_themes = [
            {'date': '2/6', 'theme': 'Dress up & Make up', 'vietnamese': 'Làm Đẹp - Mặc Chất', 'sub_title': 'Hot deal giảm đến 50%'},
            {'date': '3/6', 'theme': 'Low Price Day', 'vietnamese': 'Thứ 4 Siêu rẻ', 'sub_title': 'Độc Quyền Deal 1.000Đ'},
            {'date': '4/6', 'theme': 'Early Bird Sale', 'vietnamese': 'Sale bắt đầu từ 0H 4.6', 'sub_title': 'Siêu Nhanh Siêu Rẻ'},
            {'date': '6/6', 'theme': '6.6 Shopee Mid Year Mega Sale', 'vietnamese': '6.6 Siêu Sale Giữa Năm', 'sub_title': 'Giảm đến 50% + Voucher 6 triệu'},
        ]
    
    def create_campaign_post(self, campaign, affiliate_link):
        """Tạo bài viết cho campaign"""
        # Lấy ưu đãi đặc biệt theo campaign
        benefits = self.get_campaign_benefits(campaign['name'])
        
        content = f"""
{'='*60}
🎉 {campaign['name'].upper()} - {campaign['date']} 🎉
{'='*60}

🔥 SIÊU SALE CỰC SỐC 🔥

✨ ƯU ĐÃI ĐẶC BIỆT:
{benefits}

📅 Thời gian: {campaign['date']}

🛍️ MUA SẮM NGAY HÔM NAY:
{affiliate_link}

🏷️ #{self.get_hashtag(campaign['name'])} #Shopee #Affiliate #Sale
{'='*60}
"""
        return content
    
    def get_campaign_benefits(self, campaign_name):
        """Lấy ưu đãi theo campaign"""
        benefits_map = {
            '1.6': """• ✨ Siêu Rẻ - Chỉ Từ 1.000Đ
• 🎂 ShopeeVIP - Giảm 20% Mỗi Ngày
• 🚚 Freeship 0Đ (*)
• 💳 SPayLater 0%""",
            '6.6': """• ✨ Shopee Mall - Giảm Đến 50%
• 🎫 Voucher Xtra giảm đến 6 triệu
• 📺 Cơ Hội Trúng 66 Tivi 65-Inch
• 🚚 Freeship 0Đ (*)""",
            '15.6': """• 🎫 Voucher Xtra giảm đến 6 triệu đồng
• 👑 ShopeeVIP - Voucher giảm đến 30%
• 🚚 Freeship 0Đ (*)
• 💳 SPayLater 0% đến 6 kỳ""",
            '25.6': """• 🎂 ShopeeVIP 1st Birthday - Giảm 20% Mỗi Ngày
• 💳 SPayLater - Mua trước trả sau 0%
• 🚚 Freeship 0Đ (*)
• 🎁 Hàng ngàn sản phẩm giảm sốc"""
        }
        
        for key, benefits in benefits_map.items():
            if key in campaign_name:
                return benefits
        return "• ✨ Giảm giá sốc lên đến 50%\n• 🚚 Freeship 0Đ\n• 🎫 Voucher giá trị lớn"
    
    def get_hashtag(self, campaign_name):
        """Tạo hashtag cho campaign"""
        if '1.6' in campaign_name:
            return 'OpeningSale'
        elif '6.6' in campaign_name:
            return 'MidYearSale'
        elif '15.6' in campaign_name:
            return 'MidMonthSale'
        elif '25.6' in campaign_name:
            return 'PaydaySale'
        return 'ShopeeSale'
    
    def create_daily_theme_post(self, theme, affiliate_link):
        """Tạo bài viết theo chủ đề hàng ngày"""
        content = f"""
{'='*50}
📅 {theme['vietnamese']}
{'='*50}

🔥 {theme['sub_title']}

✨ CHỦ ĐỀ HÔM NAY:
{self.get_theme_description(theme['theme'])}

🛍️ SĂN DEAL NGAY:
{affiliate_link}

🏷️ #{self.get_theme_hashtag(theme['theme'])} #Shopee #DailyDeal
"""
        return content
    
    def get_theme_description(self, theme):
        """Mô tả theo chủ đề"""
        descriptions = {
            'Dress up & Make up': """• 💄 Mỹ phẩm chính hãng giảm 50%
• 👗 Thời trang mới nhất - Giá sốc
• 💋 Set quà tặng độc quyền
• 🎁 Mua 1 tặng 1 đơn hàng đầu""",
            'Low Price Day': """• ⚡ Độc quyền deal chỉ 1.000Đ
• 🔥 Số lượng có hạn - Nhanh tay
• 🎯 Hàng ngàn sản phẩm giá rẻ
• 🚚 Freeship 0Đ""",
            'Entertainment Weekend': """• 🎬 Siêu deal cuối tuần - 50%
• 🎧 Gaming & giải trí giá rẻ
• 📱 Điện thoại, tablet khuyến mãi
• 🎁 Live sale 20-22h""",
            'Early Bird Sale': """• ⏰ Sale bắt đầu từ 0h
• 🎫 Voucher độc quyền
• 🔥 Deal sốc giới hạn
• 🚚 Freeship toàn quốc"""
        }
        
        for key, desc in descriptions.items():
            if key in theme:
                return desc
        return "• ✨ Siêu ưu đãi hôm nay\n• 🎁 Quà tặng kèm hấp dẫn"
    
    def get_theme_hashtag(self, theme):
        """Hashtag cho chủ đề"""
        hashtags = {
            'Dress up & Make up': 'LamDepMacChat',
            'Low Price Day': 'Thu4Sieure',
            'Entertainment Weekend': 'CuoiTuanGiaiTri',
            'Early Bird Sale': 'EarlyBirdSale',
            '6.6 Shopee Mid Year Mega Sale': 'Shopee6_6'
        }
        
        for key, tag in hashtags.items():
            if key in theme:
                return tag
        return 'ShopeeDaily'
    
    def generate_all_posts(self):
        """Tạo tất cả bài viết"""
        print("\n" + "="*60)
        print("📝 TẠO BÀI VIẾT AFFILIATE TỪ CAMPAIGN SHOPEE")
        print("="*60)
        
        post_count = 0
        
        # Tạo bài viết cho từng campaign với từng link affiliate
        print("\n📅 CAMPAIGN POSTS:")
        for campaign in self.campaigns:
            for idx, link in enumerate(self.affiliate_links):
                post_count += 1
                content = self.create_campaign_post(campaign, link)
                filename = f"campaign_{campaign['name'].replace(' ', '_')}_link{idx+1}.txt"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"  ✅ {filename}")
        
        # Tạo bài viết cho từng chủ đề
        print("\n📌 DAILY THEME POSTS:")
        for theme in self.daily_themes[:10]:  # Giới hạn 10 theme đầu
            for idx, link in enumerate(self.affiliate_links[:2]):  # 2 link cho theme
                post_count += 1
                content = self.create_daily_theme_post(theme, link)
                theme_name = theme['theme'].replace(' ', '_').replace('/', '_')
                filename = f"theme_{theme_name}_{idx+1}.txt"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"  ✅ {filename}")
        
        # Tạo file tổng hợp
        self.create_summary_file()
        
        print(f"\n{'='*60}")
        print(f"🎉 HOÀN TẤT! Đã tạo {post_count} bài viết")
        print(f"📁 Xem các file .txt để sử dụng")
        print(f"{'='*60}")
    
    def create_summary_file(self):
        """Tạo file tổng hợp tất cả bài viết"""
        with open("ALL_AFFILIATE_POSTS_COMPLETE.txt", "w", encoding="utf-8") as f:
            f.write("="*70 + "\n")
            f.write("TỔNG HỢP BÀI VIẾT AFFILIATE - SHOPEE THÁNG 6/2026\n")
            f.write(f"Ngày tạo: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write("="*70 + "\n\n")
            
            f.write("🔗 DANH SÁCH LINK AFFILIATE:\n")
            for i, link in enumerate(self.affiliate_links, 1):
                f.write(f"  {i}. {link}\n")
            
            f.write("\n📅 CÁC CAMPAIGN CHÍNH:\n")
            for campaign in self.campaigns:
                f.write(f"  • {campaign['name']}: {campaign['date']}\n")
                f.write(f"    URL: {campaign['url']}\n")
            
            f.write("\n📌 CÁC CHỦ ĐỀ HÀNG NGÀY:\n")
            for theme in self.daily_themes[:10]:
                f.write(f"  • {theme['date']}: {theme['vietnamese']}\n")
        
        print(f"\n✅ Đã tạo file tổng hợp: ALL_AFFILIATE_POSTS_COMPLETE.txt")

def main():
    # Đường dẫn file CSV
    csv_file = "[SHOPEE]  ✨ JUNE 2026 ✨ - 1) 😀Overall-Jun.csv"
    
    if os.path.exists(csv_file):
        creator = CampaignToAffiliatePosts(csv_file)
        creator.generate_all_posts()
        
        print("\n💡 HƯỚNG DẪN:")
        print("1. Mở các file .txt vừa tạo")
        print("2. Copy nội dung để đăng lên Facebook/Telegram/Zalo")
        print("3. Thêm hình ảnh sản phẩm phù hợp với nội dung")
        print("4. Link affiliate đã được tích hợp sẵn")
    else:
        print(f"❌ Không tìm thấy file: {csv_file}")
        print("📂 Vui lòng đảm bảo file CSV ở cùng thư mục")

if __name__ == "__main__":
    main()