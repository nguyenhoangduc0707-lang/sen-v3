import sqlite3

conn = sqlite3.connect('sen_v3.db')
cursor = conn.cursor()

print("📋 LOG MỚI NHẤT")
print("="*40)

# Lấy log mới nhất
logs = cursor.execute("""
    SELECT id, task_id, worker_name, log_level, message, created_at
    FROM execution_logs
    ORDER BY id DESC
    LIMIT 10
""").fetchall()

for log in logs:
    print(f"[{log[5]}] {log[2]}: {log[4][:80]}")
    print()

conn.close()
