import sqlite3

try:
    conn = sqlite3.connect('sen_v3.db')
    cursor = conn.cursor()
    
    # Lấy danh sách bảng
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    print(f"✅ Database kết nối thành công!")
    print(f"📊 Số bảng: {len(tables)}")
    print("\n📋 Danh sách bảng:")
    for table in tables[:15]:  # Hiển thị 15 bảng đầu
        print(f"   - {table[0]}")
    
    conn.close()
except Exception as e:
    print(f"❌ Lỗi: {e}")