import os
import requests
import psycopg2
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

ACCESS_KEY = os.getenv("ACCESS_TRADE_ACCESS_KEY")
if not ACCESS_KEY:
    raise ValueError("Chưa có ACCESS_TRADE_ACCESS_KEY trong .env")

DB_CONFIG = {
    "dbname": "sen_v3",
    "user": "postgres",
    "password": "0326014497",
    "host": "localhost",
    "port": 5432
}

def init_db():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS campaigns (
            id SERIAL PRIMARY KEY,
            campaign_id VARCHAR(50) UNIQUE NOT NULL,
            name TEXT,
            min_commission FLOAT,
            max_commission FLOAT,
            commission_type VARCHAR(20),
            category_id VARCHAR(20),
            category_name TEXT,
            logo TEXT,
            merchant TEXT,
            url TEXT,
            cookie_expire INT,
            status VARCHAR(10),
            raw_data JSONB,
            fetched_at TIMESTAMP DEFAULT NOW()
        )
    """)
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Bảng campaigns đã sẵn sàng")

def fetch_campaigns(page=1, page_size=50):
    url = "https://api.accesstrade.vn/v1/cashback/campaigns"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Token {ACCESS_KEY}"
    }
    params = {"page": page, "page_size": page_size}
    resp = requests.get(url, headers=headers, params=params)
    resp.raise_for_status()
    data = resp.json()
    if data.get("status") != "success":
        raise Exception(f"API error: {data.get('message')}")
    return data["data"]  # chứa campaigns và meta

def save_campaigns(campaigns):
    if not campaigns:
        return
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    for camp in campaigns:
        campaign_id = str(camp.get("campaign_id"))
        name = camp.get("name", "")
        min_commission = float(camp.get("min_commission", 0))
        max_commission = float(camp.get("max_commission", 0))
        commission_type = camp.get("commission_type", "")
        category_id = camp.get("category_id", "")
        category_name = camp.get("category_name", "")
        logo = camp.get("logo", "")
        merchant = camp.get("merchant", "")
        url = camp.get("url", "")
        cookie_expire = camp.get("cookie_expire", 0)
        status = camp.get("status", "")

        cur.execute("""
            INSERT INTO campaigns (
                campaign_id, name, min_commission, max_commission,
                commission_type, category_id, category_name,
                logo, merchant, url, cookie_expire, status,
                raw_data, fetched_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
            ON CONFLICT (campaign_id) DO UPDATE SET
                name = EXCLUDED.name,
                min_commission = EXCLUDED.min_commission,
                max_commission = EXCLUDED.max_commission,
                commission_type = EXCLUDED.commission_type,
                category_id = EXCLUDED.category_id,
                category_name = EXCLUDED.category_name,
                logo = EXCLUDED.logo,
                merchant = EXCLUDED.merchant,
                url = EXCLUDED.url,
                cookie_expire = EXCLUDED.cookie_expire,
                status = EXCLUDED.status,
                raw_data = EXCLUDED.raw_data,
                fetched_at = NOW()
        """, (
            campaign_id, name, min_commission, max_commission,
            commission_type, category_id, category_name,
            logo, merchant, url, cookie_expire, status,
            json.dumps(camp)
        ))
    conn.commit()
    cur.close()
    conn.close()
    print(f"✅ Đã lưu {len(campaigns)} campaign vào DB")

def fetch_all_campaigns():
    all_campaigns = []
    page = 1
    page_size = 50
    while True:
        print(f"📡 Đang lấy trang {page}...")
        data = fetch_campaigns(page, page_size)
        campaigns = data.get("campaigns", [])
        if not campaigns:
            break
        all_campaigns.extend(campaigns)
        meta = data.get("meta", {})
        total = meta.get("total", 0)
        print(f"   Lấy {len(campaigns)} campaign, tổng hiện tại: {len(all_campaigns)}/{total}")
        if len(all_campaigns) >= total:
            break
        page += 1
    return all_campaigns

def fetch_and_store():
    init_db()
    campaigns = fetch_all_campaigns()
    if campaigns:
        save_campaigns(campaigns)
        print(f"🎉 Tổng cộng {len(campaigns)} campaign đã được cập nhật.")
    else:
        print("⚠️ Không có campaign nào.")

if __name__ == "__main__":
    fetch_and_store()