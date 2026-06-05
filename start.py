from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="SEN V3 Core API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "SEN V3 Core API is running!", "status": "ok", "port": 8001}

@app.get("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    print("🚀 Server starting at http://localhost:8001")
    print("📖 API Docs: http://localhost:8001/docs")
    uvicorn.run(app, host="127.0.0.1", port=8001)
