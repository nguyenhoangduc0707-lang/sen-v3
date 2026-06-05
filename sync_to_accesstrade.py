"""
Sync Lazada products to AccessTrade
"""
import asyncio
import sys
sys.path.insert(0, '.')

from src.lazada_client import LazadaClient
from src.accesstrade_client import get_accesstrade_client
from src.task_queue_db import get_task_queue

async def sync_to_accesstrade():
    print("=" * 60)
    print("🔄 Syncing Lazada Products to AccessTrade")
    print("=" * 60)
    
    # Lấy sản phẩm từ database
    import sqlite3
    conn = sqlite3.connect('sen_v3.db')
    cursor = conn.cursor()
    cursor.execute('SELECT sku, name, affiliate_link FROM lazada_products')
    products = cursor.fetchall()
    conn.close()
    
    print(f"\n📦 Found {len(products)} products to sync\n")
    
    # Tạo tasks cho AccessTrade
    queue = get_task_queue()
    
    for sku, name, aff_link in products:
        task_data = {
            'sku': sku,
            'product_name': name,
            'affiliate_link': aff_link,
            'action': 'create_campaign'
        }
        
        task_id = queue.add_task(
            'sync_to_accesstrade',
            task_data,
            priority=1
        )
        print(f"✅ Created task #{task_id} for: {name[:50]}...")
    
    print(f"\n📊 Total tasks created: {len(products)}")
    print("\n🚀 Run the AccessTrade worker to process these tasks!")

if __name__ == "__main__":
    asyncio.run(sync_to_accesstrade())
