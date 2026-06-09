#!/usr/bin/env python3
"""Simple API runner - Using sync database to avoid MissingGreenlet"""

import os
import sys

# Force sync database
os.environ['DATABASE_URL'] = 'sqlite:///./app.db'

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting API server at http://0.0.0.0:8001")
    print("📚 Swagger UI: http://localhost:8001/docs")
    print("⚠️  Using SYNC database mode")
    uvicorn.run("web.main:app", host="0.0.0.0", port=8001, reload=True)
