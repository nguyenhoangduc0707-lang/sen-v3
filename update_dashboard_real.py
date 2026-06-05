"""
Complete Dashboard with Real Data from AccessTrade API
"""
import sqlite3
import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# Lấy access key từ .env
ACCESS_KEY = os.getenv("ACCESSTRADE_ACCESS_KEY")
HEADERS = {"Authorization": f"Token {ACCESS_KEY}", "Content-Type": "application/json"}

def get_real_transactions():
    """Lấy giao dịch thật từ AccessTrade API"""
    try:
        response = requests.get(
            "https://api.accesstrade.vn/v1/transactions",
            headers=HEADERS,
            params={"limit": 100},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            return data.get('data', [])
    except Exception as e:
        print(f"Error fetching transactions: {e}")
    return []

def get_campaign_details(campaign_id):
    """Lấy thông tin campaign từ database"""
    conn = sqlite3.connect('sen_v3.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, category FROM accesstrade_campaigns WHERE id = ?", (str(campaign_id),))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"name": row[0], "category": row[1]}
    return {"name": "Unknown", "category": "N/A"}

def calculate_stats(transactions):
    """Tính toán thống kê từ transactions thật"""
    stats = {
        'total_revenue': 0,
        'total_commission': 0,
        'total_clicks': len(transactions),
        'total_orders': len([t for t in transactions if t.get('status') == 'approved']),
        'by_campaign': {}
    }
    
    for t in transactions:
        amount = float(t.get('amount', 0))
        commission = float(t.get('commission', 0))
        campaign_id = t.get('campaign_id', 'unknown')
        
        stats['total_revenue'] += amount
        stats['total_commission'] += commission
        
        if campaign_id not in stats['by_campaign']:
            stats['by_campaign'][campaign_id] = {'revenue': 0, 'commission': 0, 'clicks': 0}
        stats['by_campaign'][campaign_id]['revenue'] += amount
        stats['by_campaign'][campaign_id]['commission'] += commission
        stats['by_campaign'][campaign_id]['clicks'] += 1
    
    return stats

# Lấy dữ liệu thật
print("📡 Đang lấy dữ liệu giao dịch từ AccessTrade API...")
transactions = get_real_transactions()
stats = calculate_stats(transactions)

# Lấy thông tin từ database
conn = sqlite3.connect('sen_v3.db')
cursor = conn.cursor()

# Số campaigns
cursor.execute("SELECT COUNT(*) FROM accesstrade_campaigns")
campaigns_count = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM acfc_promotions WHERE status = 'active'")
acfc_count = cursor.fetchone()[0]

# Worker stats (từ database)
cursor.execute("SELECT worker_name, tasks_processed, tasks_succeeded FROM worker_stats")
workers = cursor.fetchall()

conn.close()

# Tạo HTML
html = f'''<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SEN V3 - Real Time Dashboard</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #f0f2f5; padding: 20px; }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        h1 {{ color: #1a1a2e; }}
        .realtime-badge {{ background: #28a745; color: white; padding: 5px 10px; border-radius: 20px; font-size: 12px; display: inline-block; margin-left: 15px; }}
        
        .stats-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin: 30px 0; }}
        .stat-card {{ background: white; padding: 25px; border-radius: 12px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
        .stat-number {{ font-size: 32px; font-weight: bold; }}
        .stat-label {{ color: #666; margin-top: 8px; }}
        .revenue {{ color: #28a745; }}
        .commission {{ color: #007bff; }}
        
        .section {{ background: white; border-radius: 12px; padding: 20px; margin-bottom: 30px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
        .section-title {{ font-size: 20px; font-weight: bold; margin-bottom: 15px; border-bottom: 2px solid #007bff; padding-bottom: 10px; }}
        
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #eee; }}
        th {{ background: #f8f9fa; font-weight: 600; }}
        tr:hover {{ background: #f8f9fa; }}
        
        .badge {{ display: inline-block; padding: 4px 8px; border-radius: 4px; font-size: 12px; }}
        .badge-real {{ background: #28a745; color: white; }}
        .badge-demo {{ background: #ffc107; color: #333; }}
        
        .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
        .update-time {{ color: #666; font-size: 12px; margin-bottom: 20px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎯 SEN V3 - Real-Time Dashboard 
            <span class="realtime-badge">🔴 LIVE DATA</span>
        </h1>
        <div class="update-time">📡 Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number revenue">{stats['total_revenue']:,.0f}đ</div>
                <div class="stat-label">💰 Total Revenue</div>
            </div>
            <div class="stat-card">
                <div class="stat-number commission">{stats['total_commission']:,.0f}đ</div>
                <div class="stat-label">🎯 Total Commission</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{stats['total_clicks']:,}</div>
                <div class="stat-label">👆 Total Clicks</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{stats['total_orders']:,}</div>
                <div class="stat-label">📦 Total Orders</div>
            </div>
        </div>
        
        <div class="section">
            <div class="section-title">📊 Thống kê theo chiến dịch</div>
            <table>
                <thead>
                    <tr><th>Chiến dịch</th><th>Clicks</th><th>Doanh thu</th><th>Hoa hồng</th></tr>
                </thead>
                <tbody>
'''
if stats['by_campaign']:
    for camp_id, data in stats['by_campaign'].items():
        camp_info = get_campaign_details(camp_id)
        html += f'''
                    <tr>
                        <td>{camp_info['name'][:50]}</td>
                        <td>{data['clicks']}</td>
                        <td>{data['revenue']:,.0f}đ</td>
                        <td class="commission">{data['commission']:,.0f}đ</td>
                    </tr>'''
else:
    html += '<tr><td colspan="4" style="text-align:center">📭 Chưa có giao dịch nào. Hãy bắt đầu quảng bá link!</td></tr>'

html += '''
                </tbody>
            </table>
        </div>
        
        <div class="section">
            <div class="section-title">👷 Worker Status</div>
            <table>
                <thead><tr><th>Worker</th><th>Tasks Done</th><th>Success Rate</th></tr></thead>
                <tbody>
'''
for w in workers:
    rate = (w[2]/w[1]*100) if w[1] > 0 else 0
    html += f'<tr><td>{w[0]}</td><td>{w[1]}</td><td>{rate:.1f}%</td></tr>'

html += f'''
                </tbody>
            </table>
        </div>
        
        <div class="section">
            <div class="section-title">📈 Tổng quan hệ thống</div>
            <table>
                <tr><td>📊 AccessTrade Campaigns</td><td>{campaigns_count}</td></tr>
                <tr><td>🎯 ACFC Promotions</td><td>{acfc_count}</td></tr>
                <tr><td>🔗 Tổng số link đang chạy</td><td>{campaigns_count + acfc_count}</td></tr>
                <tr><td>✅ Workers đang hoạt động</td><td>{len(workers)}</td></tr>
            </table>
        </div>
        
        <div class="footer">
            <p>SEN V3 - Automated Marketing System | Dữ liệu trực tiếp từ AccessTrade API</p>
            <p>📅 Cập nhật real-time | 🚀 Đã bỏ qua dữ liệu demo</p>
        </div>
    </div>
</body>
</html>
'''

# Ghi file
with open('complete_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("=" * 60)
print("✅ Dashboard đã được cập nhật với dữ liệu REAL!")
print(f"📊 Tổng doanh thu thực tế: {stats['total_revenue']:,.0f}đ")
print(f"🎯 Tổng hoa hồng: {stats['total_commission']:,.0f}đ")
print(f"📦 Số đơn hàng: {stats['total_orders']}")
print("=" * 60)

# Mở dashboard
import webbrowser
webbrowser.open('complete_dashboard.html')
