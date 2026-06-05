import asyncio
import requests
import os
from dotenv import load_dotenv

load_dotenv()

access_key = os.getenv("ACCESSTRADE_ACCESS_KEY")
headers = {"Authorization": f"Token {access_key}"}

print("=" * 60)
print("📊 AccessTrade Campaigns - REAL DATA")
print("=" * 60)

response = requests.get(
    "https://api.accesstrade.vn/v1/campaigns",
    headers=headers,
    params={"limit": 20}
)

if response.status_code == 200:
    data = response.json()
    campaigns = data.get('data', [])
    print(f"\n✅ Found {len(campaigns)} campaigns:\n")
    
    for idx, camp in enumerate(campaigns[:10], 1):
        name = camp.get('name', 'N/A')
        commission = camp.get('commission', 'N/A')
        print(f"{idx}. {name[:70]}")
        print(f"   Commission: {commission}%")
        print()
else:
    print(f"❌ Error: {response.status_code}")

print("=" * 60)
