import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import psycopg2
from affiliate.file_queue import push_campaign_to_queue

DB_CONFIG = {
    "dbname": "sen_v3",
    "user": "postgres",
    "password": "0326014497",
    "host": "localhost",
    "port": 5432
}

def push_all_campaigns():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("SELECT campaign_id FROM campaigns")
    rows = cur.fetchall()
    for (campaign_id,) in rows:
        push_campaign_to_queue(campaign_id)
    print(f"Đã đẩy {len(rows)} campaign vào file queue (tasks/campaign_queue.json)")
    cur.close()
    conn.close()

if __name__ == "__main__":
    push_all_campaigns()