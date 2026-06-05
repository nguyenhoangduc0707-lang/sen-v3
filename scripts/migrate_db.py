# scripts/migrate_db.py
"""
Migration script để cập nhật database schema từ version cũ lên mới
Chạy: python scripts/migrate_db.py
"""

import sqlite3
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_PATH = "sen_v3.db"

def migrate_database():
    """Thêm các cột mới vào bảng users nếu chưa có"""
    
    if not os.path.exists(DB_PATH):
        logger.info("Database file not found. Will be created fresh.")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Lấy danh sách cột hiện tại
    cursor.execute("PRAGMA table_info(users)")
    existing_columns = [col[1] for col in cursor.fetchall()]
    
    logger.info(f"Existing columns: {existing_columns}")
    
    # Thêm các cột mới
    new_columns = {
        "hashed_password": "TEXT NOT NULL DEFAULT ''",
        "full_name": "TEXT",
        "avatar_url": "TEXT",
        "token_quota": "INTEGER DEFAULT 50000",
        "tokens_used": "INTEGER DEFAULT 0",
        "token_reset_date": "TIMESTAMP",
        "parent_admin_id": "INTEGER",
        "updated_at": "TIMESTAMP",
        "is_active": "BOOLEAN DEFAULT 1"
    }
    
    for col, col_type in new_columns.items():
        if col not in existing_columns:
            try:
                cursor.execute(f"ALTER TABLE users ADD COLUMN {col} {col_type}")
                logger.info(f"✅ Added column: {col}")
            except Exception as e:
                logger.error(f"Failed to add {col}: {e}")
    
    # Cập nhật dữ liệu mặc định
    cursor.execute("UPDATE users SET hashed_password = ? WHERE hashed_password = ''", 
                   ("$2b$12$defaultpasswordhash",))
    
    # Thêm bảng mới nếu chưa tồn tại
    tables_to_create = [
        """
        CREATE TABLE IF NOT EXISTS ai_affiliate_products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            affiliate_link TEXT NOT NULL,
            commission_rate REAL NOT NULL,
            is_recurring BOOLEAN DEFAULT 1,
            target_task_type TEXT NOT NULL,
            description TEXT,
            total_clicks INTEGER DEFAULT 0,
            total_conversions INTEGER DEFAULT 0,
            total_revenue REAL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT 1
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            task_type TEXT NOT NULL,
            status TEXT DEFAULT 'PENDING',
            priority INTEGER DEFAULT 1,
            assigned_to_id INTEGER,
            estimated_tokens INTEGER DEFAULT 2000,
            actual_tokens_used INTEGER DEFAULT 0,
            expected_commission REAL DEFAULT 0,
            actual_commission REAL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            started_at TIMESTAMP,
            completed_at TIMESTAMP,
            FOREIGN KEY (assigned_to_id) REFERENCES users(id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS commission_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id INTEGER NOT NULL,
            task_id INTEGER,
            total_commission REAL NOT NULL,
            admin_share_amount REAL NOT NULL,
            member_share_amount REAL NOT NULL,
            admin_rate REAL DEFAULT 0.1,
            status TEXT DEFAULT 'PENDING_SETTLEMENT',
            transaction_id TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            settled_at TIMESTAMP,
            FOREIGN KEY (member_id) REFERENCES users(id),
            FOREIGN KEY (task_id) REFERENCES tasks(id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS token_usage_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            task_id INTEGER,
            tokens_used INTEGER NOT NULL,
            endpoint TEXT,
            request_data TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (task_id) REFERENCES tasks(id)
        )
        """
    ]
    
    for create_sql in tables_to_create:
        try:
            cursor.execute(create_sql)
            logger.info(f"✅ Table created/verified")
        except Exception as e:
            logger.error(f"Failed to create table: {e}")
    
    conn.commit()
    conn.close()
    logger.info("✅ Migration completed successfully!")

def verify_schema():
    """Kiểm tra schema sau migration"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Kiểm tra bảng users
    cursor.execute("PRAGMA table_info(users)")
    columns = cursor.fetchall()
    logger.info("\n📊 Users table schema:")
    for col in columns:
        logger.info(f"   - {col[1]}: {col[2]}")
    
    # Kiểm tra số lượng bảng
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    logger.info(f"\n📋 Total tables: {len(tables)}")
    for table in tables:
        logger.info(f"   - {table[0]}")
    
    conn.close()

if __name__ == "__main__":
    logger.info("🔄 Starting database migration...")
    migrate_database()
    verify_schema()
    logger.info("🎉 Migration complete!")