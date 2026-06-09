import sqlite3

conn = sqlite3.connect('app.db')
c = conn.cursor()

# Xem 2 task lỗi (dùng last_error thay vì error_msg)
c.execute('SELECT id, title, last_error FROM tasks WHERE status = \"FAILED\"')
failed = c.fetchall()

print('\n📋 FAILED TASKS:')
for task in failed:
    print(f'   #{task[0]}: {task[1]}')
    print(f'      Error: {task[2][:80] if task[2] else "Unknown"}')

# Reset các task lỗi (chạy lại 1 lần nữa)
c.execute('''
    UPDATE tasks 
    SET status = 'PENDING', 
        last_error = NULL,
        retries = retries + 1 
    WHERE status = 'FAILED' AND retries < 2
''')

reset_count = c.rowcount
conn.commit()

print(f'\n✅ Reset {reset_count} tasks to PENDING')
print('   Chúng sẽ được xử lý lại trong lần chạy tới')

conn.close()
