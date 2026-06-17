# safe_cleanup.py
import os
import shutil
import datetime
from pathlib import Path

def safe_cleanup():
    # Tạo thư mục archive
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_dir = f"ARCHIVED_{timestamp}"
    os.makedirs(archive_dir, exist_ok=True)
    
    # NHÓM 1: File có thể XÓA NGAY (tạm thời)
    temp_patterns = [
        "*.db-shm", "*.db-wal", "*.pyc", "*.log", 
        "*.tmp", "security_report_*.txt"
    ]
    
    # NHÓM 2: File DUPLICATE (chuyển vào archive)
    duplicate_files = [
        "main_clean.py", "main_nodb.py", "main_simple.py", "main_standalone.py",
        "fb_auto_click.py", "fb_auto_undetected.py", "fb_auto_v2.py",
        "fb_post_quick.py", "fb_scheduler.py", "fb_selenium.py",
        "simple_post.py", "simple_post_v1.py", "simple_worker.py",
        "ai_content_task.py", "task_shopee.py", "task_with_image.py"
    ]
    
    # NHÓM 3: Report cũ
    report_patterns = ["accesstrade_report_*.xlsx", "*_report_*.txt"]
    
    print("=== DỌN DẸP AN TOÀN DỰ ÁN ===\n")
    
    # Xóa temp files
    for pattern in temp_patterns:
        for f in Path('.').glob(pattern):
            if f.is_file():
                f.unlink()
                print(f"🗑️  Đã xóa: {f.name}")
    
    # Di chuyển duplicate vào archive
    for fname in duplicate_files:
        if os.path.exists(fname):
            shutil.move(fname, os.path.join(archive_dir, fname))
            print(f"📦 Đã archive: {fname}")
    
    # Xóa báo cáo cũ
    for pattern in report_patterns:
        for f in Path('.').glob(pattern):
            f.unlink()
            print(f"🗑️  Đã xóa: {f.name}")
    
    print(f"\n✅ DỌN XONG!")
    print(f"📁 File cũ được lưu tại: {archive_dir}")
    print(f"⚠️  Sau khi kiểm tra hệ thống vẫn chạy tốt, bạn có thể xóa thư mục này")

if __name__ == "__main__":
    safe_cleanup()