"""
Convert products from database to Lazada upload format
"""
import sqlite3
import csv
import json
from datetime import datetime

def convert_to_lazada_format():
    print("=" * 60)
    print("📦 Converting products to Lazada upload format")
    print("=" * 60)
    
    # Kết nối database
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
    
    # Tạo file CSV theo format Lazada
    csv_file = 'lazada_upload_template.csv'
    
    with open(csv_file, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        
        # Header theo yêu cầu của Lazada
        headers = [
            'Group No', 'Danh mục ngành hàng', 'Tên sản phẩm', 'Tên sản phẩm trong EN',
            'Ảnh sản phẩm1', 'Ảnh sản phẩm2', 'Ảnh sản phẩm3', 'Ảnh sản phẩm4',
            'Ảnh sản phẩm5', 'Ảnh sản phẩm6', 'Ảnh sản phẩm7', 'Ảnh sản phẩm8',
            'Thương hiệu', 'Mô tả chính', 'Hàng hóa nguy hiểm',
            'Variation Name1', 'Option for Variation1', 'Image per Variation',
            'Variation Name2', 'Option for Variation2', 'Giá', 'SellerSku',
            'Số lượng', 'Khối lượng gói hàng (kg)', 'Chiều rộng gói hàng (cm)',
            'Chiều dài gói hàng (cm)', 'Chiều cao gói hàng (cm)'
        ]
        writer.writerow(headers)
        
        # Thêm dữ liệu cho từng sản phẩm
        for idx, product in enumerate(products, 1):
            sku, name, price, url, aff_link, fetched_at = product
            
            # Xử lý tên sản phẩm (đảm bảo độ dài 5-255 ký tự)
            product_name = name if name and len(name) >= 5 else f"Sản phẩm {sku[:20]}"
            product_name = product_name[:255]  # Cắt nếu quá dài
            
            # Format giá
            price_value = price if price and price != 'N/A' else '0'
            price_value = price_value.replace(',', '').replace('.', '')
            if not price_value.isdigit():
                price_value = '100000'  # Giá mặc định nếu không có
            
            row = [
                idx,  # Group No
                'Điện thoại & Phụ kiện',  # Danh mục ngành hàng (có thể điều chỉnh)
                product_name,  # Tên sản phẩm
                product_name[:100] if len(product_name) > 100 else product_name,  # Tên EN
                '', '', '', '', '', '', '', '',  # Ảnh sản phẩm (để trống)
                'No Brand',  # Thương hiệu (tạm thời)
                f"Mô tả: {product_name[:200]}. Liên hệ để biết thêm chi tiết.",  # Mô tả
                'NO',  # Hàng hóa nguy hiểm
                '', '', '',  # Variations
                '', '',  # Variation Name2
                price_value,  # Giá
                sku,  # SellerSku
                '10',  # Số lượng tồn kho
                '0.5',  # Khối lượng (kg)
                '20',  # Chiều rộng (cm)
                '20',  # Chiều dài (cm)
                '10'   # Chiều cao (cm)
            ]
            writer.writerow(row)
            
            print(f"✅ {idx}. {product_name[:50]}... -> Giá: {price_value} VND")
    
    print(f"\n✅ Đã tạo file: {csv_file}")
    print(f"📊 Tổng số sản phẩm: {len(products)}")
    print("\n📋 Hướng dẫn upload lên Lazada:")
    print("   1. Đăng nhập https://sellercenter.lazada.vn")
    print("   2. Vào 'Sản phẩm' → 'Thêm sản phẩm hàng loạt'")
    print(f"   3. Tải file {csv_file} lên")
    print("   4. Kiểm tra và hoàn tất upload")

if __name__ == "__main__":
    convert_to_lazada_format()
