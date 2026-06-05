"""
Add sales tracking and worker statistics tables
"""
import sqlite3

conn = sqlite3.connect('sen_v3.db')
cursor = conn.cursor()

# 1. Tạo bảng theo dõi doanh số
cursor.execute('''
    CREATE TABLE IF NOT EXISTS sales_tracking (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        campaign_id TEXT,
        campaign_name TEXT,
        source TEXT,
        clicks INTEGER DEFAULT 0,
        orders INTEGER DEFAULT 0,
        revenue DECIMAL DEFAULT 0,
        commission DECIMAL DEFAULT 0,
        conversion_rate DECIMAL DEFAULT 0,
        date DATE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

# 2. Tạo bảng thống kê workers
cursor.execute('''
    CREATE TABLE IF NOT EXISTS worker_stats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        worker_name TEXT,
        status TEXT,
        tasks_processed INTEGER DEFAULT 0,
        tasks_succeeded INTEGER DEFAULT 0,
        tasks_failed INTEGER DEFAULT 0,
        last_active TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

# 3. Tạo bảng tổng hợp campaign performance
cursor.execute('''
    CREATE TABLE IF NOT EXISTS campaign_performance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        campaign_id TEXT,
        campaign_name TEXT,
        source TEXT,
        total_clicks INTEGER DEFAULT 0,
        total_orders INTEGER DEFAULT 0,
        total_revenue DECIMAL DEFAULT 0,
        total_commission DECIMAL DEFAULT 0,
        avg_conversion_rate DECIMAL DEFAULT 0,
        last_updated TIMESTAMP
    )
''')

print("✅ Created sales tracking tables")

# Thêm dữ liệu mẫu
sample_data = [
    ('6767399642708413705', 'TPBANK CREATOR', 'AccessTrade', 150, 5, 25000000, 1250000, 3.33, '2026-06-01'),
    ('6802131001370895715', 'LEAFY SHOPEE PUB', 'AccessTrade', 500, 12, 4800000, 240000, 2.4, '2026-06-01'),
    ('ACFCNEWU200', 'ACFC Online - Voucher 200K', 'ACFC', 200, 8, 12000000, 600000, 4.0, '2026-06-01'),
]

cursor.executemany('''
    INSERT INTO sales_tracking (campaign_id, campaign_name, source, clicks, orders, revenue, commission, conversion_rate, date)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
''', sample_data)

# Thêm thống kê workers
worker_data = [
    ('Lazada Worker', 'running', 45, 40, 5, '2026-06-02 02:30:00'),
    ('ACFC Worker', 'running', 16, 16, 0, '2026-06-02 02:30:00'),
    ('AccessTrade Worker', 'idle', 20, 18, 2, '2026-06-02 02:25:00'),
]

cursor.executemany('''
    INSERT INTO worker_stats (worker_name, status, tasks_processed, tasks_succeeded, tasks_failed, last_active)
    VALUES (?, ?, ?, ?, ?, ?)
''', worker_data)

conn.commit()
conn.close()

print("✅ Added sample data")
print("📊 Tables created: sales_tracking, worker_stats, campaign_performance")
