from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, JSON
from sqlalchemy.sql import func
from src.db.session import Base

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), default="pending", index=True)  # pending, running, completed, failed
    task_type = Column(String(100), nullable=False, index=True)  # affiliate, ai_content, etc.
    config = Column(JSON, nullable=True)  # Lưu cấu hình task
    result = Column(JSON, nullable=True)  # Lưu kết quả
    
    created_by = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    is_active = Column(Boolean, default=True)
