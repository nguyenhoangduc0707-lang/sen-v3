# fetch_accesstrade_simple.py
import requests
import pandas as pd
import os
import time
from datetime import datetime, timedelta

def get_accesstrade_orders(api_key, days=30, status=1):
    """Lấy đơn hàng từ AccessTrade API"""
    
    # Tính thời gian
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    since = start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    until = end_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    url = "https://api.accesstrade.vn/v1/order-list"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    all_orders = []
    page = 1
    
    while True:
        params = {
            "since": since,
            "until": until,
            "status": status,
            "limit": 300,
            "page": page
        }
        
        print(f"📥 Đang lấy trang {page}...")
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code != 200:
            print(f"❌ Lỗi API: {response.status_code} - {response.text}")
            break
        
        data = response.json()
        orders = data.get('data', [])
        total = data.get('total', 0)
        
        if not orders:
            break
            
        all_orders.extend(orders)
        print(f"   ✅ Đã lấy {len(all_orders)}/{total} đơn")
        
        if len(all_orders) >= total:
            break
            
        page += 1
        time.sleep(6)  # Rate limit: 10 requests/phút
    
    return all_orders

def main():
    # Lấy API key từ environment
    api_key = os.environ.get('ACCESS_TRADE_API_KEY')
    
    if not api_key or api_key == "YOUR_ACCESSTRADE_API_KEY":
        print("❌ Chưa set API key AccessTrade!")
        print("   Chạy lệnh: $env:ACCESS_TRADE_API_KEY='your_actual_key'")
        print("   Lấy key tại: https://accesstrade.vn/affiliate/account/api")
        return
    
    print("🚀 Bắt đầu lấy dữ liệu AccessTrade...")
    orders = get_accesstrade_orders(api_key, days=30, status=1)
    
    if not orders:
        print("⚠️ Không có đơn hàng nào!")
        
        # Tạo file mẫu để test
        print("\n📝 Tạo file dữ liệu mẫu để test...")
        import random
        sample_orders = []
        for i in range(20):
            sample_orders.append({
                'order_id': f'SAMPLE{i:04d}',
                'merchant': random.choice(['Shopee', 'Lazada', 'Tiki']),
                'billing': random.randint(100000, 5000000),
                'pub_commission': random.randint(5000, 500000),
                'status': 1,
                'sales_time': datetime.now().strftime('%Y-%m-%d'),
                'utm_source': random.choice(['Facebook', 'Google', 'Direct'])
            })
        orders = sample_orders
        print(f"✅ Đã tạo {len(orders)} đơn hàng mẫu")
    
    # Tạo DataFrame
    df = pd.DataFrame(orders)
    
    # Xuất Excel
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"accesstrade_report_{timestamp}.xlsx"
    df.to_excel(filename, index=False)
    
    # Thống kê
    print("\n" + "="*50)
    print("📊 THỐNG KÊ")
    print("="*50)
    print(f"✅ Số đơn hàng: {len(df)}")
    if 'billing' in df.columns:
        print(f"💰 Tổng doanh thu: {df['billing'].sum():,.0f} VNĐ")
    if 'pub_commission' in df.columns:
        print(f"💵 Tổng hoa hồng: {df['pub_commission'].sum():,.0f} VNĐ")
    print(f"📁 File: {filename}")
    print("="*50)

if __name__ == "__main__":
    main()