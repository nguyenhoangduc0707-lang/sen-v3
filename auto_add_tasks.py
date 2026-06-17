import sqlite3
from datetime import datetime

def auto_add_tasks():
    conn = sqlite3.connect('sen_v3.db')
    cursor = conn.cursor()
    
    # Thêm task mới
    tasks = [
        ("Bài đăng Facebook sáng", "content_facebook"),
        ("Lời khuyên tích cực trưa", "scheduled_motivational"),
        ("Ưu đãi chiều tối", "scheduled_affiliate"),
    ]
    
    for title, task_type in tasks:
        cursor.execute("""
            INSERT INTO tasks (title, description, task_type, status, priority, created_at)
            VALUES (?, 'Tự động tạo từ scheduler', ?, 'PENDING', 1, CURRENT_TIMESTAMP)
        """, (title, task_type))
    
    conn.commit()
    conn.close()
    print(f"✅ Đã thêm {len(tasks)} task mới vào lúc {datetime.now().strftime('%H:%M:%S')}")

if __name__ == "__main__":
    auto_add_tasks()
