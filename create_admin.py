import sqlite3
import bcrypt
from datetime import datetime

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

# Tạo password hash
password = 'admin123'
hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# Xóa user cũ nếu có
cursor.execute('DELETE FROM users WHERE email = ?', ('admin@example.com',))

# Tạo admin user
cursor.execute('''
    INSERT INTO users (
        username, email, hashed_password, full_name, role, 
        token_quota, tokens_used, is_active, created_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
''', (
    'admin', 
    'admin@example.com', 
    hashed_password, 
    'Administrator', 
    'admin', 
    10000,  # token_quota
    0,      # tokens_used
    1,      # is_active
    datetime.now()
))

conn.commit()

# Kiểm tra
cursor.execute('SELECT id, username, email, role FROM users WHERE email = ?', ('admin@example.com',))
user = cursor.fetchone()
print(f'✅ User created successfully!')
print(f'   ID: {user[0]}')
print(f'   Username: {user[1]}')
print(f'   Email: {user[2]}')
print(f'   Role: {user[3]}')
print(f'   Password: admin123')

conn.close()
