# scripts/init_db.py
"""
Script khởi tạo database và seed dữ liệu mẫu
Chạy lệnh: python scripts/init_db.py
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.db.database import init_db, engine, Base
from src.db.models import User, Task, CommissionLog, AIAffiliateProduct, TokenUsageHistory, UserRole
from src.auth.jwt import get_password_hash
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_tables():
    """Tạo tất cả bảng trong database"""
    logger.info("🔄 Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("✅ Tables created successfully!")

def drop_tables():
    """Xóa tất cả bảng (CẨN THẬN!)"""
    confirm = input("⚠️ Bạn có chắc muốn xóa tất cả dữ liệu? (yes/no): ")
    if confirm.lower() == 'yes':
        logger.info("⚠️ Dropping all tables...")
        Base.metadata.drop_all(bind=engine)
        logger.info("✅ Tables dropped successfully!")
    else:
        logger.info("❌ Operation cancelled")

def seed_demo_data():
    """Thêm dữ liệu demo phong phú"""
    from src.db.database import SessionLocal
    
    db = SessionLocal()
    
    try:
        # Kiểm tra nếu đã có dữ liệu
        if db.query(User).count() > 0:
            logger.info("⚠️ Database already has data, skipping seed...")
            return
        
        logger.info("🌱 Seeding demo data...")
        
        # 1. Tạo Admin
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
        
        # 2. Tạo Members (5 members)
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
        
        # 3. Tạo Regular Users (10 users)
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
        
        # 4. Tạo AI Affiliate Products
        products_data = [
            {
                "name": "Writesonic AI",
                "affiliate_link": "https://writesonic.com/?via=senv3-admin",
                "commission_rate": 0.30,
                "is_recurring": True,
                "target_task_type": "content_facebook",
                "description": "Tạo content Facebook, Instagram, TikTok với AI. Hoa hồng 30% recurring hàng tháng."
            },
            {
                "name": "Jasper AI",
                "affiliate_link": "https://jasper.ai/?ref=senv3",
                "commission_rate": 0.25,
                "is_recurring": True,
                "target_task_type": "content_facebook",
                "description": "AI Content Writer cao cấp, hoa hồng 25% recurring."
            },
            {
                "name": "HeyGen AI Video",
                "affiliate_link": "https://heygen.com/?ref=senv3",
                "commission_rate": 0.25,
                "is_recurring": True,
                "target_task_type": "video_tiktok",
                "description": "Tạo video TikTok với AI Avatar siêu thực, hoa hồng 25% recurring."
            },
            {
                "name": "Pictory.ai",
                "affiliate_link": "https://pictory.ai/?ref=senv3",
                "commission_rate": 0.20,
                "is_recurring": True,
                "target_task_type": "video_tiktok",
                "description": "Tự động tạo video từ script, hoa hồng 20% recurring."
            },
            {
                "name": "Scrapy Cloud",
                "affiliate_link": "https://scrapycloud.com/?aff=senv3",
                "commission_rate": 0.20,
                "is_recurring": False,
                "target_task_type": "scrape_deal",
                "description": "Công cụ scrape data tự động, hoa hồng 20% one-time."
            },
            {
                "name": "Octoparse",
                "affiliate_link": "https://octoparse.com/?ref=senv3",
                "commission_rate": 0.15,
                "is_recurring": False,
                "target_task_type": "scrape_deal",
                "description": "Web scraping không cần code, hoa hồng 15%."
            },
            {
                "name": "SEMrush",
                "affiliate_link": "https://semrush.com/?ref=senv3",
                "commission_rate": 0.20,
                "is_recurring": True,
                "target_task_type": "seo_article",
                "description": "SEO Tool chuyên nghiệp, hoa hồng 20% recurring."
            }
        ]
        
        products = []
        for p_data in products_data:
            product = AIAffiliateProduct(**p_data, total_clicks=0, total_conversions=0, total_revenue=0)
            db.add(product)
            products.append(product)
        
        db.flush()
        logger.info(f"✅ Created {len(products)} AI Affiliate Products")
        
        # 5. Tạo Tasks cho Members
        tasks_data = [
            # Tasks cho member_nguyen
            {"title": "Viết bài Facebook về AI Marketing", "task_type": "content_facebook", "assigned_to": members[0], "estimated_tokens": 3000, "expected_commission": 150},
            {"title": "Tạo video TikTok review sản phẩm", "task_type": "video_tiktok", "assigned_to": members[0], "estimated_tokens": 5000, "expected_commission": 200},
            {"title": "Scrape deals từ Amazon", "task_type": "scrape_deal", "assigned_to": members[0], "estimated_tokens": 2000, "expected_commission": 100},
            
            # Tasks cho member_tran
            {"title": "Content SEO cho blog Affiliate", "task_type": "seo_article", "assigned_to": members[1], "estimated_tokens": 4000, "expected_commission": 180},
            {"title": "Video TikTok trend", "task_type": "video_tiktok", "assigned_to": members[1], "estimated_tokens": 4500, "expected_commission": 190},
            
            # Tasks cho member_lee
            {"title": "Facebook post về ChatGPT", "task_type": "content_facebook", "assigned_to": members[2], "estimated_tokens": 2500, "expected_commission": 120},
            {"title": "Scrape data từ Shopee", "task_type": "scrape_deal", "assigned_to": members[2], "estimated_tokens": 3000, "expected_commission": 150},
            
            # Tasks cho member_pham
            {"title": "SEO article về Digital Marketing", "task_type": "seo_article", "assigned_to": members[3], "estimated_tokens": 3500, "expected_commission": 160},
            
            # Tasks cho member_hoang
            {"title": "TikTok video hướng dẫn AI tools", "task_type": "video_tiktok", "assigned_to": members[4], "estimated_tokens": 6000, "expected_commission": 250},
            {"title": "Facebook content về Affiliate Marketing", "task_type": "content_facebook", "assigned_to": members[4], "estimated_tokens": 2800, "expected_commission": 130},
        ]
        
        tasks = []
        for t_data in tasks_data:
            task = Task(
                title=t_data["title"],
                description=f"Task tự động từ hệ thống: {t_data['title']}",
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
        
        # 6. Tạo Commission Logs (hoa hồng đã thanh toán)
        commission_logs = [
            {"member": members[0], "task": tasks[0], "total": 150, "admin_rate": 0.10},
            {"member": members[0], "task": tasks[1], "total": 200, "admin_rate": 0.10},
            {"member": members[1], "task": tasks[3], "total": 180, "admin_rate": 0.10},
            {"member": members[2], "task": tasks[5], "total": 120, "admin_rate": 0.10},
            {"member": members[4], "task": tasks[8], "total": 250, "admin_rate": 0.10},
        ]
        
        for cl_data in commission_logs:
            admin_share = cl_data["total"] * cl_data["admin_rate"]
            member_share = cl_data["total"] - admin_share
            
            log = CommissionLog(
                member_id=cl_data["member"].id,
                task_id=cl_data["task"].id,
                total_commission=cl_data["total"],
                admin_share_amount=admin_share,
                member_share_amount=member_share,
                admin_rate=cl_data["admin_rate"],
                status="SETTLED",
                settled_at=datetime.utcnow(),
                created_at=datetime.utcnow() - timedelta(days=5)
            )
            db.add(log)
        
        db.flush()
        logger.info(f"✅ Created {len(commission_logs)} Commission Logs")
        
        # 7. Tạo Token Usage History
        token_histories = []
        for i, member in enumerate(members[:3]):  # Chỉ 3 members đầu
            for j in range(3):  # Mỗi member 3 lần sử dụng
                history = TokenUsageHistory(
                    user_id=member.id,
                    task_id=tasks[i*2 + j].id if (i*2 + j) < len(tasks) else None,
                    tokens_used=2000 + j * 500,
                    endpoint="/api/v1/ai/generate-content",
                    request_data=f'{{"prompt": "Generate content {j}"}}',
                    created_at=datetime.utcnow() - timedelta(days=j)
                )
                db.add(history)
                token_histories.append(history)
        
        db.flush()
        logger.info(f"✅ Created {len(token_histories)} Token Usage Histories")
        
        # 8. Cập nhật token đã sử dụng cho members
        for member in members[:3]:
            member.tokens_used = 15000  # Đã dùng 15k/50k tokens
            db.add(member)
        
        # Commit tất cả
        db.commit()
        
        # Hiển thị summary
        logger.info("\n" + "="*60)
        logger.info("🎉 DATABASE INITIALIZATION COMPLETE!")
        logger.info("="*60)
        logger.info(f"📊 Summary:")
        logger.info(f"   - Admins: 1")
        logger.info(f"   - Members: {len(members)}")
        logger.info(f"   - Regular Users: {len(regular_users)}")
        logger.info(f"   - AI Products: {len(products)}")
        logger.info(f"   - Tasks: {len(tasks)}")
        logger.info(f"   - Commission Logs: {len(commission_logs)}")
        logger.info(f"   - Token History: {len(token_histories)}")
        logger.info("="*60)
        
        # Hiển thị thông tin đăng nhập demo
        logger.info("\n🔐 Demo Accounts:")
        logger.info(f"   Admin:     username='admin_system'     password='Admin@123456'")
        logger.info(f"   Member:    username='member_nguyen'    password='Member@123456'")
        logger.info(f"   Member:    username='member_tran'      password='Member@123456'")
        logger.info(f"   Regular:   username='user_1'           password='User@123456'")
        logger.info("="*60)
        
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Error seeding data: {str(e)}")
        raise
    finally:
        db.close()

def reset_database():
    """Reset toàn bộ database (xóa và tạo lại)"""
    logger.info("⚠️ Resetting entire database...")
    drop_tables()
    create_tables()
    seed_demo_data()
    logger.info("✅ Database reset complete!")

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='SEN V3 Database Management')
    parser.add_argument('--action', choices=['create', 'drop', 'seed', 'reset'], 
                       default='create', help='Action to perform')
    parser.add_argument('--force', action='store_true', 
                       help='Force operation without confirmation')
    
    args = parser.parse_args()
    
    if args.action == 'create':
        create_tables()
        if not args.force:
            confirm = input("Seed demo data? (yes/no): ")
            if confirm.lower() == 'yes':
                seed_demo_data()
        else:
            seed_demo_data()
            
    elif args.action == 'drop':
        if args.force:
            drop_tables()
        else:
            confirm = input("⚠️ Confirm drop all tables? (yes/no): ")
            if confirm.lower() == 'yes':
                drop_tables()
                
    elif args.action == 'seed':
        seed_demo_data()
        
    elif args.action == 'reset':
        if args.force:
            reset_database()
        else:
            confirm = input("⚠️ Confirm reset database? This will DELETE ALL DATA! (yes/no): ")
            if confirm.lower() == 'yes':
                reset_database()

if __name__ == "__main__":
    main()