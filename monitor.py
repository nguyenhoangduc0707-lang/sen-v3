import sqlite3
import time
import os
import sys
from datetime import datetime

def clear_screen():
    """Xóa màn hình (tùy hệ điều hành)"""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_stats():
    """Lấy thống kê từ database"""
    conn = sqlite3.connect('sen_v3.db')
    cursor = conn.cursor()
    
    # Đếm tasks theo trạng thái
    cursor.execute("SELECT status, COUNT(*) FROM tasks GROUP BY status")
    status_counts = dict(cursor.fetchall())
    
    # Tổng số tasks
    cursor.execute("SELECT COUNT(*) FROM tasks")
    total = cursor.fetchone()[0]
    
    # Lấy 5 task gần nhất
    cursor.execute("""
        SELECT id, title, status, created_at 
        FROM tasks 
        ORDER BY id DESC 
        LIMIT 5
    """)
    recent_tasks = cursor.fetchall()
    
    # Kiểm tra workers
    cursor.execute("SELECT name, status, last_heartbeat FROM workers")
    workers = cursor.fetchall()
    
    conn.close()
    
    return {
        'total': total,
        'status_counts': status_counts,
        'recent_tasks': recent_tasks,
        'workers': workers
    }

def display_stats(stats):
    """Hiển thị thống kê"""
    clear_screen()
    
    print("=" * 60)
    print("📊 DYT_01 MONITOR - GIÁM SÁT HỆ THỐNG")
    print("=" * 60)
    print(f"🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 60)
    
    # Tổng quan
    print(f"\n📋 TỔNG SỐ TASKS: {stats['total']}")
    print("-" * 40)
    
    # Phân bổ trạng thái
    status_labels = {
        'PENDING': '⏳ PENDING',
        'PROCESSING': '🔄 PROCESSING',
        'COMPLETED': '✅ COMPLETED',
        'FAILED': '❌ FAILED',
        'RUNNING': '⚡ RUNNING'
    }
    
    for status, label in status_labels.items():
        count = stats['status_counts'].get(status, 0)
        pct = (count / stats['total'] * 100) if stats['total'] > 0 else 0
        bar = '█' * int(pct / 2) if pct > 0 else ''
        print(f"  {label}: {count:3d} ({pct:4.1f}%) {bar}")
    
    # Workers
    print("\n👷 WORKERS:")
    for worker in stats['workers']:
        name, status, heartbeat = worker
        icon = '🟢' if status == 'ACTIVE' else '🔴'
        print(f"  {icon} {name}: {status} (last: {heartbeat[:16] if heartbeat else 'N/A'})")
    
    # Recent tasks
    print("\n📋 5 TASKS GẦN NHẤT:")
    for task in stats['recent_tasks']:
        task_id, title, status, created = task
        status_icon = {
            'PENDING': '⏳',
            'PROCESSING': '🔄',
            'COMPLETED': '✅',
            'FAILED': '❌',
            'RUNNING': '⚡'
        }.get(status, '❓')
        print(f"  {status_icon} Task {task_id}: {title[:35]:<35} ({status}) - {created[:16]}")
    
    print("\n" + "-" * 60)
    print("🔄 Tự động refresh sau 5 giây... (Nhấn Ctrl+C để thoát)")

def main():
    """Vòng lặp chính"""
    try:
        while True:
            stats = get_stats()
            display_stats(stats)
            time.sleep(5)
    except KeyboardInterrupt:
        print("\n\n👋 Đã dừng giám sát!")
        sys.exit(0)

if __name__ == "__main__":
    main()
