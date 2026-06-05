# fix_workers.py
import os
import sys

print("Fixing workers...")

# Kiem tra cac file worker
workers = ["content_worker.py", "monitor_workers.py", "real_affiliate_worker.py"]

for worker in workers:
    if os.path.exists(worker):
        print(f"✓ Found: {worker}")
        
        # Doc file
        with open(worker, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Kiem tra loi pho bien
        if 'while True' not in content:
            print(f"  ⚠ {worker} co the thieu vong lap chinh")
        
        if 'time.sleep' not in content:
            print(f"  ⚠ {worker} co the bi loop vo han")
    else:
        print(f"✗ Missing: {worker}")

print("\nTao worker mau...")

# Tao worker mau chuan
with open("simple_worker.py", "w", encoding='utf-8') as f:
    f.write("""
import time
import datetime

def main():
    print(f"[{datetime.datetime.now()}] Simple worker started")
    print("Processing affiliate links...")
    
    links = [
        "https://shorten.asia/3cSC6EUX",
        "https://shorten.asia/PjYek8R8",
        "https://shorten.asia/MxvRDqNg"
    ]
    
    count = 0
    while True:
        count += 1
        print(f"[{datetime.datetime.now()}] Cycle {count}")
        
        for link in links:
            print(f"  -> {link}")
            # TODO: Add your logic here
            
        time.sleep(30)

if __name__ == "__main__":
    main()
""")

print("✓ Created simple_worker.py")
print("\nRun: python simple_worker.py")