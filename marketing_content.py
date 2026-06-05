"""
Generate marketing content for each link
"""
import sqlite3

conn = sqlite3.connect('sen_v3.db')
cursor = conn.cursor()

cursor.execute("SELECT id, name FROM accesstrade_campaigns WHERE category IN ('FINANCIAL SERVICES', '60', '35')")

rows = cursor.fetchall()

print("=" * 80)
print("📢 NỘI DUNG MARKETING CHO TỪNG LINK")
print("=" * 80)

publisher_id = "6983938396644077046"

for row in rows:
    campaign_id = row[0]
    name = row[1] if row[1] else "N/A"
    link = f"https://go.isclix.com/deep_link/v5/{publisher_id}/{campaign_id}?sub4=sen_v3"
    
    print(f"\n📌 {name}")
    print(f"   Link: {link}")
    print(f"   Nội dung mẫu:")
    
    if "Vay" in name or "VPBank" in name or "TPBank" in name:
        print(f"   '💰 {name} - Vay tín chấp lên đến 500 triệu\n   ✅ Thủ tục đơn giản, giải ngân nhanh\n   👉 Đăng ký ngay: {link}'")
    elif "Thẻ" in name or "SenID" in name:
        print(f"   '💳 {name} - Mở thẻ online, nhận thẻ trong 3 ngày\n   ✅ Hoàn tiền đến 5%\n   👉 Đăng ký ngay: {link}'")
    elif "Chứng khoán" in name:
        print(f"   '📈 {name} - Đầu tư chứng khoán dễ dàng\n   ✅ Mở tài khoản miễn phí\n   👉 Đăng ký ngay: {link}'")
    else:
        print(f"   '🎯 {name} - Ưu đãi đặc biệt\n   👉 Đăng ký ngay: {link}'")
    print()

conn.close()
