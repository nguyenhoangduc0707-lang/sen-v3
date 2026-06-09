"""
DYT_01 - Affiliate Campaign Main Application
Real implementation - NO SIMULATION STUBS
"""

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
import logging
from contextlib import asynccontextmanager

from src.db.database import init_db
from src.db.models import User
from src.auth.jwt import get_current_user, get_current_user_optional

# Import routers directly (avoid __init__ cycles)
from web.routers.auth import router as auth_router
from web.routers.scheduler import router as scheduler_router
from web.routers.affiliate import router as affiliate_router

# Optional routers - import safely
try:
    from web.routers.commission import router as commission_router
except Exception:
    commission_router = None

try:
    from web.routers.member_dashboard import router as member_dashboard_router
except Exception:
    member_dashboard_router = None

try:
    from web.routers.ai_generate import router as ai_generate_router
except Exception:
    ai_generate_router = None

try:
    from web.routers.admin import router as admin_router
except Exception:
    admin_router = None

try:
    from web.routers.automation import router as automation_router
except Exception:
    automation_router = None

try:
    from web.routers.facebook_accounts import router as facebook_accounts_router
except Exception:
    facebook_accounts_router = None

try:
    from web.routers.posts import router as posts_router
except Exception:
    posts_router = None

try:
    from web.routers.content import router as content_router
except Exception:
    content_router = None

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events"""
    logger.info("🚀 Starting DYT-01 API (real endpoints only)...")
    init_db()
    logger.info("✅ Database initialized")
    yield
    logger.info("👋 Shutting down DYT-01 API...")


app = FastAPI(
    title="DYT-01 Affiliate Campaign System",
    description="Real API with DB-backed auth, scheduler, affiliate",
    version="3.1.0",
    lifespan=lifespan
)

# CORS - restricted to localhost only (per security requirements)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Register real routers (prefixes defined inside routers)
app.include_router(auth_router)          # /auth
app.include_router(scheduler_router)     # /schedules
app.include_router(affiliate_router)     # /affiliate

if commission_router:
    app.include_router(commission_router)
if member_dashboard_router:
    app.include_router(member_dashboard_router)
if ai_generate_router:
    app.include_router(ai_generate_router)
if admin_router:
    app.include_router(admin_router)
if automation_router:
    app.include_router(automation_router)
if facebook_accounts_router:
    app.include_router(facebook_accounts_router)
if posts_router:
    app.include_router(posts_router)

if content_router:
    app.include_router(content_router)


@app.get("/")
def root():
    return {
        "message": "DYT-01 Real API",
        "version": "3.1.0",
        "status": "operational",
        "documentation": "/docs"
    }


@app.get("/health")
def health_check():
    from datetime import datetime, timezone
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": "3.1.0"
    }


# Custom OpenAPI with Bearer auth
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="DYT-01 API",
        version="3.1.0",
        description=app.description,
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    openapi_schema["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("web.main:app", host="0.0.0.0", port=8001, reload=True, log_level="info")
