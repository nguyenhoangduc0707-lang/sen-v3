from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt

app = FastAPI(title="SEN V3 API", docs_url="/api/v1/docs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage
tasks_db = []
next_id = 1

@app.get("/")
async def root():
    return {"message": "SEN V3 API (No DB Version)", "docs": "/api/v1/docs"}

@app.get("/api/v1/health")
async def health():
    return {"status": "ok", "time": datetime.now().isoformat()}

@app.get("/api/v1/tasks")
async def get_tasks():
    return {"tasks": tasks_db}

@app.post("/api/v1/tasks")
async def create_task(title: str, task_type: str = "generic", description: str = None):
    global next_id
    task = {
        "id": next_id,
        "title": title,
        "description": description,
        "task_type": task_type,
        "status": "pending",
        "created_at": datetime.now().isoformat()
    }
    tasks_db.append(task)
    next_id += 1
    return task

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/api/v1/auth/login")
async def login(login_data: LoginRequest):
    if login_data.username == "admin" and login_data.password == "admin":
        token_data = {"sub": login_data.username, "exp": datetime.utcnow() + timedelta(hours=1)}
        token = jwt.encode(token_data, "test-secret", algorithm="HS256")
        return {"access_token": token, "token_type": "bearer", "username": login_data.username}
    raise HTTPException(status_code=401, detail="Invalid credentials")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
