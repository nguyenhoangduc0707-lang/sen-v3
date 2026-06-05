import os
import sqlite3

DB_PATH = "sen_v3.db"


def check_database():
    if not os.path.exists(DB_PATH):
        print(f"[LỖI] Không tìm thấy file {DB_PATH}.")
        return

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"Các bảng hiện có trong DB: {tables}")

        # SỬA Ở ĐÂY: đổi 'tasks' thành 'assigned_tasks'
        if ("assigned_tasks",) in tables:
            cursor.execute("SELECT * FROM assigned_tasks")
            rows = cursor.fetchall()
            print(f"Số lượng task đang có trong 'assigned_tasks': {len(rows)}")
            for row in rows:
                print(f" - ID: {row[0]}, Status: {row[4]}, URL: {row[3]}")
        else:
            print("[CẢNH BÁO] Không tìm thấy bảng 'assigned_tasks'!")

        conn.close()
    except Exception as e:
        print(f"[LỖI] {e}")


if __name__ == "__main__":
    check_database()
