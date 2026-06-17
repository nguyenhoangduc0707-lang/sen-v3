import subprocess
import time

print("🚀 KHỞI ĐỘNG WORKERS")
print("="*40)

workers = [
    "run_worker.py",
    # "run_scheduler.py",
    # "run_api.py"
]

for worker in workers:
    print(f"▶️ Đang khởi động {worker}...")
    # Chạy worker trong nền
    subprocess.Popen(["python", worker])
    time.sleep(1)

print("\n✅ Các worker đã được khởi động!")
print("📋 Kiểm tra logs trong thư mục logs/")
