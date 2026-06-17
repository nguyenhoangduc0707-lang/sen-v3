"""
Top priority campaigns - Bắt đầu quảng bá ngay
"""
import sqlite3

conn = sqlite3.connect('sen_v3.db')
cursor = conn.cursor()

# Top campaigns theo category ưu tiên
top_campaigns = [
    ('Shopee', 'E-COMMERCE'),
    ('VPBank', 'FINANCIAL SERVICES'),
    ('TPBank', 'FINANCIAL SERVICES'),
    ('Lazada', 'E-COMMERCE'),
    ('Sun World', 'TRAVEL'),
    ('HDBank', 'FINANCIAL SERVICES'),
    ('Alibaba', 'E-COMMERCE'),
    ('Ding Tea', 'E-COMMERCE'),
    ('Traphaco', 'HEALTHCARE'),
]

print("=" * 70)
print("🎯 TOP CAMPAIGNS ĐỂ BẮT ĐẦU QUẢNG BÁ")
print("=" * 70)

found_count = 0
for keyword, category in top_campaigns:
    cursor.execute('''
        SELECT id, name, category 
        FROM accesstrade_campaigns 
        WHERE name LIKE ? AND category = ?
        LIMIT 1
    ''', (f'%{keyword}%', category))
    
    row = cursor.fetchone()
    if row:
        found_count += 1
        print(f"\n✅ {row[1]}")
        print(f"   📌 ID: {row[0]}")
        print(f"   📂 Category: {row[2]}")
        print(f"   🔗 Link: https://pub.accesstrade.vn/campaigns/{row[0]}")
    else:
        # Thử tìm kiếm rộng hơn
        cursor.execute('''
            SELECT id, name, category 
            FROM accesstrade_campaigns 
            WHERE name LIKE ? 
            LIMIT 1
        ''', (f'%{keyword}%',))
        row = cursor.fetchone()
        if row:
            found_count += 1
            print(f"\n✅ {row[1]}")
            print(f"   📌 ID: {row[0]}")
            print(f"   📂 Category: {row[2]}")
            print(f"   🔗 Link: https://pub.accesstrade.vn/campaigns/{row[0]}")

print("\n" + "=" * 70)
print(f"📊 Tìm thấy {found_count}/{len(top_campaigns)} campaigns")
print("\n💡 CÁCH LẤY LINK AFFILIATE:")
print("   1. Đăng nhập https://pub.accesstrade.vn")
print("   2. Vào mục 'Campaigns'")
print("   3. Tìm campaign theo ID hoặc tên")
print("   4. Nhấn 'Get Link' để lấy link tiếp thị")
print("   5. Chia sẻ link lên Facebook, Zalo, TikTok...")
print("=" * 70)

# Thống kê tổng quan
cursor.execute('''
    SELECT category, COUNT(*) 
    FROM accesstrade_campaigns 
    GROUP BY category 
    ORDER BY COUNT(*) DESC
''')

print("\n📊 THỐNG KÊ CAMPAIGNS THEO LOẠI:")
for category, count in cursor.fetchall()[:10]:
    print(f"   {category}: {count} campaigns")

conn.close()
