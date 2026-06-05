"""
CHẠY NHIỀU WORKER SONG SONG
Sử dụng multiprocessing để chạy tối đa worker
"""

import multiprocessing
import subprocess
import sys
import os
from datetime import datetime

# Danh sách worker cần chạy
WORKERS = [
    # Nhóm lấy link affiliate
    ("worker_accesstrade", "E:/DYT_01/workers/accesstrade_worker.py"),
    ("worker_shopee", "E:/DYT_01/workers/shopee_worker.py"),
    ("worker_tiki", "E:/DYT_01/workers/tiki_worker.py"),
    ("worker_lazada", "E:/DYT_01/workers/lazada_worker.py"),
    
    # Nhóm tổng hợp
    ("worker_aggregator", "E:/DYT_01/workers/affiliate_aggregator.py"),
    ("worker_content", "E:/DYT_01/workers/content_generator.py"),
    
    # Nhóm đăng bài
    ("worker_threads_1", "E:/DYT_01/workers/threads_poster.py"),
    ("worker_threads_2", "E:/DYT_01/workers/threads_poster_2.py"),
    ("worker_tiktok", "E:/DYT_01/workers/tiktok_poster.py"),
]

def run_worker(name, path):
    """Chạy một worker riêng lẻ"""
    print(f"[{datetime.now()}] 🚀 Khởi động: {name}")
    try:
        result = subprocess.run(
            [sys.executable, path],
            capture_output=True,
            text=True,
            timeout=300
        )
        print(f"[{datetime.now()}] ✅ Hoàn thành: {name}")
        return True
    except subprocess.TimeoutExpired:
        print(f"[{datetime.now()}] ⚠️ Timeout: {name}")
        return False
    except Exception as e:
        print(f"[{datetime.now()}] ❌ Lỗi {name}: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 CHẠY NHIỀU WORKER SONG SONG")
    print(f"📅 Thời gian: {datetime.now()}")
    print("=" * 60)
    
    # Chạy song song tối đa 4 worker cùng lúc
    max_parallel = 4
    with multiprocessing.Pool(processes=max_parallel) as pool:
        results = pool.starmap(run_worker, WORKERS)
    
    # Tổng kết
    success_count = sum(results)
    print("\n" + "=" * 60)
    print(f"📊 KẾT QUẢ: {success_count}/{len(WORKERS)} worker thành công")
    print("=" * 60)
