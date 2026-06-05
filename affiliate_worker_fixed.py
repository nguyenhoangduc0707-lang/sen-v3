# affiliate_worker_fixed.py
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
        self.links = []  # Reset links
        
        # Cach 1: Doc tu file affiliate_links.txt
        try:
            if os.path.exists("affiliate_links.txt"):
                print("[*] Doc file affiliate_links.txt...")
                # Thu doc voi cac encoding khac nhau
                for encoding in ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']:
                    try:
                        with open("affiliate_links.txt", "r", encoding=encoding) as f:
                            content = f.read()
                            # Tim cac link
                            lines = content.split('\n')
                            for line in lines:
                                line = line.strip()
                                if line and 'shorten.asia' in line:
                                    # Lay link tu dong
                                    if line.startswith('http'):
                                        self.links.append(line)
                                    elif ': ' in line:
                                        link = line.split(': ')[-1]
                                        if 'shorten.asia' in link:
                                            self.links.append(link)
                            if self.links:
                                print(f"[+] Da doc duoc {len(self.links)} link")
                                break
                    except:
                        continue
        except Exception as e:
            print(f"[-] Loi doc file: {e}")
        
        # Cach 2: Link mac dinh neu khong doc duoc
        if not self.links:
            print("[*] Su dung link mac dinh")
            self.links = [
                "https://shorten.asia/3cSC6EUX",
                "https://shorten.asia/PjYek8R8",
                "https://shorten.asia/MxvRDqNg"
            ]
        
        # Hien thi danh sach link
        print(f"\nDanh sach link affiliate ({len(self.links)}):")
        for i, link in enumerate(self.links, 1):
            print(f"  {i}. {link}")
        print()
    
    def process_link(self, link):
        """Xu ly tung link affiliate"""
        print(f"  -> Dang xu ly: {link}")
        time.sleep(1)
        return True
    
    def create_posts(self):
        """Tao bai viet tu link"""
        if not self.links:
            print("[-] Khong co link de tao bai viet")
            return
        
        print(f"\n[*] Dang tao {len(self.links)} bai viet...")
        
        for i, link in enumerate(self.links, 1):
            content = f"""
========================================
AFFILIATE POST {i} - SHOPEE 6.6 MEGA SALE
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
            filename = f"affiliate_post_{i}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  [+] Da tao: {filename}")
        
        print(f"\n✅ Da tao {len(self.links)} bai viet")
    
    def check_links(self):
        """Kiem tra link"""
        if not self.links:
            print("[-] Khong co link de kiem tra")
            return
        
        print(f"\n📋 DANH SACH LINK AFFILIATE ({len(self.links)}):")
        print("=" * 60)
        for i, link in enumerate(self.links, 1):
            print(f"{i}. {link}")
        print("=" * 60)
        
        # Kiem tra tung link
        print("\n[*] Dang kiem tra link...")
        for i, link in enumerate(self.links, 1):
            if 'shorten.asia' in link:
                print(f"  {i}. OK - Link shorten hop le")
            else:
                print(f"  {i}. WARNING - Link khong dung dinh dang")
    
    def run(self):
        """Chay worker chinh"""
        print(f"\n{'='*50}")
        print(f"AFFILIATE WORKER STARTED")
        print(f"Time: {datetime.datetime.now()}")
        print(f"Links: {len(self.links)}")
        print(f"{'='*50}\n")
        
        if not self.links:
            print("[!] Khong co link affiliate de xu ly")
            return
        
        cycle = 0
        while self.running:
            try:
                cycle += 1
                print(f"[{datetime.datetime.now()}] Cycle {cycle}")
                
                for link in self.links:
                    self.process_link(link)
                
                print(f"  [+] Hoan thanh cycle {cycle}")
                time.sleep(30)
                
            except KeyboardInterrupt:
                print("\n[*] Nhan Ctrl+C, dang dung...")
                self.running = False
            except Exception as e:
                print(f"[-] Loi: {e}")
                time.sleep(10)
        
        print(f"[+] Worker da dung. Tong so cycle: {cycle}")

def main():
    worker = AffiliateWorker()
    
    print("\n" + "="*50)
    print("AFFILIATE WORKER - SHOPEE 6.6")
    print("="*50)
    print("\nCHON CHUC NANG:")
    print("1. Chay worker (xu ly link tu dong)")
    print("2. Tao bai viet tu link")
    print("3. Kiem tra link")
    print("4. Them link moi")
    
    choice = input("\nLua chon (1-4): ").strip()
    
    if choice == "1":
        worker.run()
    elif choice == "2":
        worker.create_posts()
    elif choice == "3":
        worker.check_links()
    elif choice == "4":
        new_link = input("Nhap link affiliate moi: ").strip()
        if new_link:
            with open("affiliate_links.txt", "a", encoding="utf-8") as f:
                f.write(f"\n{new_link}")
            print(f"[+] Da them link: {new_link}")
            worker.load_links()  # Reload
    else:
        print("Lua chon khong hop le")

if __name__ == "__main__":
    main()