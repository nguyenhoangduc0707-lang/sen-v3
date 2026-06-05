# affiliate_worker.py
import time
import datetime
import os
import json

class AffiliateWorker:
    def __init__(self):
        self.links = []
        self.load_links()
        self.running = True
        
    def load_links(self):
        """Tai link affiliate tu file"""
        try:
            # Thu doc tu file da tao
            if os.path.exists("affiliate_links.txt"):
                with open("affiliate_links.txt", "r", encoding="utf-8") as f:
                    for line in f:
                        if "https://shorten.asia" in line:
                            link = line.split(": ")[-1].strip()
                            self.links.append(link)
                print(f"[+] Da tai {len(self.links)} link affiliate")
            else:
                # Link mac dinh
                self.links = [
                    "https://shorten.asia/3cSC6EUX",
                    "https://shorten.asia/PjYek8R8",
                    "https://shorten.asia/MxvRDqNg"
                ]
                print(f"[+] Su dung {len(self.links)} link mac dinh")
        except Exception as e:
            print(f"[-] Loi tai link: {e}")
            self.links = []
    
    def process_link(self, link):
        """Xu ly tung link affiliate"""
        print(f"  -> Dang xu ly: {link}")
        # O day co the them code:
        # - Kiem tra link con hieu luc khong
        # - Lay thong tin san pham
        # - Cap nhat thong ke
        time.sleep(1)
        return True
    
    def run(self):
        """Chay worker chinh"""
        print(f"\n{'='*50}")
        print(f"AFFILIATE WORKER STARTED")
        print(f"Time: {datetime.datetime.now()}")
        print(f"Links: {len(self.links)}")
        print(f"{'='*50}\n")
        
        cycle = 0
        while self.running:
            try:
                cycle += 1
                print(f"[{datetime.datetime.now()}] Cycle {cycle}")
                
                if not self.links:
                    print("  [!] Khong co link affiliate")
                else:
                    for link in self.links:
                        self.process_link(link)
                
                print(f"  [+] Hoan thanh cycle {cycle}")
                time.sleep(30)  # Cho 30 giay giua cac cycle
                
            except KeyboardInterrupt:
                print("\n[*] Nhan Ctrl+C, dang dung...")
                self.running = False
            except Exception as e:
                print(f"[-] Loi: {e}")
                time.sleep(10)
        
        print(f"[+] Worker da dung. Tong so cycle: {cycle}")
    
    def create_post_content(self, link):
        """Tao noi dung bai viet cho link"""
        return f"""
========================================
AFFILIATE POST - SHOPEE 6.6 MEGA SALE
========================================

🔥 SIÊU SALE 6.6 - GIẢM ĐẾN 50% 🔥

✨ ƯU ĐÃI ĐẶC BIỆT:
• Giảm giá lên đến 50%
• Freeship 0Đ toàn quốc
• Voucher Xtra 6 triệu đồng
• Mua trước trả sau 0%

🛍️ ĐẶT HÀNG NGAY:
{link}

🏷️ #Shopee6_6 #MegaSale #Affiliate #Freeship
"""

def main():
    worker = AffiliateWorker()
    
    # Hoi nguoi dung muon lam gi
    print("\nCHON CHUC NANG:")
    print("1. Chay worker (xu ly link tu dong)")
    print("2. Tao bai viet tu link")
    print("3. Kiem tra link")
    
    choice = input("\nLua chon (1-3): ").strip()
    
    if choice == "1":
        worker.run()
    elif choice == "2":
        for i, link in enumerate(worker.links, 1):
            content = worker.create_post_content(link)
            filename = f"affiliate_post_{i}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Da tao: {filename}")
        print(f"\nDa tao {len(worker.links)} bai viet")
    elif choice == "3":
        print(f"\nDanh sach link affiliate ({len(worker.links)}):")
        for i, link in enumerate(worker.links, 1):
            print(f"{i}. {link}")
    else:
        print("Lua chon khong hop le")

if __name__ == "__main__":
    main()