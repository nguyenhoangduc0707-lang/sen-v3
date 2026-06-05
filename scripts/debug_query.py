import sqlite3


def force_scan():
    try:
        conn = sqlite3.connect("sen_v3.db")
        cursor = conn.cursor()

        # Lấy tất cả mọi thứ trong bảng tasks, không lọc gì cả
        cursor.execute("SELECT * FROM tasks")
        rows = cursor.fetchall()

        print(f"DEBUG: Tìm thấy {len(rows)} bản ghi trong bảng 'tasks'.")
        for row in rows:
            print(f"Dữ liệu: {row}")

        conn.close()
    except Exception as e:
        print(f"LỖI: {e}")


if __name__ == "__main__":
    force_scan()
