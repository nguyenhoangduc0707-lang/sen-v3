"""
Real Dashboard - Doanh thu thật từ API
"""
import requests
import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def get_real_stats():
    """Lấy thống kê thật từ AccessTrade"""
    headers = {"Authorization": f"Token {os.getenv('ACCESSTRADE_ACCESS_KEY')}"}
    
    # Lấy transactions thật
    response = requests.get(
        "https://api.accesstrade.vn/v1/transactions",
        headers=headers,
        params={"limit": 100}
    )
    
    if response.status_code == 200:
        transactions = response.json().get('data', [])
        return {
            "revenue": sum(t.get('amount', 0) for t in transactions),
            "commission": sum(t.get('commission', 0) for t in transactions),
            "transactions": len(transactions),
            "timestamp": datetime.now().isoformat()
        }
    return {"error": "Không thể lấy dữ liệu"}

if __name__ == "__main__":
    stats = get_real_stats()
    print("=" * 50)
    print("💰 DOANH THU THẬT TỪ ACCESSTRADE")
    print("=" * 50)
    print(f"   💰 Doanh thu: {stats.get('revenue', 0):,.0f} VND")
    print(f"   🎁 Hoa hồng: {stats.get('commission', 0):,.0f} VND")
    print(f"   📦 Giao dịch: {stats.get('transactions', 0)}")
    print("=" * 50)
