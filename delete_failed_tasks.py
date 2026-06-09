import sqlite3

conn = sqlite3.connect('app.db')
c = conn.cursor()

# Xem danh sách task lỗi
c.execute('SELECT id, title, last_error FROM tasks WHERE status = \"FAILED\"')
failed = c.fetchall()

print('\n📋 FAILED TASKS TO DELETE:')
for task in failed:
    print(f'   #{task[0]}: {task[1]}')
    print(f'      Error: {task[2][:100] if task[2] else "Unknown"}')

# Xóa các task lỗi
c.execute('DELETE FROM tasks WHERE status = \"FAILED\"')
deleted_count = c.rowcount
conn.commit()

print(f'\n🗑️ Deleted {deleted_count} failed tasks')

# Kiểm tra lại
c.execute('SELECT COUNT(*) FROM tasks WHERE status = \"FAILED\"')
remaining = c.fetchone()[0]

if remaining == 0:
    print('✅ No failed tasks remaining!')
else:
    print(f'⚠️ Still {remaining} failed tasks')

conn.close()
