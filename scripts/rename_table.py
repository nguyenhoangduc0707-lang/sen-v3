import sqlite3

try:
    conn = sqlite3.connect("sen_v3.db")
    cursor = conn.cursor()
    # Đổi tên bảng
    cursor.execute("ALTER TABLE assigned_tasks RENAME TO tasks")
    conn.commit()
    conn.close()
    print("✅ Đã đổi tên bảng thành 'tasks' thành công!")
except Exception as e:
    print(f"❌ Lỗi: {e}")
