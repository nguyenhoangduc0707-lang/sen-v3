import sqlite3

conn = sqlite3.connect('sen_v3.db')
cursor = conn.cursor()

print("🔍 CẤU TRÚC BẢNG TASKS")
print("="*40)

cursor.execute("PRAGMA table_info(tasks)")
columns = cursor.fetchall()

print("Các cột trong bảng tasks:")
for col in columns:
    print(f"   {col[1]} ({col[2]})")

# Kiểm tra task bị lỗi
print("\n📊 TASKS BỊ LỖI:")
failed_tasks = cursor.execute("""
    SELECT id, title, task_type, status, created_at, last_error 
    FROM tasks 
    WHERE status = 'FAILED' 
    LIMIT 5
""").fetchall()

for task in failed_tasks:
    print(f"   Task {task[0]}: {task[1][:40] if task[1] else 'N/A'}... ({task[2]}) - {task[3]}")

conn.close()
