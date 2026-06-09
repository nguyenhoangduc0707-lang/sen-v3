#!/usr/bin/env python3
"""
SYNC version of database initializer - FIXED for MissingGreenlet error
Run: python scripts/init_db_sync.py --action create --force
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, Session
from src.db.models import Base, User, Task, CommissionLog, AIAffiliateProduct, TokenUsageHistory, UserRole
from src.auth.jwt import get_password_hash
from datetime import datetime, timedelta
import logging
import argparse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# SYNC engine - KHÔNG dùng aiosqlite
DATABASE_URL = "sqlite:///./app.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def create_tables():
    """Create all tables"""
    logger.info("🔄 Creating database tables (SYNC mode)...")
    Base.metadata.create_all(bind=engine)
    logger.info("✅ Tables created successfully!")

def drop_tables():
    """Drop all tables"""
    confirm = input("⚠️ Bạn có chắc muốn xóa tất cả dữ liệu? (yes/no): ")
    if confirm.lower() == 'yes':
        logger.info("⚠️ Dropping all tables...")
        Base.metadata.drop_all(bind=engine)
        logger.info("✅ Tables dropped successfully!")
    else:
        logger.info("❌ Operation cancelled")

def seed_demo_data():
    """Seed demo data - same as original but using sync session"""
    db = SessionLocal()
    
    try:
        if db.query(User).count() > 0:
            logger.info("⚠️ Database already has data, skipping seed...")
            return
        
        logger.info("🌱 Seeding demo data...")
        
        # 1. Admin
        admin = User(
            username="admin_system",
            email="admin@senv3.com",
            hashed_password=get_password_hash("Admin@123456"),
            role=UserRole.ADMIN,
            full_name="System Administrator",
            token_quota=1000000,
            tokens_used=0,
            is_active=True
        )
        db.add(admin)
        db.flush()
        logger.info(f"✅ Created Admin: {admin.username}")
        
        # 2. Members
        members_data = [
            {"username": "member_nguyen", "email": "nguyen@senv3.com", "full_name": "Nguyen Van A"},
            {"username": "member_tran", "email": "tran@senv3.com", "full_name": "Tran Thi B"},
            {"username": "member_lee", "email": "lee@senv3.com", "full_name": "Lee Quoc C"},
            {"username": "member_pham", "email": "pham@senv3.com", "full_name": "Pham Van D"},
            {"username": "member_hoang", "email": "hoang@senv3.com", "full_name": "Hoang Thi E"},
        ]
        
        members = []
        for m_data in members_data:
            member = User(
                username=m_data["username"],
                email=m_data["email"],
                hashed_password=get_password_hash("Member@123456"),
                role=UserRole.MEMBER,
                full_name=m_data["full_name"],
                token_quota=50000,
                tokens_used=0,
                parent_admin_id=admin.id,
                is_active=True
            )
            db.add(member)
            members.append(member)
        db.flush()
        logger.info(f"✅ Created {len(members)} Members")
        
        # 3. Regular Users
        regular_users = []
        for i in range(1, 11):
            user = User(
                username=f"user_{i}",
                email=f"user{i}@example.com",
                hashed_password=get_password_hash("User@123456"),
                role=UserRole.USER_KHOAHOC,
                full_name=f"Regular User {i}",
                token_quota=10000,
                tokens_used=0,
                parent_admin_id=None,
                is_active=True
            )
            db.add(user)
            regular_users.append(user)
        db.flush()
        logger.info(f"✅ Created {len(regular_users)} Regular Users")
        
        # 4. AI Affiliate Products
        products_data = [
            {"name": "Writesonic AI", "affiliate_link": "https://writesonic.com/?via=senv3-admin", "commission_rate": 0.30, "is_recurring": True, "target_task_type": "content_facebook", "description": "AI content creation"},
            {"name": "Jasper AI", "affiliate_link": "https://jasper.ai/?ref=senv3", "commission_rate": 0.25, "is_recurring": True, "target_task_type": "content_facebook", "description": "Advanced AI writer"},
            {"name": "HeyGen AI Video", "affiliate_link": "https://heygen.com/?ref=senv3", "commission_rate": 0.25, "is_recurring": True, "target_task_type": "video_tiktok", "description": "AI Avatar video"},
            {"name": "Pictory.ai", "affiliate_link": "https://pictory.ai/?ref=senv3", "commission_rate": 0.20, "is_recurring": True, "target_task_type": "video_tiktok", "description": "Auto video creator"},
            {"name": "SEMrush", "affiliate_link": "https://semrush.com/?ref=senv3", "commission_rate": 0.20, "is_recurring": True, "target_task_type": "seo_article", "description": "SEO tool"},
        ]
        
        products = []
        for p_data in products_data:
            product = AIAffiliateProduct(**p_data, total_clicks=0, total_conversions=0, total_revenue=0)
            db.add(product)
            products.append(product)
        db.flush()
        logger.info(f"✅ Created {len(products)} AI Products")
        
        # 5. Tasks
        tasks_data = [
            {"title": "Viết bài Facebook về AI Marketing", "task_type": "content_facebook", "assigned_to": members[0], "estimated_tokens": 3000, "expected_commission": 150},
            {"title": "Tạo video TikTok review sản phẩm", "task_type": "video_tiktok", "assigned_to": members[0], "estimated_tokens": 5000, "expected_commission": 200},
            {"title": "Content SEO cho blog Affiliate", "task_type": "seo_article", "assigned_to": members[1], "estimated_tokens": 4000, "expected_commission": 180},
            {"title": "Facebook post về ChatGPT", "task_type": "content_facebook", "assigned_to": members[2], "estimated_tokens": 2500, "expected_commission": 120},
        ]
        
        tasks = []
        for t_data in tasks_data:
            task = Task(
                title=t_data["title"],
                description=f"Auto task: {t_data['title']}",
                task_type=t_data["task_type"],
                status="PENDING",
                assigned_to_id=t_data["assigned_to"].id,
                estimated_tokens=t_data["estimated_tokens"],
                expected_commission=t_data["expected_commission"],
                priority=2,
                created_at=datetime.utcnow()
            )
            db.add(task)
            tasks.append(task)
        db.flush()
        logger.info(f"✅ Created {len(tasks)} Tasks")
        
        db.commit()
        
        logger.info("\n" + "="*60)
        logger.info("🎉 DATABASE INITIALIZATION COMPLETE!")
        logger.info("="*60)
        logger.info(f"📊 Summary:")
        logger.info(f"   - Admins: 1")
        logger.info(f"   - Members: {len(members)}")
        logger.info(f"   - Regular Users: {len(regular_users)}")
        logger.info(f"   - AI Products: {len(products)}")
        logger.info(f"   - Tasks: {len(tasks)}")
        logger.info("="*60)
        logger.info("\n🔐 Demo Accounts:")
        logger.info(f"   Admin:     admin_system / Admin@123456")
        logger.info(f"   Member:    member_nguyen / Member@123456")
        logger.info(f"   Regular:   user_1 / User@123456")
        logger.info("="*60)
        
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Error seeding data: {str(e)}")
        raise
    finally:
        db.close()

def reset_database():
    """Reset database"""
    logger.info("⚠️ Resetting database...")
    drop_tables()
    create_tables()
    seed_demo_data()
    logger.info("✅ Database reset complete!")

def main():
    parser = argparse.ArgumentParser(description='SEN V3 DB Management (SYNC)')
    parser.add_argument('--action', choices=['create', 'drop', 'seed', 'reset'], default='create')
    parser.add_argument('--force', action='store_true')
    args = parser.parse_args()
    
    if args.action == 'create':
        create_tables()
        if args.force or input("Seed demo data? (yes/no): ").lower() == 'yes':
            seed_demo_data()
    elif args.action == 'drop':
        if args.force or input("⚠️ Confirm drop? (yes/no): ").lower() == 'yes':
            drop_tables()
    elif args.action == 'seed':
        seed_demo_data()
    elif args.action == 'reset':
        if args.force or input("⚠️ Confirm RESET? (yes/no): ").lower() == 'yes':
            reset_database()

if __name__ == "__main__":
    main()