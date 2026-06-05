import requests
import os
from dotenv import load_dotenv
import json
from datetime import datetime, timedelta

load_dotenv()

ACCESS_KEY = os.getenv("ACCESSTRADE_ACCESS_KEY")
HEADERS = {"Authorization": f"Token {ACCESS_KEY}"}

print("=" * 60)
print("💰 ACCESSTRADE - DOANH THU THẬT")
print("=" * 60)

# Lấy transactions thật
url = "https://api.accesstrade.vn/v1/transactions"
params = {"limit": 50, "startDate": (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")}

try:
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code == 200:
        data = response.json()
        transactions = data.get('data', [])
        
        total_revenue = sum(float(t.get('amount', 0)) for t in transactions)
        total_commission = sum(float(t.get('commission', 0)) for t in transactions)
        
        print(f"\n📊 Thống kê 30 ngày qua:")
        print(f"   💰 Doanh thu: {total_revenue:,.0f} VND")
        print(f"   🎁 Hoa hồng: {total_commission:,.0f} VND")
        print(f"   📦 Số giao dịch: {len(transactions)}")
        
        # Lưu vào database
        import sqlite3
        conn = sqlite3.connect('sen_v3.db')
        cursor = conn.cursor()
        
        for t in transactions:
            cursor.execute('''
                INSERT OR REPLACE INTO sales_tracking 
                (campaign_id, revenue, commission, date)
                VALUES (?, ?, ?, ?)
            ''', (t.get('campaign_id'), t.get('amount', 0), t.get('commission', 0), t.get('created_at', datetime.now().isoformat())))
        
        conn.commit()
        print(f"\n✅ Đã lưu {len(transactions)} giao dịch vào database")
        conn.close()
    else:
        print(f"❌ Lỗi: {response.status_code} - {response.text}")
except Exception as e:
    print(f"❌ Exception: {e}")
