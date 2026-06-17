import sqlite3
from datetime import datetime

def reset_processing_tasks():
    conn = sqlite3.connect('sen_v3.db')
    cursor = conn.cursor()
    
    print("🔄 RESET TASKS PROCESSING")
    print("="*40)
    
    # Đếm task PROCESSING
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'PROCESSING'")
    processing_count = cursor.fetchone()[0]
    print(f"📋 Tasks PROCESSING: {processing_count}")
    
    if processing_count > 0:
        # Reset về PENDING
        cursor.execute("""
            UPDATE tasks 
            SET status = 'PENDING', 
                last_error = 'Auto-reset from PROCESSING',
                worker_name = NULL,
                started_at = NULL
            WHERE status = 'PROCESSING'
        """)
        reset_count = cursor.rowcount
        conn.commit()
        print(f"✅ Đã reset {reset_count} tasks về PENDING")
    
    # Hiển thị tasks PENDING
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'PENDING'")
    pending = cursor.fetchone()[0]
    print(f"\n📋 Tasks PENDING hiện tại: {pending}")
    
    conn.close()

if __name__ == "__main__":
    reset_processing_tasks()
