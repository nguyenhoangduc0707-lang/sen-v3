"""
Get AccessTrade Campaigns - Real Data
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.accesstrade_client import get_accesstrade_client

async def get_campaigns():
    print("=" * 60)
    print("📊 AccessTrade Campaigns - REAL DATA")
    print("=" * 60)
    
    client = await get_accesstrade_client()
    result = await client.get_campaigns(limit=10)
    
    if result.get('success'):
        campaigns = result.get('data', [])
        print(f"\n✅ Found {len(campaigns)} campaigns:\n")
        
        for idx, camp in enumerate(campaigns[:10], 1):
            name = camp.get('name', 'N/A')
            commission = camp.get('commission', 'N/A')
            print(f"{idx}. {name[:60]}")
            print(f"   Commission: {commission}%")
            print()
    else:
        print(f"❌ Error: {result.get('error')}")
    
    await client.close()
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(get_campaigns())
