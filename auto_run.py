import subprocess
import sys
import time

print("🚀 TỰ ĐỘNG THÊM TASK VÀ CHẠY WORKER")
print("="*50)

# 1. Thêm task mới
print("📥 Đang thêm task...")
subprocess.run([sys.executable, "add_tasks_quick.py"])

# 2. Chạy worker để xử lý
print("\n⚙️ Đang chạy worker...")
subprocess.run([sys.executable, "worker_simple.py"])

print("\n✅ Hoàn tất!")
