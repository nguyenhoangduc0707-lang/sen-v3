import sqlite3
import json

conn = sqlite3.connect('sen_v3.db')
cursor = conn.cursor()

print("🔍 KIỂM TRA FACEBOOK ACCOUNTS")
print("="*40)

# Kiểm tra bảng facebook_accounts
cursor.execute("PRAGMA table_info(facebook_accounts)")
columns = [col[1] for col in cursor.fetchall()]
print("Các cột:", columns)

# Lấy dữ liệu
cursor.execute("SELECT * FROM facebook_accounts")
accounts = cursor.fetchall()

if accounts:
    print(f"\n📊 Tìm thấy {len(accounts)} tài khoản:")
    for acc in accounts:
        print(f"   - ID: {acc[0]}")
        print(f"   - Page: {acc[2] if len(acc) > 2 else 'N/A'}")
        print(f"   - Token: {acc[4][:20] if len(acc) > 4 and acc[4] else 'None'}...")
else:
    print("\n⚠️ Không tìm thấy tài khoản Facebook trong database")
    print("   Cần thêm token Facebook vào .env hoặc database")

conn.close()
