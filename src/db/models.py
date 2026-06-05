# src/db/models.py
"""
DYT_01 - Affiliate Campaign Database Models
Tích hợp Core Upgrade từ SEN V3
"""

from datetime import datetime
from enum import Enum
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, Enum as SQLEnum, Text
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
    """Task Queue - Mở rộng từ SEN V3"""
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    task_type = Column(String(100), nullable=False, comment="video_tiktok, content_facebook, scrape_deal")
    status = Column(String(50), default="PENDING", comment="PENDING, RUNNING, COMPLETED, FAILED, CANCELLED")
    priority = Column(Integer, default=1, comment="1: Thấp, 2: Trung bình, 3: Cao")
    
    assigned_to_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    estimated_tokens = Column(Integer, default=2000, comment="Token ước tính khi chạy")
    actual_tokens_used = Column(Integer, default=0, comment="Token thực tế đã dùng")
    
    # Commission tracking
    expected_commission = Column(Float, default=0.0, comment="Hoa hồng dự kiến")
    actual_commission = Column(Float, default=0.0, comment="Hoa hồng thực tế")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
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