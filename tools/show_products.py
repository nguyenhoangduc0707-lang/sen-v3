import sqlite3

conn = sqlite3.connect('sen_v3.db')
cursor = conn.cursor()

# Xem bảng lazada_products
cursor.execute('SELECT sku, name, price, affiliate_link, fetched_at FROM lazada_products')
products = cursor.fetchall()

print('=' * 80)
print('📦 Products in Database:')
print('=' * 80)

for sku, name, price, aff_link, fetched_at in products:
    print(f'\n🔹 SKU: {sku}')
    name_display = name[:80] if name and len(name) > 0 else "N/A"
    print(f'   Tên: {name_display}')
    price_display = price if price else "N/A"
    print(f'   Giá: {price_display} VND')
    print(f'   Affiliate: {aff_link}')
    print(f'   Fetched: {fetched_at}')

conn.close()
print('\n' + '=' * 80)
