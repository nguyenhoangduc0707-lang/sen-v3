# auto_affiliate_poster.py
import time
import datetime
import random

class AutoAffiliatePoster:
    def __init__(self):
        self.links = []
        self.load_links()
        self.posted = []
        
    def load_links(self):
        with open("affiliate_links.txt", "r") as f:
            self.links = [line.strip() for line in f if line.strip() and 'shorten.asia' in line]
        print(f"[+] Loaded {len(self.links)} affiliate links")
    
    def create_post_content(self, link, post_number):
        """Tạo nội dung bài viết đa dạng"""
        templates = [
            f"""
🔥 SIÊU SALE 6.6 - GIẢM ĐẾN 50% 🔥

✨ Mua sắm thả ga với ưu đãi:
• Giảm giá lên đến 50%
• Freeship 0Đ toàn quốc
• Voucher Xtra 6 triệu đồng

🛍️ ĐẶT HÀNG NGAY: {link}
#Shopee6_6 #Sale
""",
            f"""
⚡⚠️ CÒN RẤT ÍT GIỜ! ⚠️⚡

SHOPEE 6.6 MEGA SALE:
- Giảm 50% toàn bộ sản phẩm
- Freeship 0Đ
- Voucher 6 triệu

👉 {link}
#FlashSale #6_6
""",
            f"""
📣 ĐÃ CÓ SIÊU SALE 6.6 📣

🎉 Ưu đãi cực khủng:
✨ Giảm đến 50%
✨ Freeship mọi đơn hàng
✨ Voucher Xtra 6 triệu
✨ Trả góp 0%

🔗 {link}
#MegaSale #Shopee6_6
"""
        ]
        return random.choice(templates)
    
    def run(self):
        print(f"\n{'='*50}")
        print("AUTO AFFILIATE POSTER STARTED")
        print(f"Time: {datetime.datetime.now()}")
        print(f"Links: {len(self.links)}")
        print(f"{'='*50}\n")
        
        post_count = 0
        while True:
            try:
                for link in self.links:
                    post_count += 1
                    content = self.create_post_content(link, post_count)
                    
                    # Lưu bài viết
                    filename = f"ready_to_post_{post_count}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(content)
                    
                    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Created: {filename}")
                    time.sleep(30)  # Chờ 30 giây giữa các bài
                    
            except KeyboardInterrupt:
                print(f"\n[*] Stopped. Total posts created: {post_count}")
                break
            except Exception as e:
                print(f"[-] Error: {e}")
                time.sleep(5)

if __name__ == "__main__":
    poster = AutoAffiliatePoster()
    poster.run()