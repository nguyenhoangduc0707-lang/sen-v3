"""
Auto fetch and analyze campaign links - Fixed
"""
import sqlite3
import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

ACCESS_KEY = os.getenv("ACCESSTRADE_ACCESS_KEY")
HEADERS = {"Authorization": f"Token {ACCESS_KEY}"}

def auto_fetch_campaigns():
    """Tự động lấy và phân tích campaigns"""
    
    print("📡 Đang lấy campaigns từ AccessTrade API...")
    all_campaigns = []
    
    # 1. Lấy từ database trước
    conn = sqlite3.connect('sen_v3.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, category FROM accesstrade_campaigns")
    db_campaigns = cursor.fetchall()
    conn.close()
    
    for c in db_campaigns:
        if c[0] and c[1]:  # Chỉ lấy nếu có id và name
            all_campaigns.append({
                'id': str(c[0]),
                'name': str(c[1]) if c[1] else "Unknown",
                'category': str(c[2]) if c[2] else "Other",
                'source': 'database'
            })
    
    # 2. Thử lấy từ API
    try:
        response = requests.get(
            "https://api.accesstrade.vn/v1/campaigns",
            headers=HEADERS,
            params={"limit": 100},
            timeout=15
        )
        if response.status_code == 200:
            api_campaigns = response.json().get('data', [])
            for c in api_campaigns:
                if c.get('id') and c.get('name'):
                    all_campaigns.append({
                        'id': str(c.get('id')),
                        'name': str(c.get('name')),
                        'category': str(c.get('category')) if c.get('category') else "Other",
                        'commission': c.get('commission'),
                        'source': 'api'
                    })
            print(f"✅ Lấy thêm {len(api_campaigns)} campaigns từ API")
    except Exception as e:
        print(f"⚠️ API error: {e}")
    
    return all_campaigns

def analyze_strategy(campaigns):
    """Phân tích chiến lược cho từng campaign - Fixed"""
    
    high_value = []    # Hoa hồng cao
    high_volume = []   # Dễ bán, số lượng nhiều
    new_trend = []     # Xu hướng mới
    
    for camp in campaigns:
        name = camp.get('name', '').lower() if camp.get('name') else ''
        category = camp.get('category', '').lower() if camp.get('category') else ''
        
        if not name:
            continue
        
        # Phân loại theo từ khóa
        if any(kw in name for kw in ['vay', 'tín chấp', 'credit', 'loan', 'vpbank', 'tpbank', 'hdbank']):
            high_value.append(camp)
        elif any(kw in name for kw in ['shopee', 'lazada', 'tiki', 'sendo', 'alibaba', 'e-commerce']):
            high_volume.append(camp)
        elif any(kw in name for kw in ['chứng khoán', 'stock', 'invest', 'maybank']):
            new_trend.append(camp)
        elif 'financial' in category or '35' in category or '60' in category:
            high_value.append(camp)
        elif 'e-commerce' in category or '59' in category:
            high_volume.append(camp)
    
    return {
        'high_value': high_value,
        'high_volume': high_volume,
        'new_trend': new_trend,
        'total': len(campaigns)
    }

def suggest_priority(analysis):
    """Đề xuất chiến lược chạy"""
    
    print("\n" + "=" * 70)
    print("🎯 CHIẾN LƯỢC ĐỀ XUẤT")
    print("=" * 70)
    
    suggestions = []
    
    # Ưu tiên 1: High value (hoa hồng cao)
    if analysis['high_value']:
        print(f"\n💰 ƯU TIÊN 1 - HOA HỒNG CAO ({len(analysis['high_value'])} campaigns)")
        for camp in analysis['high_value'][:5]:
            name = camp.get('name', 'Unknown')[:50]
            print(f"   → {name}")
            suggestions.append({
                'campaign': name,
                'priority': 1,
                'type': 'high_value',
                'estimated_commission': '500,000 - 2,000,000đ'
            })
    
    # Ưu tiên 2: High volume (dễ bán)
    if analysis['high_volume']:
        print(f"\n📦 ƯU TIÊN 2 - DỄ BÁN ({len(analysis['high_volume'])} campaigns)")
        for camp in analysis['high_volume'][:5]:
            name = camp.get('name', 'Unknown')[:50]
            print(f"   → {name}")
            suggestions.append({
                'campaign': name,
                'priority': 2,
                'type': 'high_volume',
                'estimated_commission': '50,000 - 500,000đ'
            })
    
    # Ưu tiên 3: New trend
    if analysis['new_trend']:
        print(f"\n📈 ƯU TIÊN 3 - XU HƯỚNG MỚI ({len(analysis['new_trend'])} campaigns)")
        for camp in analysis['new_trend'][:3]:
            name = camp.get('name', 'Unknown')[:50]
            print(f"   → {name}")
            suggestions.append({
                'campaign': name,
                'priority': 3,
                'type': 'new_trend',
                'estimated_commission': '100,000 - 1,000,000đ'
            })
    
    return suggestions

def generate_worker_tasks(analysis, target_workers=500):
    """Tạo tasks cho workers"""
    
    tasks = []
    publisher_id = "6983938396644077046"
    
    # Phân bổ workers theo chiến lược
    high_value_count = min(len(analysis['high_value']), int(target_workers * 0.4))  # 40%
    high_volume_count = min(len(analysis['high_volume']), int(target_workers * 0.4))  # 40%
    new_trend_count = min(len(analysis['new_trend']), int(target_workers * 0.2))  # 20%
    
    # Tạo tasks cho high value
    for camp in analysis['high_value'][:high_value_count]:
        camp_id = camp.get('id')
        if camp_id:
            link = f"https://go.isclix.com/deep_link/v5/{publisher_id}/{camp_id}?sub4=sen_v3_auto"
            tasks.append({
                'campaign': camp.get('name', 'Unknown')[:50],
                'link': link,
                'type': 'high_value',
                'priority': 1,
                'campaign_id': camp_id
            })
    
    # Tạo tasks cho high volume
    for camp in analysis['high_volume'][:high_volume_count]:
        camp_id = camp.get('id')
        if camp_id:
            link = f"https://go.isclix.com/deep_link/v5/{publisher_id}/{camp_id}?sub4=sen_v3_auto"
            tasks.append({
                'campaign': camp.get('name', 'Unknown')[:50],
                'link': link,
                'type': 'high_volume',
                'priority': 2,
                'campaign_id': camp_id
            })
    
    # Tạo tasks cho new trend
    for camp in analysis['new_trend'][:new_trend_count]:
        camp_id = camp.get('id')
        if camp_id:
            link = f"https://go.isclix.com/deep_link/v5/{publisher_id}/{camp_id}?sub4=sen_v3_auto"
            tasks.append({
                'campaign': camp.get('name', 'Unknown')[:50],
                'link': link,
                'type': 'new_trend',
                'priority': 3,
                'campaign_id': camp_id
            })
    
    return tasks

# === MAIN ===
print("=" * 70)
print("🤖 AUTO SYSTEM - PHÂN TÍCH & ĐỀ XUẤT CHIẾN LƯỢC")
print("=" * 70)

# 1. Lấy campaigns
campaigns = auto_fetch_campaigns()
print(f"\n📊 Tổng số campaigns: {len(campaigns)}")

# 2. Phân tích
analysis = analyze_strategy(campaigns)
print(f"\n📈 PHÂN TÍCH:")
print(f"   💰 High value (vay, tín chấp): {len(analysis['high_value'])}")
print(f"   📦 High volume (e-commerce): {len(analysis['high_volume'])}")
print(f"   📊 New trend (chứng khoán): {len(analysis['new_trend'])}")

# 3. Đề xuất
suggestions = suggest_priority(analysis)

# 4. Tạo tasks
tasks = generate_worker_tasks(analysis, target_workers=500)
print(f"\n🚀 TẠO TASKS CHO WORKERS:")
print(f"   📋 Tổng số tasks: {len(tasks)}")
print(f"   💰 High value: {len([t for t in tasks if t['type'] == 'high_value'])}")
print(f"   📦 High volume: {len([t for t in tasks if t['type'] == 'high_volume'])}")
print(f"   📈 New trend: {len([t for t in tasks if t['type'] == 'new_trend'])}")

# 5. Lưu kết quả
with open('auto_strategy.json', 'w', encoding='utf-8') as f:
    json.dump({
        'analysis': {
            'high_value_count': len(analysis['high_value']),
            'high_volume_count': len(analysis['high_volume']),
            'new_trend_count': len(analysis['new_trend'])
        },
        'suggestions': suggestions,
        'tasks': tasks,
        'total_tasks': len(tasks),
        'generated_at': datetime.now().isoformat()
    }, f, indent=2, ensure_ascii=False)

print(f"\n✅ Đã lưu chiến lược vào auto_strategy.json")
print("=" * 70)

# Hiển thị top tasks
print("\n🔗 TOP 5 TASKS ƯU TIÊN:")
for i, task in enumerate(tasks[:5], 1):
    print(f"{i}. {task['campaign']} - {task['type']}")
print("=" * 70)
