import time
import sqlite3
from datetime import datetime

print("🔄 SCHEDULER MANUAL")
print("="*40)
print("Chạy thủ công, kiểm tra task mỗi 10 giây")
print("Nhấn Ctrl+C để dừng")

while True:
    conn = sqlite3.connect('sen_v3.db')
    cursor = conn.cursor()
    
    # Tìm tasks cần chạy
    cursor.execute("""
        SELECT id, title, task_type 
        FROM tasks 
        WHERE status = 'PENDING' 
        AND scheduled_at <= CURRENT_TIMESTAMP
        LIMIT 5
    """)
    tasks = cursor.fetchall()
    
    if tasks:
        print(f"\n📋 Tìm thấy {len(tasks)} tasks cần chạy tại {datetime.now().strftime('%H:%M:%S')}:")
        for task in tasks:
            print(f"   - Task {task[0]}: {task[1][:40]} ({task[2]})")
            # Update status
            cursor.execute("""
                UPDATE tasks 
                SET status = 'PROCESSING', 
                    started_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (task[0],))
            conn.commit()
    else:
        print(".", end="", flush=True)
    
    conn.close()
    time.sleep(10)
