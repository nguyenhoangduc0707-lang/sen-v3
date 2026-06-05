"""
==========================================================================================
DỰ ÁN: SEN V3 INTERNAL ECOSYSTEM - CORE UPGRADE BLUEPRINT
MỤC TIÊU CHO AI DEVELOPER TIẾP THEO: 
1. Hiện thực hóa hệ thống phân chia hoa hồng tự động giữa Admin và Member.
2. Tích hợp phễu Affiliate AI (Gợi ý công cụ có tính năng ăn % gia hạn trọn đời cho Admin).
3. Quản lý hạn mức Token sử dụng hệ thống của từng Member nhằm tối ưu chi phí API Gemini.
4. Xây dựng phân quyền dữ liệu nghiêm ngặt giữa các cấp độ tài khoản: Admin, Member, User.

VỊ TRÍ TÍCH HỢP TRONG SOURCE CODE HIỆN TẠI:
- Các Model SQLAlchemy cần được bóc tách và chuyển vào: `src/db/models.py`
- Các Router API cần được đăng ký vào hệ thống FastAPI tại: `web/main.py` hoặc `web/routers/`
==========================================================================================
"""

import os
from enum import Enum
from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel, Field
from fastapi import FastAPI, Depends, HTTPException, status, Header
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime, Boolean, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship

# ==========================================
# 1. CẤU TRÚC DATABASE & PHÂN QUYỀN (SQLAlchemy)
# ==========================================

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sen_v3.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class UserRole(str, Enum):
    ADMIN = "admin"
    MEMBER = "member"
    USER_KHOAHOC = "user_khoahoc"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.USER_KHOAHOC, nullable=False)
    
    # Quản lý Token (Rate Limiting)
    token_quota = Column(Integer, default=50000)  # Số lượng token tối đa được cấp
    tokens_used = Column(Integer, default=0)       # Số lượng token đã tiêu thụ
    
    # Liên kết phân cấp (Member thuộc sự quản lý của Admin nào)
    parent_admin_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Quan hệ dữ liệu
    tasks = relationship("Task", back_populates="assigned_to")
    commission_logs = relationship("CommissionLog", back_populates="member")

class AIAffiliateProduct(Base):
    """Bảng lưu trữ các công cụ AI chứa link tiếp thị liên kết của Admin"""
    __tablename__ = "ai_affiliate_products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)        # Ví dụ: Writesonic, Jasper, HeyGen
    affiliate_link = Column(String, nullable=False)           # Link Affiliate của riêng Admin
    commission_rate = Column(Float, nullable=False)           # % hoa hồng nhận được khi Member gia hạn
    is_recurring = Column(Boolean, default=True)              # Hoa hồng gia hạn trọn đời/định kỳ
    target_task_type = Column(String, nullable=False)         # Gợi ý dựa trên loại task (Ví dụ: "video", "content")
    description = Column(String)

class Task(Base):
    """Hàng đợi nhiệm vụ mở rộng từ cấu trúc Task Queue gốc của SEN V3"""
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    task_type = Column(String, nullable=False)                # "video_tiktok", "content_facebook", "scrape_deal"
    status = Column(String, default="PENDING")                # PENDING, RUNNING, COMPLETED, FAILED
    assigned_to_id = Column(Integer, ForeignKey("users.id"))
    estimated_tokens = Column(Integer, default=2000)          # Ước tính số token tiêu tốn khi dùng Gemini
    
    assigned_to = relationship("User", back_populates="tasks")

class CommissionLog(Base):
    """Bảng kiểm soát doanh thu và tự động phân tách lợi nhuận thực tế"""
    __tablename__ = "commission_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    
    total_commission = Column(Float, nullable=False)          # Tổng hoa hồng chiến dịch thu về từ AccessTrade/Shopify
    admin_share_amount = Column(Float, nullable=False)        # Số tiền cắt lại cho Admin hệ thống
    member_share_amount = Column(Float, nullable=False)       # Số tiền thực tế chia cho Member làm task
    
    status = Column(String, default="PENDING_SETTLEMENT")     # Trạng thái đối soát dòng tiền
    created_at = Column(DateTime, default=datetime.utcnow)
    
    member = relationship("User", back_populates="commission_logs")

