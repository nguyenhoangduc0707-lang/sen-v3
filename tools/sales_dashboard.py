"""
Sales Dashboard with Worker Statistics
"""
import sqlite3
from datetime import datetime

conn = sqlite3.connect('sen_v3.db')
cursor = conn.cursor()

print("=" * 70)
print("📊 SEN V3 - SALES & WORKER DASHBOARD")
print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 70)

# 1. Tổng doanh số
cursor.execute('''
    SELECT 
        SUM(clicks) as total_clicks,
        SUM(orders) as total_orders,
        SUM(revenue) as total_revenue,
        SUM(commission) as total_commission
    FROM sales_tracking
''')
stats = cursor.fetchone()
total_clicks, total_orders, total_revenue, total_commission = stats

print("\n💰 TỔNG DOANH SỐ:")
print("-" * 40)
print(f"   📍 Tổng clicks: {total_clicks:,}")
print(f"   📦 Tổng đơn hàng: {total_orders:,}")
print(f"   💰 Tổng doanh thu: {total_revenue:,.0f} VND")
print(f"   🎯 Tổng hoa hồng: {total_commission:,.0f} VND")
if total_clicks > 0:
    cr = (total_orders / total_clicks) * 100
    print(f"   📈 Tỷ lệ chuyển đổi: {cr:.2f}%")

# 2. Doanh số theo nguồn
cursor.execute('''
    SELECT source, 
           SUM(clicks) as clicks,
           SUM(orders) as orders,
           SUM(revenue) as revenue,
           SUM(commission) as commission
    FROM sales_tracking
    GROUP BY source
''')
print("\n📊 DOANH SỐ THEO NGUỒN:")
print("-" * 40)
for row in cursor.fetchall():
    source, clicks, orders, revenue, commission = row
    print(f"   {source}:")
    print(f"      Clicks: {clicks:,} | Orders: {orders:,}")
    print(f"      Revenue: {revenue:,.0f} VND | Commission: {commission:,.0f} VND")

# 3. Thống kê workers
cursor.execute('''
    SELECT worker_name, status, tasks_processed, tasks_succeeded, tasks_failed, last_active
    FROM worker_stats
''')
print("\n👷 THỐNG KÊ WORKERS:")
print("-" * 40)
for row in cursor.fetchall():
    name, status, processed, success, failed, last_active = row
    status_icon = "🟢" if status == "running" else "🟡" if status == "idle" else "🔴"
    print(f"   {status_icon} {name}: {status}")
    print(f"      Tasks: {processed} total | ✅ {success} | ❌ {failed}")
    print(f"      Last active: {last_active}")

# 4. Top campaigns theo doanh số
cursor.execute('''
    SELECT campaign_name, source, clicks, orders, revenue, commission
    FROM sales_tracking
    ORDER BY revenue DESC
    LIMIT 5
''')
print("\n🏆 TOP CAMPAIGNS THEO DOANH SỐ:")
print("-" * 40)
for idx, row in enumerate(cursor.fetchall(), 1):
    name, source, clicks, orders, revenue, commission = row
    print(f"   {idx}. {name[:35]}")
    print(f"      Source: {source} | Clicks: {clicks} | Orders: {orders}")
    print(f"      Revenue: {revenue:,.0f} VND | Commission: {commission:,.0f} VND")

# 5. Hiệu suất conversion
cursor.execute('''
    SELECT campaign_name, source, 
           clicks, orders,
           ROUND(CAST(orders AS FLOAT) / NULLIF(clicks, 0) * 100, 2) as cr
    FROM sales_tracking
    WHERE clicks > 0
    ORDER BY cr DESC
    LIMIT 5
''')
print("\n🎯 TOP CONVERSION RATE:")
print("-" * 40)
for idx, row in enumerate(cursor.fetchall(), 1):
    name, source, clicks, orders, cr = row
    print(f"   {idx}. {name[:35]}")
    print(f"      CR: {cr}% | Clicks: {clicks} → Orders: {orders}")

conn.close()
print("\n" + "=" * 70)
