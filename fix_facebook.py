import sqlite3
from datetime import datetime

def fix_facebook_tasks():
    conn = sqlite3.connect('sen_v3.db')
    cursor = conn.cursor()
    
    print("🔧 FIX FACEBOOK AUTOPOSTER")
    print("="*50)
    
    # 1. Đếm dead_letters Facebook
    cursor.execute("""
        SELECT COUNT(*) FROM dead_letters 
        WHERE worker_name = 'facebook_autoposter'
    """)
    dead_count = cursor.fetchone()[0]
    print(f"📊 Dead letters Facebook: {dead_count}")
    
    # 2. Xem các task bị lỗi
    cursor.execute("""
        SELECT id, original_task_id, category, failure_reason 
        FROM dead_letters 
        WHERE worker_name = 'facebook_autoposter'
        ORDER BY id DESC LIMIT 10
    """)
    dead_tasks = cursor.fetchall()
    
    print("\n📋 Các task bị lỗi (dead_letters):")
    for task in dead_tasks:
        print(f"   - Dead {task[0]}: {task[2]} - {task[3][:50]}...")
    
    # 3. Kiểm tra tasks bị lỗi trong bảng tasks
    cursor.execute("""
        SELECT id, title, task_type, status, last_error, created_at
        FROM tasks 
        WHERE status = 'FAILED' 
        AND task_type IN ('content_facebook', 'scheduled_affiliate', 'scheduled_motivational')
        ORDER BY id DESC LIMIT 10
    """)
    failed_tasks = cursor.fetchall()
    
    print(f"\n📋 Tasks bị lỗi: {len(failed_tasks)} task")
    for task in failed_tasks:
        print(f"   - Task {task[0]}: {task[1][:40] if task[1] else 'N/A'}... ({task[2]}) - {task[3]}")
    
    # 4. Reset các task bị lỗi về PENDING (không dùng updated_at)
    print("\n🔄 Đang reset tasks...")
    cursor.execute("""
        UPDATE tasks 
        SET status = 'PENDING', 
            last_error = NULL
        WHERE status = 'FAILED' 
        AND task_type IN ('content_facebook', 'scheduled_affiliate', 'scheduled_motivational')
        AND created_at < datetime('now', '-1 days')
    """)
    reset_count = cursor.rowcount
    conn.commit()
    print(f"✅ Đã reset {reset_count} tasks về PENDING")
    
    # 5. Hiển thị tasks đã reset
    cursor.execute("""
        SELECT id, title, status, task_type 
        FROM tasks 
        WHERE task_type IN ('content_facebook', 'scheduled_affiliate', 'scheduled_motivational')
        AND status = 'PENDING'
        ORDER BY id DESC LIMIT 5
    """)
    pending_tasks = cursor.fetchall()
    
    if pending_tasks:
        print("\n📋 Tasks PENDING (đã reset):")
        for task in pending_tasks:
            print(f"   - Task {task[0]}: {task[1][:40] if task[1] else 'N/A'}... ({task[3]})")
    else:
        print("\n⚠️ Không có task nào được reset thành PENDING")
    
    conn.close()
    print("\n✅ Hoàn tất!")

if __name__ == "__main__":
    fix_facebook_tasks()
