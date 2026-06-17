import sqlite3

conn = sqlite3.connect('sen_v3.db')
cursor = conn.cursor()

# Kiểm tra cấu trúc bảng dead_letters
print("🔍 CẤU TRÚC BẢNG DEAD_LETTERS")
print("="*40)

cursor.execute("PRAGMA table_info(dead_letters)")
columns = cursor.fetchall()

for col in columns:
    print(f"   {col[1]} ({col[2]})")

# Kiểm tra dữ liệu mẫu
print("\n📊 DỮ LIỆU MẪU:")
sample = cursor.execute("SELECT * FROM dead_letters LIMIT 2").fetchall()
for row in sample:
    print(row)

conn.close()
