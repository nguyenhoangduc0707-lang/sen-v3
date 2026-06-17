import subprocess
import sys

print("📥 Đang thêm task mới...")
subprocess.run([sys.executable, "add_tasks_quick.py"])
print("✅ Đã thêm task! Worker đang chạy nền sẽ tự xử lý.")
