import sqlite3
from datetime import datetime, timedelta

def reset_stuck_tasks():
    conn = sqlite3.connect('sen_v3.db')
    cursor = conn.cursor()
    
    print("🔄 RESET TASKS TREO")
    print("="*40)
    
    # Đếm task RUNNING quá 1 giờ
    cursor.execute("""
        SELECT COUNT(*) FROM tasks 
        WHERE status = 'RUNNING' 
        AND started_at < datetime('now', '-1 hour')
    """)
    stuck_count = cursor.fetchone()[0]
    print(f"📋 Task RUNNING quá 1 giờ: {stuck_count}")
    
    if stuck_count > 0:
        # Reset về PENDING
        cursor.execute("""
            UPDATE tasks 
            SET status = 'PENDING', 
                last_error = 'Auto-reset due to timeout',
                worker_name = NULL
            WHERE status = 'RUNNING' 
            AND started_at < datetime('now', '-1 hour')
        """)
        reset_count = cursor.rowcount
        conn.commit()
        print(f"✅ Đã reset {reset_count} tasks về PENDING")
    
    # Hiển thị tasks RUNNING hiện tại
    cursor.execute("""
        SELECT id, title, task_type, started_at 
        FROM tasks 
        WHERE status = 'RUNNING'
        ORDER BY id
    """)
    running = cursor.fetchall()
    
    if running:
        print("\n⚠️ Tasks RUNNING hiện tại:")
        for task in running:
            print(f"   - Task {task[0]}: {task[1][:40]} ({task[2]}) - {task[3]}")
    else:
        print("\n✅ Không có task RUNNING nào")
    
    conn.close()

if __name__ == "__main__":
    reset_stuck_tasks()
