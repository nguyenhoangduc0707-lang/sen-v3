import sqlite3
import os

db_path = 'app.db'

# Kết nối database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 1. Thêm cột task_type vào bảng scheduled_tasks nếu chưa có
try:
    cursor.execute('ALTER TABLE scheduled_tasks ADD COLUMN task_type TEXT')
    print('✓ Added column task_type to scheduled_tasks')
except sqlite3.OperationalError:
    print('ℹ Column task_type already exists in scheduled_tasks')

# 2. Thêm cột data vào bảng scheduled_tasks nếu chưa có
try:
    cursor.execute('ALTER TABLE scheduled_tasks ADD COLUMN data TEXT')
    print('✓ Added column data to scheduled_tasks')
except sqlite3.OperationalError:
    print('ℹ Column data already exists in scheduled_tasks')

# 3. Thêm cột priority vào bảng scheduled_tasks nếu chưa có
try:
    cursor.execute('ALTER TABLE scheduled_tasks ADD COLUMN priority INTEGER DEFAULT 0')
    print('✓ Added column priority to scheduled_tasks')
except sqlite3.OperationalError:
    print('ℹ Column priority already exists in scheduled_tasks')

# 4. Thêm cột created_by vào bảng scheduled_tasks nếu chưa có
try:
    cursor.execute('ALTER TABLE scheduled_tasks ADD COLUMN created_by TEXT')
    print('✓ Added column created_by to scheduled_tasks')
except sqlite3.OperationalError:
    print('ℹ Column created_by already exists in scheduled_tasks')

# 5. Thêm cột processed_at vào bảng scheduled_tasks nếu chưa có
try:
    cursor.execute('ALTER TABLE scheduled_tasks ADD COLUMN processed_at TIMESTAMP')
    print('✓ Added column processed_at to scheduled_tasks')
except sqlite3.OperationalError:
    print('ℹ Column processed_at already exists in scheduled_tasks')

# 6. Thêm cột created_at vào bảng scheduled_tasks nếu chưa có
try:
    cursor.execute('ALTER TABLE scheduled_tasks ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP')
    print('✓ Added column created_at to scheduled_tasks')
except sqlite3.OperationalError:
    print('ℹ Column created_at already exists in scheduled_tasks')

# 7. Thêm cột updated_at vào bảng scheduled_tasks nếu chưa có
try:
    cursor.execute('ALTER TABLE scheduled_tasks ADD COLUMN updated_at TIMESTAMP')
    print('✓ Added column updated_at to scheduled_tasks')
except sqlite3.OperationalError:
    print('ℹ Column updated_at already exists in scheduled_tasks')

# 8. Tạo bảng dead_letters
cursor.execute('''
    CREATE TABLE IF NOT EXISTS dead_letters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        original_task_id INTEGER,
        category TEXT,
        worker_name TEXT,
        payload TEXT,
        failure_reason TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
print('✓ Created table: dead_letters')

# 9. Tạo bảng task_logs (có thể cần)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS task_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id INTEGER,
        worker_name TEXT,
        action TEXT,
        message TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
print('✓ Created table: task_logs')

# 10. Xóa dữ liệu test cũ nếu có
cursor.execute('DELETE FROM tasks WHERE title LIKE "Test Task%"')
cursor.execute('DELETE FROM scheduled_tasks WHERE task_type = "test"')
print('✓ Cleaned up test data')

conn.commit()
conn.close()

print('\n✅ Database updated successfully!')
print('📋 Tables available:')
tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
for table in tables:
    print(f'   - {table[0]}')
