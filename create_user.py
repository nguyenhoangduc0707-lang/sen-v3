import sqlite3
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Thông tin tài khoản mới
email = "nguyenhoangduc0707@gmail.com"
username = "nguyenhoangduc"
password = "0325655987Duc@@"
role = "ADMIN"  # Hoặc "MEMBER" nếu muốn quyền thấp hơn

# Mã hóa mật khẩu
hashed_password = pwd_context.hash(password)

conn = sqlite3.connect("app.db")
cursor = conn.cursor()

# Kiểm tra xem email đã tồn tại chưa
cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
existing = cursor.fetchone()

if existing:
    # Cập nhật mật khẩu nếu đã tồn tại
    cursor.execute("UPDATE users SET hashed_password = ? WHERE email = ?", (hashed_password, email))
    print(f'✅ Đã cập nhật mật khẩu cho: {email}')
else:
    # Tạo user mới
    cursor.execute("""
        INSERT INTO users (email, username, hashed_password, role, is_active)
        VALUES (?, ?, ?, ?, 1)
    """, (email, username, hashed_password, role))
    print(f'✅ Đã tạo user mới: {email}')

conn.commit()
conn.close()

print(f'   Username: {username}')
print(f'   Password: {password}')
print(f'   Role: {role}')
