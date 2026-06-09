# src/db/models.py
"""
DYT_01 - Affiliate Campaign Database Models
Tích hợp Core Upgrade từ SEN V3
"""

from datetime import datetime
from enum import Enum
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, Enum as SQLEnum, Text, JSON
from sqlalchemy.orm import relationship
from src.db.database import Base

class UserRole(str, Enum):
    """Phân cấp tài khoản hệ thống"""
    ADMIN = "admin"
    MEMBER = "member"
    USER_KHOAHOC = "user_khoahoc"

class User(Base):
    """Bảng Users - Mở rộng từ hệ thống gốc"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(200), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    role = Column(SQLEnum(UserRole), default=UserRole.USER_KHOAHOC, nullable=False)
    
    # Token Management (Từ Core Upgrade)
    token_quota = Column(Integer, default=50000, comment="Số token tối đa được cấp")
    tokens_used = Column(Integer, default=0, comment="Số token đã tiêu thụ")
    token_reset_date = Column(DateTime, default=datetime.utcnow, comment="Ngày reset quota")
    
    # Hierarchical Management
    parent_admin_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    tasks = relationship("Task", back_populates="assigned_to", cascade="all, delete-orphan")
    commission_logs = relationship("CommissionLog", back_populates="member", cascade="all, delete-orphan")
    parent_admin = relationship("User", remote_side=[id], backref="members")
    # Temporarily commented to fix mapper configuration error for UAT
    # facebook_accounts = relationship("FacebookAccount", back_populates="user", cascade="all, delete-orphan")
    # affiliate_links = relationship("AffiliateLink", back_populates="user", cascade="all, delete-orphan")
    
    @property
    def available_tokens(self) -> int:
        """Tính số token còn lại"""
        return self.token_quota - self.tokens_used
    
    @property
    def token_usage_percent(self) -> float:
        """Phần trăm token đã sử dụng"""
        if self.token_quota == 0:
            return 0.0
        return (self.tokens_used / self.token_quota) * 100


class AIAffiliateProduct(Base):
    """Sản phẩm AI Affiliate - Tạo passive income cho Admin"""
    __tablename__ = "ai_affiliate_products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), unique=True, nullable=False, comment="Tên công cụ AI")
    affiliate_link = Column(String(500), nullable=False, comment="Link affiliate của Admin")
    commission_rate = Column(Float, default=0.20, comment="% hoa hồng")
    is_recurring = Column(Boolean, default=True, comment="Hoa hồng định kỳ trọn đời")
    target_task_type = Column(String(100), nullable=False, comment="Loại task phù hợp")
    description = Column(Text, comment="Mô tả chi tiết")
    
    # Thống kê
    total_clicks = Column(Integer, default=0)
    total_conversions = Column(Integer, default=0)
    total_revenue = Column(Float, default=0.0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)


class Task(Base):
    """Task Queue - Mở rộng từ SEN V3 (supports both business tasks + generic queue)"""
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=True)  # Made optional for pure queue tasks
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=True)  # For queue categorization
    task_type = Column(String(100), nullable=True, comment="video_tiktok, content_facebook, ... or null for generic")
    status = Column(String(50), default="PENDING", comment="PENDING, RUNNING, COMPLETED, FAILED, CANCELLED")
    priority = Column(Integer, default=1, comment="1: Thấp, 2: Trung bình, 3: Cao")
    
    # Queue-specific fields (used by TaskQueueDB)
    worker_name = Column(String(100), nullable=True)
    payload = Column(Text, nullable=True)  # JSON serialized payload
    retries = Column(Integer, default=0)
    last_error = Column(Text, nullable=True)
    
    assigned_to_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    estimated_tokens = Column(Integer, default=2000, comment="Token ước tính khi chạy")
    actual_tokens_used = Column(Integer, default=0, comment="Token thực tế đã dùng")
    
    # Commission tracking
    expected_commission = Column(Float, default=0.0, comment="Hoa hồng dự kiến")
    actual_commission = Column(Float, default=0.0, comment="Hoa hồng thực tế")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    finished_at = Column(DateTime, nullable=True)  # renamed from completed_at for queue compat
    completed_at = Column(DateTime, nullable=True)
    
    assigned_to = relationship("User", back_populates="tasks")
    
    @property
    def processing_time(self) -> float:
        """Thời gian xử lý task (giây)"""
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return 0.0


class CommissionLog(Base):
    """Log phân chia hoa hồng tự động"""
    __tablename__ = "commission_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    
    # Financial tracking
    total_commission = Column(Float, nullable=False, comment="Tổng hoa hồng từ chiến dịch")
    admin_share_amount = Column(Float, nullable=False, comment="Phần của Admin (passive income)")
    member_share_amount = Column(Float, nullable=False, comment="Phần của Member (active income)")
    admin_rate = Column(Float, default=0.10, comment="Tỷ lệ Admin hưởng")
    
    # Status tracking
    status = Column(String(50), default="PENDING_SETTLEMENT", comment="PENDING, SETTLED, CANCELLED")
    transaction_id = Column(String(100), nullable=True, comment="Mã giao dịch từ payment gateway")
    
    # Metadata
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    settled_at = Column(DateTime, nullable=True)
    
    member = relationship("User", back_populates="commission_logs")
    task = relationship("Task")
    
    @property
    def admin_percent(self) -> float:
        return self.admin_rate * 100
    
    @property
    def member_percent(self) -> float:
        return (1 - self.admin_rate) * 100


class TokenUsageHistory(Base):
    """Lịch sử sử dụng token - Để audit và báo cáo"""
    __tablename__ = "token_usage_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    tokens_used = Column(Integer, nullable=False)
    endpoint = Column(String(200), comment="API endpoint được gọi")
    request_data = Column(Text, comment="Dữ liệu request (JSON)")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User")
    task = relationship("Task")


# ==================== QUEUE SYSTEM MODELS (for TaskQueueDB / orchestrator) ====================

class Worker(Base):
    """Registered worker heartbeat/status"""
    __tablename__ = "workers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    version = Column(String(50), default="1.0")
    status = Column(String(20), default="ACTIVE")  # ACTIVE, IDLE, STOPPED
    last_heartbeat = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)


class ExecutionLog(Base):
    """Log of worker executions"""
    __tablename__ = "execution_logs"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    worker_name = Column(String(100), nullable=True)
    log_level = Column(String(20), default="INFO")
    message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class DeadLetter(Base):
    """Failed tasks that exceeded retries"""
    __tablename__ = "dead_letters"

    id = Column(Integer, primary_key=True, index=True)
    original_task_id = Column(Integer, nullable=True)
    category = Column(String(100), nullable=True)
    worker_name = Column(String(100), nullable=True)
    payload = Column(Text)  # JSON string
    failure_reason = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


# ==================== AUTOMATION SYSTEM ====================
# For cutting down on repetitive tasks: route tasks, update statuses, send notifications
# Supports templates and no-code rules (JSON conditions/actions)

class AutomationTemplate(Base):
    """Pre-built automation templates for common workflows"""
    __tablename__ = "automation_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=True)  # e.g. "task_routing", "notification", "content"
    trigger = Column(String(100), nullable=False)  # "task.created", "task.failed", etc.
    conditions = Column(Text, nullable=True)  # JSON example conditions
    actions = Column(Text, nullable=False)  # JSON list of actions
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class AutomationRule(Base):
    """User-defined automation rules (no-code)"""
    __tablename__ = "automation_rules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    trigger = Column(String(100), nullable=False)  # e.g. "task.created"
    conditions = Column(Text, nullable=True)  # JSON array of conditions: [{"field": "category", "op": "equals", "value": "content"}]
    actions = Column(Text, nullable=False)  # JSON array of actions: [{"type": "set_worker", "value": "content_creator"}, {"type": "notify", "channel": "email", "to": "admin"}]
    enabled = Column(Boolean, default=True)
    priority = Column(Integer, default=10)  # lower = higher priority
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_triggered_at = Column(DateTime, nullable=True)
    trigger_count = Column(Integer, default=0)

    created_by = relationship("User", foreign_keys=[created_by_id])


class AutomationLog(Base):
    """Log of automation executions for auditing"""
    __tablename__ = "automation_logs"

    id = Column(Integer, primary_key=True, index=True)
    rule_id = Column(Integer, ForeignKey("automation_rules.id"), nullable=True)
    template_id = Column(Integer, ForeignKey("automation_templates.id"), nullable=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    trigger = Column(String(100))
    status = Column(String(50), default="success")  # success, failed, skipped
    details = Column(Text, nullable=True)  # JSON or message
    executed_at = Column(DateTime, default=datetime.utcnow)


# ==================== LEGACY COMPATIBILITY MODELS ====================
# These support older/standalone scripts and the FacebookAutoPoster raw SQL paths
# (e.g. direct lookup by post_id in facebook_posts table). The core Task queue is preferred.

class FacebookPost(Base):
    """Legacy table for Facebook posts (used by facebook_autoposter.py raw queries and many root scripts).
    Adding this model ensures Base.metadata.create_all creates the table when using the core DB init.
    """
    __tablename__ = "facebook_posts"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=True)
    media_path = Column(String(500), nullable=True)
    media_type = Column(String(50), nullable=True)  # image, video, etc.

    status = Column(String(50), default="pending", index=True)  # pending, posted, failed
    post_url = Column(String(500), nullable=True)
    error_message = Column(Text, nullable=True)

    fanpage_key = Column(String(100), nullable=True)
    fanpage_url = Column(String(500), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    scheduled_at = Column(DateTime, nullable=True)

    # Optional link back to the new unified Task system
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)


# ==================== PHASE 1/3 MODELS ====================

class FacebookAccount(Base):
    """Encrypted storage for Facebook Page access"""
    __tablename__ = "facebook_accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    page_id = Column(String(100), nullable=False, index=True)
    page_name = Column(String(200))
    page_category = Column(String(100))
    access_token_encrypted = Column(String(500), nullable=False)
    token_expires_at = Column(DateTime)
    app_id_encrypted = Column(String(100))
    app_secret_encrypted = Column(String(100))
    cookies_encrypted = Column(Text)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    last_used_at = Column(DateTime)
    last_error = Column(Text)
    usage_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", backref="facebook_accounts")


class ScheduledTask(Base):
    """Scheduled tasks that the SchedulerWorker will pick up and enqueue"""
    __tablename__ = "scheduled_tasks"

    id = Column(Integer, primary_key=True, index=True)
    task_type = Column(String(50), nullable=False)
    data = Column(JSON, nullable=False)
    scheduled_at = Column(DateTime, nullable=False, index=True)
    is_processed = Column(Boolean, default=False, index=True)
    is_active = Column(Boolean, default=True)
    priority = Column(Integer, default=0)
    created_by = Column(Integer, ForeignKey("users.id"))
    processed_at = Column(DateTime)
    task_id = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    creator = relationship("User", foreign_keys=[created_by])


class AffiliateLink(Base):
    """Tracking for generated affiliate links"""
    __tablename__ = "affiliate_links"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    product_id = Column(String(100))
    product_name = Column(String(500))
    campaign_id = Column(String(100))
    original_url = Column(String(1000))
    affiliate_url = Column(String(1000))
    short_code = Column(String(50), unique=True, index=True)
    clicks = Column(Integer, default=0)
    conversions = Column(Integer, default=0)
    commission_earned = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)
    last_clicked_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", backref="affiliate_links")

# Fix for relationship mappers (added during UAT fix)
from sqlalchemy.orm import configure_mappers
configure_mappers()

