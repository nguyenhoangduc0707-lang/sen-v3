"""
Auto post Lazada products to AccessTrade
"""
import sqlite3
import csv
import json
from datetime import datetime

def upload_to_accesstrade():
    print("=" * 60)
    print("🚀 Preparing products for AccessTrade")
    print("=" * 60)
    
    # Đọc dữ liệu từ database trực tiếp
    conn = sqlite3.connect('sen_v3.db')
    cursor = conn.cursor()
    
    # Lấy sản phẩm từ database
    cursor.execute('''
        SELECT sku, name, price, url, affiliate_link, fetched_at 
        FROM lazada_products 
        ORDER BY fetched_at DESC
    ''')
    
    products = cursor.fetchall()
    conn.close()
    
    if not products:
        print("❌ No products found in database!")
        return
    
    print(f"\n📦 Found {len(products)} products to prepare\n")
    
    # Hiển thị danh sách
    for idx, product in enumerate(products, 1):
        sku, name, price, url, aff_link, fetched_at = product
        print(f"{idx}. {name[:60] if name else 'N/A'}")
        print(f"   SKU: {sku}")
        print(f"   Link: {aff_link}")
        print()
    
    # Tạo file CSV cho AccessTrade (đúng format)
    csv_file = 'ready_for_accesstrade.csv'
    with open(csv_file, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        # Header theo format AccessTrade mong đợi
        writer.writerow(['Product Name', 'Affiliate Link', 'Price', 'SKU', 'Original URL'])
        
        for product in products:
            sku, name, price, url, aff_link, fetched_at = product
            writer.writerow([
                name if name else 'N/A',
                aff_link,
                price if price else 'Contact for price',
                sku,
                url
            ])
    
    print(f"✅ Created {csv_file} - Ready to upload to AccessTrade")
    
    # Tạo file JSON cho reference
    json_file = 'products_for_accesstrade.json'
    products_list = []
    for product in products:
        sku, name, price, url, aff_link, fetched_at = product
        products_list.append({
            'sku': sku,
            'name': name,
            'price': price,
            'original_url': url,
            'affiliate_link': aff_link,
            'fetched_at': fetched_at,
            'status': 'ready_for_accesstrade'
        })
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(products_list, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Created {json_file}")
    
    # Tạo hướng dẫn upload
    print("\n" + "=" * 60)
    print("📋 UPLOAD INSTRUCTIONS:")
    print("=" * 60)
    print("\n1. Go to https://accesstrade.vn")
    print("2. Log in to your account")
    print("3. Navigate to 'Campaigns' → 'Import Products'")
    print(f"4. Upload file: {csv_file}")
    print("5. Map the columns:")
    print("   - 'Product Name' → Tên sản phẩm")
    print("   - 'Affiliate Link' → Link tiếp thị")
    print("   - 'Price' → Giá")
    print("   - 'SKU' → Mã sản phẩm")
    print("6. Complete the import process")
    print("\n✅ Your products are now ready to be promoted on AccessTrade!")
    print("=" * 60)
    
    # Tạo báo cáo
    report = {
        'exported_at': datetime.now().isoformat(),
        'total_products': len(products_list),
        'products': products_list,
        'status': 'ready_for_upload',
        'next_steps': [
            'Upload CSV to AccessTrade dashboard',
            'Create campaigns for each product',
            'Share affiliate links on social media',
            'Track orders and commissions'
        ]
    }
    
    with open('upload_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Created upload_report.json")
    
    # Hiển thị thống kê nhanh
    print("\n📊 QUICK STATS:")
    print(f"   Total products: {len(products_list)}")
    print(f"   CSV file: {csv_file}")
    print(f"   JSON file: {json_file}")
    print(f"   Report file: upload_report.json")

if __name__ == "__main__":
    upload_to_accesstrade()
