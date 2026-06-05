import psycopg2
from datetime import datetime

DB_CONFIG = {
    "dbname": "sen_v3",
    "user": "postgres",
    "password": "0326014497",
    "host": "localhost",
    "port": 5432
}

def insert_mock_campaigns():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    campaigns = [
        ("mock_001", "Chiến dịch thời trang mùa hè", 12.5, "thời trang"),
        ("mock_002", "Điện thoại thông minh giảm giá", 8.0, "điện tử"),
        ("mock_003", "Mỹ phẩm Hàn Quốc", 15.0, "làm đẹp")
    ]
    for camp in campaigns:
        cur.execute("""
            INSERT INTO campaigns (campaign_id, name, commission_rate, category, fetched_at)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (campaign_id) DO NOTHING
        """, (camp[0], camp[1], camp[2], camp[3], datetime.now()))
    conn.commit()
    print(f"✅ Đã chèn {len(campaigns)} mock campaigns")
    cur.close()
    conn.close()

if __name__ == "__main__":
    insert_mock_campaigns()