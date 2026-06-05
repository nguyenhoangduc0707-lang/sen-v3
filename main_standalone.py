from config_global import config
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt
import hashlib
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, JSON
from sqlalchemy.sql import func

# ============ DATABASE SETUP ============
DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ============ MODELS ============
class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), default="pending")
    task_type = Column(String(100), nullable=False)
    config = Column(JSON, nullable=True)
    result = Column(JSON, nullable=True)
    created_by = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)

# Create tables
Base.metadata.create_all(bind=engine)

# ============ FASTAPI APP ============
app = FastAPI(title="SEN V3 API", version="0.1.0", docs_url="/api/v1/docs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============ HELPER FUNCTIONS ============
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    if hashed_password.startswith("simple:"):
        _, salt, hash_value = hashed_password.split(":")
        test_hash = hashlib.sha256((salt + plain_password).encode()).hexdigest()
        return test_hash == hash_value
    return False

# ============ ENDPOINTS ============
@app.get("/")
async def root():
    return {"message": "SEN V3 API", "docs": "/api/v1/docs"}

@app.get("/api/v1/health")
async def health():
    return {"status": "ok", "time": datetime.now().isoformat()}

@app.get("/api/v1/tasks")
async def get_tasks():
    db = SessionLocal()
    try:
        tasks = db.query(Task).all()
        return {"tasks": [{"id": t.id, "title": t.title, "status": t.status} for t in tasks]}
    finally:
        db.close()

@app.post("/api/v1/tasks")
async def create_task(title: str, task_type: str = "generic", description: str = None):
    db = SessionLocal()
    try:
        task = Task(title=title, task_type=task_type, description=description)
        db.add(task)
        db.commit()
        db.refresh(task)
        return {"id": task.id, "title": task.title, "status": task.status}
    finally:
        db.close()

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/api/v1/auth/login")
async def login(login_data: LoginRequest):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == login_data.username).first()
        if not user or not verify_password(login_data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Create token
        SECRET_KEY = "your-secret-key-change-me"
        token_data = {"sub": user.username, "exp": datetime.utcnow() + timedelta(hours=1)}
        token = jwt.encode(token_data, SECRET_KEY, algorithm="HS256")
        
        return {"access_token": token, "token_type": "bearer", "username": user.username}
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


