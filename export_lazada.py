"""
Export Lazada Products to CSV/JSON for AccessTrade
"""
import sqlite3
import csv
import json
from datetime import datetime

print("=" * 60)
print("📦 Exporting Lazada Products")
print("=" * 60)

# Kết nối database
conn = sqlite3.connect('sen_v3.db')
cursor = conn.cursor()

# Kiểm tra bảng lazada_products có tồn tại không
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='lazada_products'")
if not cursor.fetchone():
    print("❌ Table 'lazada_products' not found!")
    print("   Please run fetch products first.")
    conn.close()
    exit(1)

# Lấy thông tin cột trong bảng
cursor.execute("PRAGMA table_info(lazada_products)")
columns = [col[1] for col in cursor.fetchall()]
print(f"📋 Available columns: {', '.join(columns)}")

# Lấy dữ liệu (chỉ lấy các cột tồn tại)
select_columns = ['sku', 'name', 'price', 'affiliate_link', 'fetched_at']
available_select = [col for col in select_columns if col in columns]

if not available_select:
    print("❌ No valid columns found!")
    conn.close()
    exit(1)

query = f"SELECT {', '.join(available_select)} FROM lazada_products ORDER BY fetched_at DESC"
cursor.execute(query)
products = cursor.fetchall()

if not products:
    print("❌ No products found in database!")
    conn.close()
    exit(1)

print(f"\n✅ Found {len(products)} products\n")

# Hiển thị danh sách
for idx, product in enumerate(products, 1):
    # Tìm index của từng cột
    sku = product[available_select.index('sku')] if 'sku' in available_select else 'N/A'
    name = product[available_select.index('name')] if 'name' in available_select else 'N/A'
    price = product[available_select.index('price')] if 'price' in available_select else 'N/A'
    aff_link = product[available_select.index('affiliate_link')] if 'affiliate_link' in available_select else 'N/A'
    
    print(f"{idx}. {name[:60] if name else 'N/A'}")
    print(f"   SKU: {sku}")
    print(f"   Price: {price if price else 'N/A'} VND")
    print(f"   Affiliate: {aff_link}")
    print()

# Export CSV
csv_file = 'lazada_products_for_accesstrade.csv'
with open(csv_file, 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerow(available_select)
    writer.writerows(products)

print(f"✅ Exported to {csv_file}")

# Export JSON
json_file = 'lazada_products_for_accesstrade.json'
products_list = []
for product in products:
    product_dict = {}
    for idx, col in enumerate(available_select):
        product_dict[col] = product[idx]
    products_list.append(product_dict)

with open(json_file, 'w', encoding='utf-8') as f:
    json.dump(products_list, f, indent=2, ensure_ascii=False)

print(f"✅ Exported to {json_file}")

# Export HTML for easy viewing
html_file = 'lazada_products.html'
with open(html_file, 'w', encoding='utf-8') as f:
    f.write("""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Lazada Products for AccessTrade</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #4CAF50; color: white; }
            tr:nth-child(even) { background-color: #f2f2f2; }
            .aff-link { color: #2196F3; text-decoration: none; }
            .aff-link:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <h1>📦 Lazada Products for AccessTrade</h1>
        <p>Total products: """ + str(len(products_list)) + """</p>
        <p>Export date: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</p>
        <table>
            <tr>
                <th>#</th>
                <th>SKU</th>
                <th>Product Name</th>
                <th>Price (VND)</th>
                <th>Affiliate Link</th>
                <th>Fetch Date</th>
            </tr>
    """)
    
    for idx, p in enumerate(products_list, 1):
        name = p.get('name', 'N/A')[:100] if p.get('name') else 'N/A'
        price = p.get('price', 'N/A') if p.get('price') else 'N/A'
        aff_link = p.get('affiliate_link', '#')
        fetched_at = p.get('fetched_at', 'N/A')
        
        f.write(f"""
            <tr>
                <td>{idx}</td>
                <td>{p.get('sku', 'N/A')}</td>
                <td>{name}</td>
                <td>{price}</td>
                <td><a href="{aff_link}" target="_blank" class="aff-link">{aff_link[:50]}...</a></td>
                <td>{fetched_at}</td>
            </tr>
        """)
    
    f.write("""
        </table>
    </body>
    </html>
    """)

print(f"✅ Exported to {html_file}")

# Thống kê
print("\n" + "=" * 60)
print("📊 Statistics:")
print("=" * 60)
print(f"   Total products: {len(products_list)}")
print(f"   CSV file: {csv_file}")
print(f"   JSON file: {json_file}")
print(f"   HTML file: {html_file}")
print("\n💡 You can now upload these files to AccessTrade dashboard")
print("=" * 60)

conn.close()
