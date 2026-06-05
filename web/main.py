# web/main.py
"""
DYT_01 - Affiliate Campaign Main Application
Tích hợp Core Upgrade SEN V3
"""

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
import logging
from contextlib import asynccontextmanager

from src.db.database import init_db, get_db
from src.db.models import User
from src.auth.jwt import get_current_user

# Import routers
from web.routers import (
    auth,
    commission,
    member_dashboard,
    ai_generate,
    admin
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Xử lý startup và shutdown events"""
    # Startup
    logger.info("🚀 Starting SEN V3 Core API...")
    init_db()
    logger.info("✅ Database initialized")
    yield
    # Shutdown
    logger.info("👋 Shutting down SEN V3 Core API...")

# Create FastAPI app
app = FastAPI(
    title="SEN V3 Core - Affiliate Campaign System",
    description="""
    ## Hệ thống quản lý Affiliate Campaign với AI Integration
    
    ### 🎯 Core Features:
    - **Tự động phân chia hoa hồng** giữa Admin (passive income) và Member (active income)
    - **Phễu Affiliate AI** gợi ý công cụ giúp Admin ăn hoa hồng trọn đời
    - **Quản lý Token thông minh** tối ưu chi phí Gemini API
    - **Phân quyền dữ liệu nghiêm ngặt** Admin > Member > User
    
    ### 📊 Commission Structure:
    - Mặc định: Admin 10% | Member 90%
    - Hỗ trợ điều chỉnh tỷ lệ linh hoạt
    - Ghi nhận hoa hồng recurring từ affiliate tools
    
    ### 🔐 Authentication:
    - Sử dụng JWT Bearer token
    - Gửi token trong Header: `Authorization: Bearer <your_token>`
    
    ### 💰 Token System:
    - Member được cấp quota token (mặc định 50,000)
    - Mỗi lần gọi Gemini API sẽ trừ token
    - Admin có thể nạp thêm token khi cần
    """,
    version="3.1.0",
    contact={
        "name": "SEN V3 Support",
        "email": "support@senv3.com",
    },
    license_info={
        "name": "Proprietary",
    },
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cấu hình cụ thể trong production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth.router)
app.include_router(commission.router)
app.include_router(member_dashboard.router)
app.include_router(ai_generate.router)
app.include_router(admin.router)

# ========== ROOT ENDPOINTS ==========
@app.get("/")
def root():
    """Welcome endpoint"""
    return {
        "message": "Welcome to SEN V3 Core - Affiliate Campaign System",
        "version": "3.1.0",
        "status": "operational",
        "documentation": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z"  # Will be dynamic
    }

@app.get("/api/v1/info")
def system_info(current_user: User = Depends(get_current_user)):
    """Lấy thông tin hệ thống (yêu cầu authentication)"""
    return {
        "system": "SEN V3 Core",
        "version": "3.1.0",
        "user_role": current_user.role.value,
        "features": [
            "Auto Commission Split",
            "AI Affiliate Funnel",
            "Token Management",
            "Role-based Access Control"
        ]
    }

# Custom OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="SEN V3 Core API",
        version="3.1.0",
        description=app.description,
        routes=app.routes,
    )
    
    # Add security scheme
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    
    # Apply security globally
    openapi_schema["security"] = [{"BearerAuth": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# ========== RUN SERVER ==========
if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "web.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )