# run_production_workers.py
import subprocess
import os
import sys
from datetime import datetime
import time

def run_real_workers():
    """Chạy tất cả worker với API thật"""
    
    workers = [
        ("Shopee Campaign Worker", "shopee_campaign_worker.py"),
        ("Real Affiliate Worker", "real_affiliate_worker.py"),
        ("Auto Worker Improved", "auto_worker_improved.py"),
        ("Content Worker", "content_worker.py"),
    ]
    
    print(f"""
    ╔════════════════════════════════════════════════╗
    ║   🚀 PRODUCTION WORKERS - REAL API MODE 🚀    ║
    ║   {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}      ║
    ╚════════════════════════════════════════════════╝
    """)
    
    # Kiểm tra file .env
    if not os.path.exists(".env"):
        print("❌ ERROR: File .env không tồn tại!")
        print("Vui lòng copy .env.example và cấu hình API keys thật")
        return
    
    processes = []
    
    for name, script in workers:
        if os.path.exists(script):
            print(f"🟢 Đang khởi động: {name}")
            process = subprocess.Popen(
                [sys.executable, script],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            processes.append((name, process))
            time.sleep(2)
        else:
            print(f"🔴 Không tìm thấy: {script}")
    
    print(f"\n✅ Đã khởi động {len(processes)} workers")
    print("\n📊 Workers đang chạy:")
    for name, proc in processes:
        print(f"   • {name} (PID: {proc.pid})")
    
    print("\n💡 Nhấn Ctrl+C để dừng tất cả workers\n")
    
    try:
        while True:
            time.sleep(10)
            # Kiểm tra health check
            for name, proc in processes:
                if proc.poll() is not None:
                    print(f"⚠️ Worker {name} đã dừng!")
    except KeyboardInterrupt:
        print("\n🛑 Đang dừng tất cả workers...")
        for name, proc in processes:
            proc.terminate()
        print("✅ Đã dừng toàn bộ workers")

if __name__ == "__main__":
    run_real_workers()