import sqlite3
conn = sqlite3.connect('sen_v3.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print(f'✅ Database OK! Số bảng: {len(tables)}')
conn.close()