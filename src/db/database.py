# src/db/database.py
"""
Database Configuration - DYT_01 Affiliate Campaign
Tích hợp Core Upgrade SEN V3
"""

from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import os
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger(__name__)

# Database URL - Hỗ trợ SQLite (dev) và PostgreSQL (production)
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "sqlite:///./sen_v3.db"  # Mặc định dùng file sen_v3.db hiện tại
)

# Engine configuration với tối ưu cho từng loại DB
if "sqlite" in DATABASE_URL:
    # SQLite config cho development
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=False,  # Set True để debug SQL
        poolclass=StaticPool  # Tối ưu cho SQLite
    )
    
    # Enable foreign key constraints cho SQLite
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
        
else:
    # PostgreSQL config cho production
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,  # Kiểm tra connection trước khi dùng
        pool_size=10,         # Số connection tối đa
        max_overflow=20,      # Connection vượt quá pool_size
        pool_recycle=3600,    # Recycle connection sau 1 giờ
        echo=False
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """
    Dependency để lấy database session
    Sử dụng trong các API endpoints
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database error: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

def init_db():
    """Khởi tạo database: tạo tất cả bảng nếu chưa tồn tại"""
    try:
        # Import tất cả models để register với Base (include legacy for facebook_posts etc.)
        from src.db.models import (
            User, Task, CommissionLog, AIAffiliateProduct, TokenUsageHistory,
            FacebookPost, Worker, ExecutionLog, DeadLetter,
            AutomationTemplate, AutomationRule, AutomationLog,
        )
        
        # Tạo bảng
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database initialized successfully!")
        
        # Kiểm tra dữ liệu mẫu
        seed_sample_data()
        
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {str(e)}")
        raise

def seed_sample_data():
    """Thêm dữ liệu mẫu nếu database trống"""
    # Import models locally so the function is self-contained
    # (they are not in global scope because init_db imports them locally)
    from src.db.models import (
        User, Task, AIAffiliateProduct, UserRole
    )
    from passlib.context import CryptContext

    db = SessionLocal()
    try:
        # Kiểm tra nếu đã có dữ liệu
        if db.query(User).count() == 0:
            
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
            
            # Tạo Admin mặc định (sử dụng env hoặc mặc định an toàn)
            admin_pass = os.getenv("ADMIN_INITIAL_PASSWORD", "ChangeMeImmediately123!")
            admin = User(
                username="admin_system",
                email="admin@senv3.com",
                hashed_password=pwd_context.hash(admin_pass),
                role=UserRole.ADMIN,
                token_quota=1000000,  # Admin có quota lớn
                tokens_used=0,
                full_name="System Admin",
                is_active=True
            )
            db.add(admin)
            db.flush()
            
            # Tạo Member mẫu (sử dụng env)
            member_pass = os.getenv("MEMBER_INITIAL_PASSWORD", "ChangeMe123!")
            member = User(
                username="member_demo",
                email="member@senv3.com",
                hashed_password=pwd_context.hash(member_pass),
                role=UserRole.MEMBER,
                token_quota=50000,
                tokens_used=0,
                parent_admin_id=admin.id,
                full_name="Demo Member",
                is_active=True
            )
            db.add(member)
            db.flush()
            
            # Tạo AI Affiliate Products mẫu
            products = [
                AIAffiliateProduct(
                    name="Writesonic AI",
                    affiliate_link="https://writesonic.com/?via=senv3-admin",
                    commission_rate=0.30,
                    is_recurring=True,
                    target_task_type="content_facebook",
                    description="Tạo content Facebook chất lượng cao với AI, hoa hồng 30% recurring hàng tháng"
                ),
                AIAffiliateProduct(
                    name="HeyGen AI Video",
                    affiliate_link="https://heygen.com/?ref=senv3",
                    commission_rate=0.25,
                    is_recurring=True,
                    target_task_type="video_tiktok",
                    description="Tạo video TikTok với AI Avatar, hoa hồng 25% recurring"
                ),
                AIAffiliateProduct(
                    name="Scrapy Cloud",
                    affiliate_link="https://scrapycloud.com/?aff=senv3",
                    commission_rate=0.20,
                    is_recurring=False,
                    target_task_type="scrape_deal",
                    description="Công cụ scrape data tự động, hoa hồng 20% one-time"
                )
            ]
            
            for product in products:
                db.add(product)
            
            # Tạo Task mẫu
            task = Task(
                title="Viết bài Facebook về AI Marketing",
                description="Tạo 5 bài post Facebook về xu hướng AI trong Marketing",
                task_type="content_facebook",
                status="PENDING",
                assigned_to_id=member.id,
                estimated_tokens=3000,
                expected_commission=100.0,
                priority=2
            )
            db.add(task)
            
            db.commit()
            logger.info("✅ Sample data seeded successfully!")
            
    except Exception as e:
        db.rollback()
        logger.warning(f"⚠️ Seeding sample data failed (may already exist): {str(e)}")
    finally:
        db.close()

# Export để dùng trong các module khác
__all__ = ["engine", "SessionLocal", "Base", "get_db", "init_db"]