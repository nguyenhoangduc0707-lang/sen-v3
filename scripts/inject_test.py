import sqlite3

try:
    conn = sqlite3.connect("sen_v3.db")
    cursor = conn.cursor()
    # Chèn task mẫu
    cursor.execute("INSERT INTO tasks (user_id, worker, url, status) VALUES (1, 'tiktok_worker', 'https://tiktok.com/test', 'pending')")
    conn.commit()
    conn.close()
    print("✅ Đã chèn task mẫu vào bảng 'tasks'!")
except Exception as e:
    print(f"❌ Lỗi: {e}")
