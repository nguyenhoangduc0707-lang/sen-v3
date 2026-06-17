import sqlite3
from datetime import datetime, timedelta

def cleanup_failed_tasks():
    conn = sqlite3.connect('sen_v3.db')
    cursor = conn.cursor()
    
    print("🧹 DỌN DẸP TASK FAILED")
    print("="*40)
    
    # Đếm failed tasks
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'FAILED'")
    failed_count = cursor.fetchone()[0]
    print(f"📋 Task FAILED: {failed_count}")
    
    if failed_count > 0:
        # Xem failed tasks
        cursor.execute("SELECT id, title, last_error, created_at FROM tasks WHERE status = 'FAILED'")
        tasks = cursor.fetchall()
        print("\n📋 Chi tiết:")
        for task in tasks:
            print(f"   - Task {task[0]}: {task[1][:40]} ({task[3][:16]})")
            print(f"     Lỗi: {task[2][:60]}...")
        
        # Hỏi xóa
        confirm = input("\n🔄 Xóa các task FAILED cũ (>7 ngày)? (y/n): ")
        if confirm.lower() == 'y':
            cursor.execute("""
                DELETE FROM tasks 
                WHERE status = 'FAILED' 
                AND created_at < datetime('now', '-7 days')
            """)
            deleted = cursor.rowcount
            conn.commit()
            print(f"✅ Đã xóa {deleted} task FAILED cũ")
    
    conn.close()

if __name__ == "__main__":
    cleanup_failed_tasks()
