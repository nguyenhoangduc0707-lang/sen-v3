import sqlite3
from datetime import datetime

print("📊 KIỂM TRA SCHEDULER")
print("="*40)

conn = sqlite3.connect('sen_v3.db')
cursor = conn.cursor()

# Kiểm tra bảng scheduled_tasks
cursor.execute("SELECT COUNT(*) FROM scheduled_tasks")
task_count = cursor.fetchone()[0]
print(f"📋 Scheduled tasks: {task_count}")

# Kiểm tra workers
cursor.execute("SELECT id, name, status, last_heartbeat FROM workers")
workers = cursor.fetchall()
print("\n👷 Workers:")
for w in workers:
    print(f"   - {w[1]}: {w[2]} (last: {w[3]})")

# Kiểm tra tasks pending
cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'PENDING'")
pending = cursor.fetchone()[0]
print(f"\n📋 Tasks PENDING: {pending}")

# Kiểm tra tasks failed
cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'FAILED'")
failed = cursor.fetchone()[0]
print(f"📋 Tasks FAILED: {failed}")

# Xem 5 task mới nhất
cursor.execute("SELECT id, title, status, created_at FROM tasks ORDER BY id DESC LIMIT 5")
recent = cursor.fetchall()
print("\n📋 5 tasks mới nhất:")
for t in recent:
    print(f"   - Task {t[0]}: {t[1][:30]}... ({t[2]}) - {t[3]}")

conn.close()
