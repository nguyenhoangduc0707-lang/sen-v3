import sqlite3
import os
import sys
from datetime import datetime

sys.path.insert(0, os.getcwd())

def add_accesstrade_tasks():
    conn = sqlite3.connect('sen_v3.db')
    cursor = conn.cursor()
    
    print("📥 THÊM TASK TỪ ACCESSTRADE")
    print("="*40)
    
    # Số task mới
    print("Chọn loại task:")
    print("1. Facebook content (3 tasks)")
    print("2. Motivational content (3 tasks)")
    print("3. Affiliate content (3 tasks)")
    print("4. Tất cả (9 tasks)")
    
    choice = input("Chọn (1-4): ").strip()
    
    task_types = {
        '1': ['content_facebook'] * 3,
        '2': ['scheduled_motivational'] * 3,
        '3': ['scheduled_affiliate'] * 3,
        '4': ['content_facebook', 'scheduled_motivational', 'scheduled_affiliate'] * 3
    }
    
    titles = {
        'content_facebook': [
            "Facebook content về AI Marketing",
            "Facebook post về ChatGPT",
            "Facebook content về Affiliate Marketing"
        ],
        'scheduled_motivational': [
            "Bài đăng truyền động lực sáng",
            "Lời khuyên tích cực cho ngày mới",
            "Thông điệp cảm hứng cuối tuần"
        ],
        'scheduled_affiliate': [
            "Giới thiệu sản phẩm hot tháng",
            "Review sản phẩm bán chạy",
            "Ưu đãi đặc biệt cho thành viên"
        ]
    }
    
    tasks = []
    for task_type in task_types.get(choice, []):
        # Lấy title theo thứ tự
        title_list = titles.get(task_type, ['Task'])
        title = title_list[len(tasks) % len(title_list)]
        tasks.append((title, task_type))
    
    if not tasks:
        print("❌ Lựa chọn không hợp lệ")
        return
    
    # Thêm task
    count = 0
    for title, task_type in tasks[:9]:
        cursor.execute("""
            INSERT INTO tasks (title, description, task_type, status, priority, created_at)
            VALUES (?, 'Task tự động tạo', ?, 'PENDING', 1, CURRENT_TIMESTAMP)
        """, (title, task_type))
        count += 1
    
    conn.commit()
    conn.close()
    print(f"✅ Đã thêm {count} task mới!")

if __name__ == "__main__":
    add_accesstrade_tasks()
