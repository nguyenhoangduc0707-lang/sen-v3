import sqlite3
import os

db_path = 'app.db'

# Xóa database cũ nếu có
if os.path.exists(db_path):
    os.remove(db_path)
    print('✓ Removed old database')

# Tạo kết nối database mới
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Tạo bảng tasks
cursor.execute('''
    CREATE TABLE tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT,
        category TEXT,
        task_type TEXT,
        status TEXT DEFAULT 'PENDING',
        priority INTEGER DEFAULT 0,
        worker_name TEXT,
        payload TEXT,
        retries INTEGER DEFAULT 0,
        last_error TEXT,
        assigned_to_id TEXT,
        estimated_tokens INTEGER,
        actual_tokens_used INTEGER,
        expected_commission REAL,
        actual_commission REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        started_at TIMESTAMP,
        finished_at TIMESTAMP,
        completed_at TIMESTAMP,
        scheduled_at TIMESTAMP
    )
''')
print('✓ Created table: tasks')

# Tạo bảng scheduled_tasks
cursor.execute('''
    CREATE TABLE scheduled_tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id INTEGER,
        scheduled_at TIMESTAMP,
        is_processed INTEGER DEFAULT 0,
        is_active INTEGER DEFAULT 1,
        FOREIGN KEY (task_id) REFERENCES tasks (id)
    )
''')
print('✓ Created table: scheduled_tasks')

# Tạo bảng workers
cursor.execute('''
    CREATE TABLE workers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        status TEXT,
        last_heartbeat TIMESTAMP,
        current_task_id INTEGER
    )
''')
print('✓ Created table: workers')

# Tạo một số dữ liệu mẫu (tùy chọn)
cursor.execute('''
    INSERT INTO tasks (title, description, task_type, status, priority)
    VALUES ('Test Task 1', 'This is a test task', 'test', 'PENDING', 1)
''')
cursor.execute('''
    INSERT INTO tasks (title, description, task_type, status, priority)
    VALUES ('Test Task 2', 'Another test task', 'test', 'PENDING', 2)
''')
print('✓ Added sample data')

conn.commit()
conn.close()

print(f'\n✅ Database created successfully: {db_path}')
print('   Size:', os.path.getsize(db_path), 'bytes')
print('\n📋 Tables created:')
print('   - tasks')
print('   - scheduled_tasks')
print('   - workers')
