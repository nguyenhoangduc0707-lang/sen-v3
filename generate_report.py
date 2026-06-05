"""
Revenue Report Generator for AccessTrade
"""
import json
from datetime import datetime

def generate_report():
    print("=" * 60)
    print("📊 ACCESSTRADE REVENUE REPORT")
    print("=" * 60)
    
    # Đọc tracking data
    try:
        with open('order_tracking.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except:
        print("❌ No tracking data found. Run create_tracking.py first")
        return
    
    products = data['products']
    
    # Tính tổng
    total_clicks = sum(p['clicks'] for p in products)
    total_orders = sum(p['orders'] for p in products)
    total_revenue = sum(p['revenue'] for p in products)
    total_commission = sum(p['commission'] for p in products)
    
    print(f"\n📈 SUMMARY STATISTICS:")
    print(f"   Total Products: {len(products)}")
    print(f"   Total Clicks: {total_clicks}")
    print(f"   Total Orders: {total_orders}")
    print(f"   Total Revenue: {total_revenue:,.0f} VND")
    print(f"   Total Commission: {total_commission:,.0f} VND")
    
    print(f"\n📋 PRODUCT PERFORMANCE:")
    for idx, p in enumerate(products, 1):
        print(f"\n   {idx}. {p['name'][:50]}")
        print(f"      Clicks: {p['clicks']}")
        print(f"      Orders: {p['orders']}")
        print(f"      Revenue: {p['revenue']:,.0f} VND")
        print(f"      Commission: {p['commission']:,.0f} VND")
        if p['clicks'] > 0:
            conversion_rate = (p['orders'] / p['clicks']) * 100
            print(f"      Conversion Rate: {conversion_rate:.1f}%")
    
    # Tạo file báo cáo
    report_file = f'report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Report saved to {report_file}")
    print("=" * 60)

if __name__ == "__main__":
    generate_report()