# ==========================================
# PANYDANTIC SCHEMAS FOR API VALIDATION
# ==========================================
class TaskCompleteRequest(BaseModel):
    total_commission: float = Field(..., gt=0, description="Tổng số tiền hoa hồng ghi nhận từ hệ thống Affiliate gốc")
    admin_override_rate: Optional[float] = Field(None, description="Tỷ lệ Admin muốn điều chỉnh riêng cho task này (Ví dụ: 0.15 cho 15%)")

# ==========================================
# DEPENDENCIES & CORE UTILITIES
# ==========================================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Giả lập hàm kiểm tra Auth JWT từ hệ thống SEN V3 gốc
# AI Developer tiếp theo cần thay thế bằng dependency thực tế tại `src/auth/jwt.py`
def get_current_user(x_user_id: int = Header(...), db: Session = Depends(get_db)) -> User:
    user = db.query(User).filter(User.id == x_user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Xác thực người dùng thất bại")
    return user

# ==========================================
# INITIALIZE FASTAPI CORE UPGRADE APPLICATION
# ==========================================
app = FastAPI(title="SEN V3 Core - Admin & Member Subsystem", version="3.1.0")

# ==========================================
# 2. LOGIC TÍNH TOÁN HOA HỒNG (PROFIT SPLIT)
# ==========================================

@app.post("/api/v1/tasks/{task_id}/complete", tags=["Commission & Tasks"])
def complete_task_and_split_profit(
    task_id: int, 
    payload: TaskCompleteRequest, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """
    Xử lý hoàn thành task và tự động phân tách dòng tiền giữa Admin và Member.
    Tỷ lệ hoa hồng mặc định Admin hưởng thu nhập thụ động là 10% trên tổng số hoa hồng Member làm ra.
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Không tìm thấy thông tin Task")
        
    # Phân quyền bảo mật: Chỉ cho phép Member được giao task hoặc Admin hệ thống cập nhật hoàn thành
    if current_user.role != UserRole.ADMIN and task.assigned_to_id != current_user.id:
        raise HTTPException(status_code=403, detail="Bạn không có quyền cập nhật trạng thái của Task này")
        
    # Xác định tỷ lệ trích hoa hồng cho Admin (Mặc định hệ thống là 10% = 0.10)
    admin_rate = payload.admin_override_rate if payload.admin_override_rate is not None else 0.10
    
    # Thực hiện thuật toán chia dòng tiền
    admin_share = payload.total_commission * admin_rate
    member_share = payload.total_commission - admin_share
    
    # Cập nhật trạng thái Task trong Queue
    task.status = "COMPLETED"
    
    # Ghi nhận lịch sử dòng tiền vào hệ thống đối soát tổng của Admin
    log = CommissionLog(
        member_id=task.assigned_to_id,
        task_id=task.id,
        total_commission=payload.total_commission,
        admin_share_amount=admin_share,
        member_share_amount=member_share,
        status="SETTLED"
    )
    
    db.add(log)
    db.commit()
    db.refresh(log)
    
    return {
        "status": "Success",
        "task_id": task.id,
        "distribution": {
            "total_received": payload.total_commission,
            "admin_passive_income": admin_share,
            "member_net_income": member_share,
            "applied_rate": admin_rate
        }
    }

# ==========================================
# 3. CHIẾN LƯỢC "ADMIN AI MARKETING" (Smart Suggestion)
# ==========================================

@app.get("/api/v1/member/dashboard", tags=["Member Interface"])
def get_member_dashboard_with_ai_suggestions(
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """
    Giao diện Dashboard của Member: Hiển thị các task được giao đồng thời quét các Task sắp tới 
    để tự động đẩy link tiếp thị liên kết (Affiliate Recurring) các công cụ AI của Admin lên màn hình.
    """
    if current_user.role != UserRole.MEMBER:
        raise HTTPException(status_code=403, detail="Giao diện này chỉ dành riêng cho tài khoản cấp độ Member")
        
    # Lấy danh sách task đang chờ xử lý của Member
    pending_tasks = db.query(Task).filter(Task.assigned_to_id == current_user.id, Task.status == "PENDING").all()
    
    # Thu thập các dạng công việc (Task types) đang có trong danh sách đợi
    active_task_types = set([task.task_type for task in pending_tasks])
    
    # Hệ thống AI thông minh tự động quét các sản phẩm bổ trợ tối ưu có sẵn link Affiliate của Admin
    ai_suggestions = []
    for task_type in active_task_types:
        products = db.query(AIAffiliateProduct).filter(AIAffiliateProduct.target_task_type == task_type).all()
        for prod in products:
            ai_suggestions.append({
                "notice": f"Hệ thống phát hiện bạn có Task dạng '{task_type}'. Hãy sử dụng công cụ sau để tăng tốc 5x hiệu suất làm việc!",
                "tool_name": prod.name,
                "recommended_link": prod.affiliate_link,
                "benefit_description": prod.description,
                "is_recurring_bonus": prod.is_recurring
            })
            
    return {
        "member_info": {"id": current_user.id, "username": current_user.username},
        "assigned_pending_tasks_count": len(pending_tasks),
        "admin_smart_ai_recommendations": ai_suggestions
    }

# ==========================================
# 4. GIỚI HẠN TOKEN CHO MEMBER (Rate Limiting Middleware)
# ==========================================

@app.post("/api/v1/ai/generate-content", tags=["AI Processing Engine"])
def generate_affiliate_content_with_token_check(
    prompt: str, 
    task_id: int, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """
    Cổng xử lý AI Content (Gọi tới bộ não Gemini). 
    Tích hợp Middleware kiểm tra chặt chẽ hạn mức Token còn lại của Member trước khi cho phép kích hoạt API tốn phí.
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    estimated_cost = task.estimated_tokens if task else 2000
    
    # Thuật toán kiểm soát hạn mức (Rate limit) bằng token cứng trong DB nhằm bảo vệ tài khoản API của Admin
    available_tokens = current_user.token_quota - current_user.tokens_used
    if available_tokens < estimated_cost:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED, 
            detail=f"Hết hạn mức tài nguyên! Cần {estimated_cost} tokens nhưng tài khoản chỉ còn {available_tokens} tokens. Vui lòng liên hệ Admin để nâng cấp hạn mức hoặc sử dụng link AI gợi ý trên hệ thống để tự vận hành độc lập."
        )
        
    # Giả lập luồng kích hoạt Gemini Agent sinh nội dung thành công (Ứng với file `content_creation_agent.py`)
    # Logic thực tế sẽ gọi hàm: `content_creation_agent.generate_with_gemini(prompt)`
    simulated_gemini_response = f"[SEN V3 AI GENED] Bài viết Affiliate tự động tối ưu hóa cấu trúc cho prompt: '{prompt}'"
    
    # Thực hiện trừ hạn mức Token của Member ngay sau khi xử lý thành công
    current_user.tokens_used += estimated_cost
    db.commit()
    
    return {
        "status": "Success",
        "generated_content": simulated_gemini_response,
        "resource_consumption": {
            "tokens_deducted": estimated_cost,
            "remaining_tokens": current_user.token_quota - current_user.tokens_used
        }
    }

# Lệnh khởi chạy và tạo cấu trúc bảng nhanh để kiểm thử
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("🚀 [SEN V3 CRITICAL UPDATE] Cấu trúc Database đã được đồng bộ hóa thành công!")
    print("💡 Mẹo dành cho AI Dev: Chạy lệnh 'uvicorn sen_v3_core_upgrade:app --reload' để khởi chạy máy chủ API thử nghiệm.")