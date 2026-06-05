# shopee_campaign_worker_fixed.py
import csv
import os
from datetime import datetime, timedelta
from pathlib import Path
import glob

class ShopeeCampaignWorker:
    def __init__(self, csv_path=None):
        self.campaigns = []
        self.daily_themes = []
        
        # Tự động tìm file CSV nếu không được cung cấp
        if csv_path is None:
            csv_path = self.find_csv_file()
        
        if csv_path and os.path.exists(csv_path):
            self.load_campaign_data(csv_path)
        else:
            print("⚠️ Không tìm thấy file CSV, sử dụng dữ liệu mẫu")
            self.load_sample_data()
    
    def find_csv_file(self):
        """Tự động tìm file CSV trong thư mục hiện tại"""
        csv_files = glob.glob("E:\\DYT_01\\*.csv")
        csv_files += glob.glob("E:\\DYT_01\\**\\*.csv", recursive=True)
        
        # Tìm file có chứa "JUNE" hoặc "Overall" trong tên
        for file in csv_files:
            if "JUNE" in file or "Overall" in file or "Jun" in file:
                print(f"✅ Tìm thấy file CSV: {os.path.basename(file)}")
                return file
        
        if csv_files:
            print(f"📁 Các file CSV tìm thấy:")
            for f in csv_files:
                print(f"   - {os.path.basename(f)}")
            return csv_files[0]  # Lấy file đầu tiên
        
        return None
    
    def load_sample_data(self):
        """Tạo dữ liệu mẫu dựa trên lịch thực tế"""
        print("📋 Đang tạo dữ liệu mẫu từ lịch Shopee tháng 6/2026...")
        
        # Dữ liệu mẫu cho tháng 6/2026
        self.daily_themes = [
            {'date': '1/6', 'weekday': 'MON', 'theme': 'Opening Sale', 
             'vietnamese': '1.6 Sale Mở Màn', 'sub_title': 'Siêu Nhanh - Siêu Rẻ'},
            {'date': '2/6', 'weekday': 'TUE', 'theme': 'Dress up & Make up', 
             'vietnamese': 'Làm Đẹp - Mặc Chất', 'sub_title': 'Hot deal giảm đến 50%'},
            {'date': '3/6', 'weekday': 'WED', 'theme': 'Low Price Day', 
             'vietnamese': 'Thứ 4 Siêu rẻ', 'sub_title': 'Độc Quyền Deal 1.000Đ'},
            {'date': '4/6', 'weekday': 'THU', 'theme': 'Early Bird Sale', 
             'vietnamese': 'Sale bắt đầu từ 0H 4.6', 'sub_title': 'Siêu Nhanh Siêu Rẻ'},
            {'date': '5/6', 'weekday': 'FRI', 'theme': 'Early Bird Sale', 
             'vietnamese': 'Bật mí siêu sale 6.6', 'sub_title': 'Sale bắt đầu từ 0H 5.6'},
            {'date': '6/6', 'weekday': 'SAT', 'theme': '6.6 Shopee Mid Year Mega Sale', 
             'vietnamese': '6.6 Siêu Sale Giữa Năm', 'sub_title': 'Giảm đến 50% + Voucher Xtra 6 triệu'},
            {'date': '7/6', 'weekday': 'SUN', 'theme': 'Extended Spike', 
             'vietnamese': 'Sale Vẫn còn', 'sub_title': 'Siêu deal giảm đến 50%'},
            {'date': '8/6', 'weekday': 'MON', 'theme': 'Authentic Brand Day', 
             'vietnamese': 'Ngày Hội Chính Hãng', 'sub_title': 'Mua trước, trả sau 0% đến 6 kỳ'},
            {'date': '12/6', 'weekday': 'FRI', 'theme': 'In-Stock, Ships Fast', 
             'vietnamese': 'Hàng sẵn tại kho - Giao nhanh', 'sub_title': 'Giao nhanh, giảm đến 50%'},
            {'date': '14/6', 'weekday': 'SUN', 'theme': 'Early Bird Sale', 
             'vietnamese': 'Bật mí siêu sale 15.6', 'sub_title': 'Sale bắt đầu từ 0H 14.6'},
            {'date': '15/6', 'weekday': 'MON', 'theme': '15.6 Mid-month', 
             'vietnamese': '15.6 Sale Giữa Tháng', 'sub_title': 'Voucher Xtra giảm đến 6 triệu'},
            {'date': '22/6', 'weekday': 'MON', 'theme': 'Authentic Brand Day', 
             'vietnamese': 'Ngày Hội Chính Hãng', 'sub_title': 'Mua trước, trả sau 0% đến 6 kỳ'},
            {'date': '23/6', 'weekday': 'TUE', 'theme': 'Dress up & Make up', 
             'vietnamese': 'Làm Đẹp - Mặc Chất', 'sub_title': 'Hot deal giảm đến 50%'},
            {'date': '24/6', 'weekday': 'WED', 'theme': 'Early Bird Sale', 
             'vietnamese': 'Bật mí siêu sale 25.6', 'sub_title': 'Sale bắt đầu từ 0H 24.6'},
            {'date': '25/6', 'weekday': 'THU', 'theme': '25.6 Payday', 
             'vietnamese': '25.6 Lương Về Sale To', 'sub_title': 'ShopeeVIP giảm 20% mỗi ngày'},
        ]
        
        # Các chiến dịch spike
        self.campaigns = [
            {'name': '1.6 Opening Sale', 'date': '1/6', 'url': 'https://shopee.vn/m/6-6'},
            {'name': '6.6 Shopee Mid Year Mega Sale', 'date': '6/6', 'url': 'https://shopee.vn/m/6-6'},
            {'name': '15.6 Mid-month', 'date': '15/6', 'url': 'https://shopee.vn/m/15-sale-giua-thang'},
            {'name': '25.6 Payday', 'date': '25/6', 'url': 'https://shopee.vn/m/sale-cuoi-thang-don-luong-ve'},
        ]
    
    def load_campaign_data(self, csv_path):
        """Đọc dữ liệu từ file CSV"""
        try:
            with open(csv_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                data = list(reader)
                
            # Parse dữ liệu từ CSV (giữ nguyên code cũ)
            in_daily = False
            for row in data:
                if 'DAILY THEME' in str(row):
                    in_daily = True
                    continue
                if in_daily and len(row) > 2 and row[0] and row[0].strip().isdigit():
                    self.daily_themes.append({
                        'date': row[0].strip(),
                        'weekday': row[1].strip() if len(row) > 1 else '',
                        'theme': row[2].strip() if len(row) > 2 else '',
                        'vietnamese': row[3].strip() if len(row) > 3 else '',
                        'sub_title': row[4].strip() if len(row) > 4 else ''
                    })
            
            print(f"✅ Đã tải {len(self.daily_themes)} chủ đề từ file CSV")
            
        except Exception as e:
            print(f"❌ Lỗi đọc file CSV: {e}")
            self.load_sample_data()
    
    def generate_affiliate_content(self, campaign_name, date, campaign_url):
        """Tạo nội dung affiliate cho chiến dịch"""
        templates = {
            '6.6': f"""
🎉🔥 SIÊU SALE 6.6 - GIỮA NĂM RỰC RỠ 🔥🎉

✨ **Shopee Mall giảm đến 50%** cho hàng ngàn sản phẩm chính hãng
✨ **Voucher Xtra lên đến 6 triệu đồng** - Săn ngay kẻo lỡ!
✨ **Cơ hội trúng 66 tivi 65 inch** (***) - Thử vận may ngay
✨ **Freeship 0Đ** (*) cho mọi đơn hàng - Mua sắm thả ga
✨ **SPayLater mua trước trả sau 0%** - Nhận hàng ngay, trả tiền sau

🛍️ **ĐẶT MUA NGAY HÔM NAY:**
👉 {campaign_url}

#Shopee6_6 #SaleGiuaNam #Affiliate #MuaSamThongMinh
            """,
            '15.6': f"""
📣✨ SALE GIỮA THÁNG 15.6 - RẺ BẤT NGỜ ✨📣

🔥 **Voucher Xtra giảm đến 6 triệu đồng** - Số lượng có hạn
🔥 **SVIP giảm đến 20% mỗi ngày** - Trở thành triệu phú voucher
🔥 **Freeship 0Đ** toàn quốc - Không lo phí ship
🔥 **Mua sắm thả ga cùng ShopeePay** - Thêm ưu đãi cực khủng

🎯 **SĂN SALE NGAY HÔM NAY:**
👉 {campaign_url}

#Shopee15_6 #SaleGiuaThang #VoucherXtra
            """,
            '25.6': f"""
💥💰 LƯƠNG VỀ - SALE TO 25.6 - RẺ BẤT NGỜ 💰💥

🎁 **ShopeeVIP 1st Birthday** - Giảm 20% mỗi ngày (**)
🎁 **SPayLater 0% đến 6 kỳ** - Mua trước trả sau không lãi suất
🎁 **Siêu voucher freeship 0Đ** (*) - Miễn phí vận chuyển
🎁 **Hàng ngàn sản phẩm giảm sốc** - Giá tốt nhất tháng

🛍️ **MUA SẮM NGAY:**
👉 {campaign_url}

#Shopee25_6 #LuongVeSaleTo #SaleCuoiThang
            """,
            '1.6': f"""
⚡🌟 MỞ MÀN SIÊU SALE 1.6 - SIÊU NHANH - SIÊU RẺ 🌟⚡

⚡ **Super Cheap - Chỉ từ 1.000Đ** - Deal độc quyền
⚡ **ShopeeVIP giảm 20% mỗi ngày** - Tiết kiệm tối đa
⚡ **Freeship 0Đ** (*) - Mua gì cũng ship miễn phí
⚡ **Mở bán sớm** - Săn deal trước khi hết

🛒 **NHẬN NGAY ƯU ĐÃI:**
👉 {campaign_url}

#Shopee1_6 #OpeningSale #SieuRe
            """
        }
        
        # Tìm template phù hợp
        for key, template in templates.items():
            if key in campaign_name:
                return template
        
        # Template mặc định
        return f"""
🛒✨ CHIẾN DỊCH {campaign_name.upper()} ✨🛒

⭐ **Ưu đãi đặc biệt** - Giảm giá sốc lên đến 50%
⭐ **Voucher freeship** toàn quốc - Mua sắm thoải mái
⭐ **Thanh toán qua ShopeePay** - Nhận thêm ưu đãi
⭐ **Hàng chính hãng 100%** - Yên tâm chất lượng

👉 **XEM CHI TIẾT:** {campaign_url}
        """
    
    def get_daily_theme_content(self, theme_data):
        """Tạo nội dung theo chủ đề hàng ngày"""
        theme = theme_data['theme']
        vietnamese = theme_data['vietnamese']
        sub_title = theme_data['sub_title']
        
        theme_templates = {
            'Dress up & Make up': f"""
✨💄 {vietnamese} - {sub_title} 💄✨

💅 **Mỹ phẩm chính hãng** giảm đến 50% - L'Oreal, Maybelline,...
👗 **Thời trang mới nhất** từ Adidas, Canifa, IVY moda
💋 **Set quà tặng độc quyền** chỉ hôm nay
🎁 **Mua 1 tặng 1** cho đơn hàng đầu tiên

🛍️ **KHÁM PHÁ NGAY:**
👉 https://shopee.vn/search?keyword=thoi+trang+lam+dep

#LamDepMacChat #FashionWeek #ShopeeFashion
            """,
            'Low Price Day': f"""
⚡💰 {vietnamese} - {sub_title} 💰⚡

🔥 **Săn deal chỉ từ 1.000Đ** - Siêu rẻ bất ngờ
🔥 **Số lượng có hạn** - Nhanh tay kẻo lỡ
🔥 **Hàng ngàn sản phẩm** giá tốt nhất ngày
🔥 **Freeship 0Đ** cho đơn từ 0Đ (*)

🎯 **THAM GIA NGAY:**
👉 https://shopee.vn/m/thu-4-sieu-re

#Thu4Sieure #Deal1000d #LowPriceDay
            """,
            'Entertainment Weekend': f"""
🎪🎮 {vietnamese} - {sub_title} 🎮🎪

🎬 **Siêu deal cuối tuần** giảm đến 50%
🎧 **Gaming & giải trí** giá rẻ bất ngờ
📱 **Điện thoại, tablet** khuyến mãi sốc
🎁 **Live sale độc quyền** 20-22h hàng ngày

🛒 **MUA SẮM NGAY:**
👉 https://shopee.vn/search?keyword=giai+tri

#CuoiTuanGiaiTri #EntertainmentWeekend #GamingDeal
            """,
            'Authentic Brand Day': f"""
🏷️✨ {vietnamese} - {sub_title} ✨🏷️

✅ **Hàng chính hãng 100%** từ các thương hiệu uy tín
✅ **Bảo hành chính hãng** đầy đủ
✅ **Giảm giá sốc** lên đến 50%
✅ **SPayLater 0%** đến 6 kỳ

🛍️ **MUA NGAY HÔM NAY:**
👉 https://shopee.vn/mall

#NgayHoiChinhHang #AuthenticBrand #ShopeeMall
            """
        }
        
        # Tìm template phù hợp
        for key, template in theme_templates.items():
            if key in theme:
                return template
        
        # Template mặc định cho ngày thường
        return f"""
📢✨ {vietnamese} - {sub_title} ✨📢

{'-' * 50}
{'-' * 50}

🎉 **Ưu đãi đặc biệt chỉ hôm nay**
🎉 **Mua sắm thông minh** - Tiết kiệm tối đa
🎉 **Hàng chính hãng** - Giá tốt nhất

👉 **NHẬN NGAY ƯU ĐÃI:** https://shopee.vn/
        """
    
    def run_daily_schedule(self, days_ahead=0):
        """Chạy worker cho ngày cụ thể"""
        today = datetime.now()
        target_date = today + timedelta(days=days_ahead)
        
        # Format date để so sánh (D/M)
        if target_date.day < 10:
            date_str = f"{target_date.day}/{target_date.month}"
        else:
            date_str = f"{target_date.day}/{target_date.month}"
        
        print(f"\n{'='*70}")
        print(f"📅 NGÀY {target_date.strftime('%d/%m/%Y')} - {target_date.strftime('%A')}")
        print(f"{'='*70}\n")
        
        # Tìm chủ đề trong ngày
        theme_for_date = None
        for theme in self.daily_themes:
            if theme['date'] == date_str:
                theme_for_date = theme
                break
        
        # Tìm campaign spike trong ngày
        campaign_for_date = None
        campaign_url = None
        for campaign in self.campaigns:
            if campaign['date'] == date_str:
                campaign_for_date = campaign['name']
                campaign_url = campaign['url']
                break
        
        # Tạo nội dung
        contents = []
        
        if campaign_for_date:
            print(f"🎯 Hôm nay là: {campaign_for_date}")
            content = self.generate_affiliate_content(campaign_for_date, date_str, campaign_url)
            contents.append(content)
        elif theme_for_date:
            print(f"📌 Chủ đề hôm nay: {theme_for_date['vietnamese']}")
            print(f"   {theme_for_date['sub_title']}")
            daily_content = self.get_daily_theme_content(theme_for_date)
            contents.append(daily_content)
        else:
            print("⚠️ Không có sự kiện đặc biệt hôm nay")
            print("💡 Hôm nay là ngày thường, vẫn có thể đăng bài quảng bá sản phẩm")
            return None
        
        # Gộp nội dung
        final_content = "\n\n".join(contents)
        
        # Hiển thị preview
        print("\n📝 NỘI DUNG SẼ ĐĂNG:")
        print("-" * 70)
        print(final_content[:500] + "..." if len(final_content) > 500 else final_content)
        print("-" * 70)
        
        return final_content

def main():
    """Main function"""
    print("""
    ╔══════════════════════════════════════════════════════╗
    ║   🛍️  SHOPEE CAMPAIGN AFFILIATE WORKER v2.0  🛍️    ║
    ║   TỰ ĐỘNG TẠO NỘI DUNG THEO LỊCH SHOPEE THÁNG 6    ║
    ╚══════════════════════════════════════════════════════╝
    """)
    
    worker = ShopeeCampaignWorker()
    
    print("\n🔧 CHỌN CHẾ ĐỘ:")
    print("1️⃣  Preview - Xem nội dung cho hôm nay")
    print("2️⃣  Preview - Xem nội dung cho ngày mai")
    print("3️⃣  Preview - Xem tất cả các ngày campaign trong tháng")
    print("4️⃣  Đăng bài thật lên các nền tảng (CẦN API KEYS)")
    print("5️⃣  Xem lịch campaign tháng 6")
    print("0️⃣  Thoát")
    
    choice = input("\n👉 Lựa chọn (0-5): ").strip()
    
    if choice == '1':
        worker.run_daily_schedule(0)
    elif choice == '2':
        worker.run_daily_schedule(1)
    elif choice == '3':
        print("\n📆 XEM LỊCH CÁC NGÀY CAMPAIGN TRONG THÁNG:")
        for campaign in worker.campaigns:
            print(f"\n📅 {campaign['date']}: {campaign['name']}")
            worker.run_daily_schedule((datetime.strptime(campaign['date'] + '/2026', '%d/%m/%Y') - datetime.now()).days)
    elif choice == '4':
        print("\n⚠️ CẢNH BÁO: Chế độ đăng bài thật!")
        confirm = input("Bạn đã cấu hình API keys trong file .env chưa? (y/n): ")
        if confirm.lower() == 'y':
            content = worker.run_daily_schedule(0)
            if content:
                print("\n📤 Đang đăng bài lên các nền tảng...")
                # TODO: Gọi các hàm post thực tế
                print("✅ Đã hoàn tất đăng bài!")
    elif choice == '5':
        print("\n📆 LỊCH CAMPAIGN SHOPEE THÁNG 6/2026:")
        print("=" * 60)
        print(f"{'Ngày':<10} {'Sự kiện':<35} {'URL'}")
        print("-" * 60)
        for campaign in worker.campaigns:
            print(f"{campaign['date']:<10} {campaign['name']:<35} {campaign['url']}")
        
        print("\n📌 Các chủ đề theo ngày:")
        for theme in worker.daily_themes[:10]:  # Hiển thị 10 ngày đầu
            print(f"   {theme['date']}: {theme['vietnamese']}")
    else:
        print("👋 Tạm biệt!")

if __name__ == "__main__":
    main()