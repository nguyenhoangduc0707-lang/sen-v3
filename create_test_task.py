import sqlite3
from datetime import datetime, timedelta

def create_test_task():
    conn = sqlite3.connect('sen_v3.db')
    cursor = conn.cursor()
    
    print("📝 TẠO TASK MẪU")
    print("="*40)
    
    # Tạo task mẫu
    cursor.execute("""
        INSERT INTO tasks (
            title, description, task_type, status, 
            priority, created_at, scheduled_at
        ) VALUES (
            'Test Scheduler Task',
            'Task được tạo để kiểm tra scheduler',
            'content_facebook',
            'PENDING',
            1,
            CURRENT_TIMESTAMP,
            datetime('now', '+1 minute')
        )
    """)
    
    task_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    print(f"✅ Đã tạo task ID: {task_id}")
    print(f"📅 Lên lịch chạy sau 1 phút")
    print("💡 Kiểm tra logs sau 1-2 phút")

if __name__ == "__main__":
    create_test_task()
