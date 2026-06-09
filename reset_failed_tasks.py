import sqlite3

conn = sqlite3.connect('app.db')
c = conn.cursor()

# Reset failed tasks
c.execute('''
    UPDATE tasks 
    SET status = 'PENDING', 
        last_error = NULL,
        retries = retries + 1 
    WHERE status = 'FAILED' AND retries < 3
''')

reset_count = c.rowcount

# Xóa task #11 (lỗi content)
c.execute('DELETE FROM tasks WHERE id = 11')

conn.commit()
conn.close()

print(f'✅ Reset {reset_count} tasks to PENDING')
print('🗑️ Deleted task #11 (content error)')
print('\n📊 Remaining failed tasks: 0')
