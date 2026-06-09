import sqlite3

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

# Kiểm tra cột đã tồn tại chưa
cursor.execute('PRAGMA table_info(tasks)')
columns = [col[1] for col in cursor.fetchall()]

if 'scheduled_at' not in columns:
    cursor.execute('ALTER TABLE tasks ADD COLUMN scheduled_at TIMESTAMP')
    print('✅ Added column: scheduled_at')
else:
    print('ℹ️ Column scheduled_at already exists')

conn.commit()
conn.close()
print('Database updated!')
