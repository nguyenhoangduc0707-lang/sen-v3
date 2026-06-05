"""
Sync real transactions from AccessTrade to database
"""
import requests
import sqlite3
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
key = os.getenv('ACCESSTRADE_ACCESS_KEY')
headers = {'Authorization': f'Token {key}'}

response = requests.get(
    'https://api.accesstrade.vn/v1/transactions',
    headers=headers,
    params={'limit': 100}
)

if response.status_code == 200:
    data = response.json()
    transactions = data.get('data', [])
    
    conn = sqlite3.connect('sen_v3.db')
    cursor = conn.cursor()
    
    for t in transactions:
        cursor.execute('''
            INSERT OR REPLACE INTO sales_tracking 
            (campaign_id, campaign_name, source, revenue, commission, date)
            VALUES (?, ?, 'AccessTrade', ?, ?, ?)
        ''', (
            t.get('campaign_id'),
            t.get('campaign_name'),
            t.get('amount', 0),
            t.get('commission', 0),
            t.get('created_at', datetime.now().isoformat())
        ))
    
    conn.commit()
    print(f'✅ Synced {len(transactions)} real transactions')
    conn.close()
else:
    print(f'❌ Cannot fetch: {response.status_code}')
