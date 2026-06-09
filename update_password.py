import sqlite3
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Mật khẩu mới
new_password = "Admin123"
hashed_password = pwd_context.hash(new_password)

conn = sqlite3.connect("app.db")
cursor = conn.cursor()

# Cập nhật mật khẩu cho admin
cursor.execute("UPDATE users SET hashed_password = ? WHERE email = 'admin@senv3.com'", (hashed_password,))
conn.commit()

# Kiểm tra lại
cursor.execute("SELECT id, email, username, role FROM users WHERE email = 'admin@senv3.com'")
user = cursor.fetchone()
if user:
    print(f'✅ Đã cập nhật mật khẩu cho: {user[1]} ({user[2]})')
else:
    print('❌ Không tìm thấy user admin@senv3.com')

conn.close()
