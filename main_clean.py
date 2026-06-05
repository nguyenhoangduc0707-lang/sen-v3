import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional, List
from dotenv import load_dotenv
import jwt
import hashlib
import secrets

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="SEN V3 API",
    version="1.0.0",
    description="Secure API for DYT_01 project",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    openapi_url="/api/v1/openapi.json"
)

# CORS configuration
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:8000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
SECRET_KEY = os.getenv("JWT_SECRET_KEY", os.getenv("SECRET_KEY", "change-this-in-production"))

# In-memory storage (replace with database in production)
tasks_db = []
users_db = [
    {
        "username": "admin",
        "password_hash": hashlib.sha256(("salt" + "admin").encode()).hexdigest()
    }
]

# ============ MODELS ============
class Task(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    task_type: str = "generic"
    status: str = "pending"
    created_at: Optional[datetime] = None

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# ============ HELPER FUNCTIONS ============
def create_token(username: str) -> str:
    """Create JWT token"""
    expiration = datetime.utcnow() + timedelta(hours=1)
    payload = {"sub": username, "exp": expiration}
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_password(username: str, password: str) -> bool:
    """Verify user credentials"""
    # Simple hash for demo (use bcrypt in production)
    expected_hash = hashlib.sha256(("salt" + password).encode()).hexdigest()
    for user in users_db:
        if user["username"] == username and user["password_hash"] == expected_hash:
            return True
    return False

# ============ ENDPOINTS ============
@app.get("/")
async def root():
    return {
        "message": "SEN V3 API",
        "version": "1.0.0",
        "docs": "/api/v1/docs",
        "status": "running"
    }

@app.get("/api/v1/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/api/v1/tasks", response_model=List[Task])
async def get_tasks():
    """Get all tasks"""
    return tasks_db

@app.post("/api/v1/tasks", response_model=Task)
async def create_task(title: str, task_type: str = "generic", description: str = None):
    """Create a new task"""
    new_task = Task(
        id=len(tasks_db) + 1,
        title=title,
        description=description,
        task_type=task_type,
        created_at=datetime.now()
    )
    tasks_db.append(new_task)
    return new_task

@app.post("/api/v1/auth/login", response_model=TokenResponse)
async def login(login_data: LoginRequest):
    """Login endpoint"""
    if not verify_password(login_data.username, login_data.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_token(login_data.username)
    return TokenResponse(access_token=token)

# Run server
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    uvicorn.run(app, host=host, port=port, reload=DEBUG)
