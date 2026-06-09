import subprocess
import sys
import os
import time

os.chdir(r'E:\DYT_01')

print("=" * 50)
print("🚀 DYT-01 - STARTING ALL WORKERS")
print("=" * 50)

# 1. API Server (nếu chưa chạy)
print("\n[1/4] API Server already running? Keep your uvicorn terminal open.")

# 2. Facebook Worker
print("\n[2/4] Starting Facebook Worker...")
fb_process = subprocess.Popen([sys.executable, "run_facebook_sync.py"])

# 3. Affiliate Worker
print("[3/4] Starting Affiliate Worker...")
aff_process = subprocess.Popen([sys.executable, "run_affiliate_sync.py"])

# 4. Scheduler Worker
print("[4/4] Starting Scheduler Worker...")
sched_process = subprocess.Popen([sys.executable, "run_scheduler.py"])

print("\n" + "=" * 50)
print("✅ ALL WORKERS STARTED!")
print("=" * 50)
print("\n📋 Running processes:")
print(f"   Facebook Worker: PID {fb_process.pid}")
print(f"   Affiliate Worker: PID {aff_process.pid}")
print(f"   Scheduler Worker: PID {sched_process.pid}")
print("\n⚠️  Keep this window open. Press Ctrl+C to stop all workers.\n")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n🛑 Stopping all workers...")
    fb_process.terminate()
    aff_process.terminate()
    sched_process.terminate()
    print("✅ All workers stopped.")
