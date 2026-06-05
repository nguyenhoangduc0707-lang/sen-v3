import logging
import os

import psycopg2
import requests
from dotenv import load_dotenv
from psycopg2.extras import Json, execute_values

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

API_KEY = os.getenv("ACCESS_TRADE_API_KEY")
API_SECRET = os.getenv("ACCESS_TRADE_API_SECRET")
DB_CONFIG = {
    "dbname": "sen_v3",
    "user": "postgres",          # sửa từ sen_user thành postgres
    "password": "0326014497",    # mật khẩu đúng
    "host": "localhost",
    "port": 5432
}

MIN_COMMISSION_RATE = 5.0
ALLOWED_CATEGORIES = ["thời trang", "điện tử", "làm đẹp"]


def get_campaigns_from_accesstrade():
    """Call AccessTrade and return campaign rows."""
    if not API_KEY:
        logger.error("Missing ACCESS_TRADE_API_KEY in .env")
        return []

    url = "https://api.accesstrade.vn/v1/campaigns"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        campaigns = data.get("data", [])
        logger.info("Fetched %s campaigns from AccessTrade", len(campaigns))
        return campaigns
    except Exception as exc:
        logger.error("AccessTrade API error: %s", exc)
        return []


def filter_campaigns(campaigns):
    """Filter campaigns by minimum commission and allowed category."""
    filtered = []
    for campaign in campaigns:
        commission = float(campaign.get("commission", 0))
        category = campaign.get("category", "").lower()
        if commission >= MIN_COMMISSION_RATE and category in ALLOWED_CATEGORIES:
            filtered.append(campaign)
    logger.info("Filtered campaigns: %s", len(filtered))
    return filtered


def init_db():
    """Create affiliate campaign table when it does not exist."""
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS campaigns (
            id SERIAL PRIMARY KEY,
            campaign_id VARCHAR(50) UNIQUE NOT NULL,
            name TEXT,
            commission_rate FLOAT,
            category TEXT,
            raw_data JSONB,
            fetched_at TIMESTAMP DEFAULT NOW()
        )
        """
    )
    conn.commit()
    cur.close()
    conn.close()
    logger.info("Campaign table is ready")


def save_campaigns(campaigns):
    """Upsert campaigns into PostgreSQL."""
    if not campaigns:
        return

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    values = [
        (
            campaign.get("id"),
            campaign.get("name"),
            float(campaign.get("commission", 0)),
            campaign.get("category", ""),
            Json(campaign),
        )
        for campaign in campaigns
    ]
    execute_values(
        cur,
        """
        INSERT INTO campaigns (campaign_id, name, commission_rate, category, raw_data, fetched_at)
        VALUES %s
        ON CONFLICT (campaign_id) DO UPDATE SET
            name = EXCLUDED.name,
            commission_rate = EXCLUDED.commission_rate,
            category = EXCLUDED.category,
            raw_data = EXCLUDED.raw_data,
            fetched_at = NOW()
        """,
        values,
    )
    conn.commit()
    logger.info("Upserted %s campaigns", len(values))
    cur.close()
    conn.close()


def fetch_and_store():
    """Fetch, filter, and store campaigns. Intended for scheduled runs."""
    init_db()
    raw = get_campaigns_from_accesstrade()
    if not raw:
        logger.warning("No campaigns fetched")
        return
    filtered = filter_campaigns(raw)
    save_campaigns(filtered)


if __name__ == "__main__":
    fetch_and_store()
