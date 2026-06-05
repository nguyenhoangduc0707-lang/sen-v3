#!/usr/bin/env python3
import json
import random
import sqlite3
from datetime import datetime, timedelta
from typing import List, Dict, Any

def generate_campaigns(count: int = 15) -> List[Dict[str, Any]]:
    categories = [
        {"name": "Thời trang", "value": 1},
        {"name": "Điện tử", "value": 2},
        {"name": "Mẹ và bé", "value": 3},
        {"name": "Nhà cửa", "value": 4},
        {"name": "Sức khỏe", "value": 5},
        {"name": "Du lịch", "value": 6},
        {"name": "Thể thao", "value": 7},
        {"name": "Làm đẹp", "value": 8}
    ]
    
    reward_types = [
        {"type": "CPA_SALES", "name": "Bán hàng", "reward": random.choice([5, 8, 10, 12, 15, 20])},
        {"type": "CPC", "name": "Click", "reward": random.choice([300, 500, 800])},
        {"type": "CPA_FIXED", "name": "Hoa hồng cố định", "reward": random.choice([50000, 100000, 200000])}
    ]
    
    shopee_products = [
        "Tai nghe không dây", "Áo thun thể thao", "Điện thoại thông minh",
        "Máy hút bụi mini", "Sách nấu ăn", "Vali kéo", "Mỹ phẩm Hàn Quốc",
        "Đồ chơi trẻ em", "Bàn phím cơ", "Đồng hồ thông minh"
    ]
    
    campaigns = []
    start_date = datetime.now()
    end_date = start_date + timedelta(days=90)
    
    for i in range(1, count + 1):
        product_name = random.choice(shopee_products)
        reward = random.choice(reward_types)
        
        commission_rate = reward["reward"] if reward["type"] == "CPA_SALES" else None
        commission_fixed = reward["reward"] if reward["type"] == "CPA_FIXED" else None
        cpc_price = reward["reward"] if reward["type"] == "CPC" else None
        
        campaign = {
            "id": 1000 + i,
            "name": f"Chương trình {product_name}",
            "type": "CPA",
            "url": f"https://shopee.vn/{product_name.lower().replace(' ', '-')}",
            "imageUrl": f"https://down-vn.img.susercontent.com/file/mock_{i}.png",
            "startDate": start_date.strftime("%Y-%m-%d"),
            "endDate": end_date.strftime("%Y-%m-%d"),
            "description": f"Mô tả chi tiết về chương trình affiliate {product_name}...",
            "englishDescription": f"Detailed description of {product_name} affiliate program...",
            "affiliationStatus": random.choice(["APPROVED", "APPLYING", "NEW"]),
            "currency": "VND",
            "defaultRewards": [{"type": reward["type"], "name": reward["name"], "reward": reward["reward"]}],
            "categories": random.sample(categories, k=random.randint(1, 2)),
            "budgetType": random.choice(["SALES_COUNT", "SALES_REWARD", "CLICK_COUNT"]),
            "budget": random.randint(100, 10000),
            "commission_rate": commission_rate,
            "commission_fixed": commission_fixed,
            "cpc_price": cpc_price
        }
        campaigns.append(campaign)
    return campaigns

def save_mock_campaigns_to_sqlite(campaigns: List[Dict[str, Any]]):
    conn = sqlite3.connect('sen_v3.db')
    cur = conn.cursor()
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS campaigns (
            id INTEGER PRIMARY KEY,
            name TEXT,
            description TEXT,
            url TEXT,
            commission_rate REAL,
            commission_fixed REAL,
            cpc_price REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    for c in campaigns:
        cur.execute('''
            INSERT OR REPLACE INTO campaigns 
            (id, name, description, url, commission_rate, commission_fixed, cpc_price)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            c["id"], c["name"], c["description"], c["url"],
            c["commission_rate"], c["commission_fixed"], c["cpc_price"]
        ))
    
    conn.commit()
    conn.close()
    print(f" Đã lưu {len(campaigns)} campaign vào SQLite")

if __name__ == "__main__":
    campaigns = generate_campaigns(15)
    print(json.dumps(campaigns, indent=2, ensure_ascii=False))
    save_mock_campaigns_to_sqlite(campaigns)
    print(f"\n Thống kê campaign đã tạo: {len(campaigns)} campaigns")
