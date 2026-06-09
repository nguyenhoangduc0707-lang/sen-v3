"""
CRUD helpers for new PHASE 1/2/3 models
"""

from sqlalchemy.orm import Session
from src.db.models import User, FacebookAccount, ScheduledTask, AffiliateLink
from src.utils.encryption import encryption
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def create_admin_user(db: Session, email: str, password: str, full_name: str = "System Admin"):
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    existing = db.query(User).filter(User.email == email).first()
    if existing:
        logger.info(f"Admin user {email} already exists")
        return existing

    admin = User(
        username=email.split("@")[0],
        email=email,
        hashed_password=pwd_context.hash(password),
        full_name=full_name,
        role="admin",
        is_active=True,
        token_quota=1_000_000,
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    logger.info(f"✅ Created admin user: {email}")
    return admin


def create_facebook_account(
    db: Session,
    user_id: int,
    page_id: str,
    page_name: str,
    access_token: str,
    app_id: str = None,
    app_secret: str = None,
    token_expires_at: datetime = None,
) -> FacebookAccount:
    existing = db.query(FacebookAccount).filter(FacebookAccount.page_id == page_id).first()
    if existing:
        existing.access_token_encrypted = encryption.encrypt(access_token)
        existing.page_name = page_name
        if app_id:
            existing.app_id_encrypted = encryption.encrypt(app_id)
        if app_secret:
            existing.app_secret_encrypted = encryption.encrypt(app_secret)
        if token_expires_at:
            existing.token_expires_at = token_expires_at
        existing.is_active = True
        existing.is_verified = True
        existing.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(existing)
        logger.info(f"✅ Updated Facebook page: {page_name} ({page_id})")
        return existing

    fb_account = FacebookAccount(
        user_id=user_id,
        page_id=page_id,
        page_name=page_name,
        access_token_encrypted=encryption.encrypt(access_token),
        app_id_encrypted=encryption.encrypt(app_id) if app_id else None,
        app_secret_encrypted=encryption.encrypt(app_secret) if app_secret else None,
        token_expires_at=token_expires_at,
        is_active=True,
        is_verified=True,
    )
    db.add(fb_account)
    db.commit()
    db.refresh(fb_account)
    logger.info(f"✅ Added Facebook page: {page_name} ({page_id})")
    return fb_account


def create_scheduled_task(
    db: Session,
    task_type: str,
    data: dict,
    scheduled_at: datetime,
    created_by: int,
    priority: int = 0,
) -> ScheduledTask:
    st = ScheduledTask(
        task_type=task_type,
        data=data,
        scheduled_at=scheduled_at,
        created_by=created_by,
        priority=priority,
        is_active=True,
        is_processed=False,
    )
    db.add(st)
    db.commit()
    db.refresh(st)
    logger.info(f"✅ Created scheduled_task #{st.id} for {scheduled_at}")
    return st
