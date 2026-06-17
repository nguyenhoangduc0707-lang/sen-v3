import sqlite3
from datetime import datetime

def add_quick_tasks():
    conn = sqlite3.connect('sen_v3.db')
    cursor = conn.cursor()
    
    print("📥 THÊM TASK NHANH")
    print("="*40)
    
    # Danh sách task mới
    tasks = [
        ("Bài đăng Facebook sáng nay", "content_facebook"),
        ("Lời khích lệ tinh thần", "scheduled_motivational"),
        ("Ưu đãi flash sale", "scheduled_affiliate"),
        ("Review sản phẩm mới", "content_facebook"),
        ("Thông điệp truyền cảm hứng", "scheduled_motivational"),
    ]
    
    count = 0
    for title, task_type in tasks:
        cursor.execute("""
            INSERT INTO tasks (title, description, task_type, status, priority, created_at)
            VALUES (?, 'Task được thêm nhanh từ script', ?, 'PENDING', 1, CURRENT_TIMESTAMP)
        """, (title, task_type))
        count += 1
    
    conn.commit()
    conn.close()
    
    print(f"✅ Đã thêm {count} task mới!")
    print("📋 Danh sách task vừa thêm:")
    for i, (title, task_type) in enumerate(tasks, 1):
        print(f"   {i}. {title} ({task_type})")

if __name__ == "__main__":
    add_quick_tasks()
