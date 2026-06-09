import os
os.environ["DATABASE_URL"] = "sqlite:///./app.db"

if __name__ == "__main__":
    import uvicorn
    print("=" * 50)
    print("?? DYT-01 API Server (FIXED)")
    print("=" * 50)
    print("?? Swagger UI: http://localhost:8001/docs")
    print("?? Health: http://localhost:8001/health")
    print("=" * 50)
    uvicorn.run("web.main:app", host="0.0.0.0", port=8001, reload=True)
