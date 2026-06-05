"""Check configuration and connectivity for SEN V3."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(".").resolve()))

from datetime import datetime

import jwt

from src.config import settings
from src.db.session import get_engine

ok = True

print("--- SEN V3 Configuration Check ---")
# 1. Env vars
required = ["DATABASE_URL", "JWT_SECRET_KEY", "ENCRYPTION_KEY"]
for k in required:
    v = getattr(settings, k, None)
    if not v:
        print(f"ERROR: Missing {k}")
        ok = False
    else:
        print(f"OK: {k} set")

# 2. CORS
print("CORS_ORIGINS:", settings.cors_origins)
if not settings.cors_origins:
    print("ERROR: No CORS origins configured")
    ok = False

# 3. DB connectivity
try:
    engine = get_engine()
    with engine.connect() as conn:
        conn.exec_driver_sql("SELECT 1")
        print("OK: DB connected:", engine.url)
except Exception as e:
    print("ERROR: DB connection failed:", e)
    ok = False

# 4. JWT token generation
try:
    payload = {"sub": "test", "iat": datetime.utcnow()}
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    decoded = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    print("OK: JWT encode/decode works")
except Exception as e:
    print("ERROR: JWT failed:", e)
    ok = False

# 5. Worker config
print("WORKER_POLL_INTERVAL_SECONDS=", settings.WORKER_POLL_INTERVAL_SECONDS)
print("MAX_CONCURRENT_WORKERS=", settings.MAX_CONCURRENT_WORKERS)

print("--- RESULT ---")
if ok:
    print("CONFIG CHECK PASSED")
    sys.exit(0)
else:
    print("CONFIG CHECK FAILED")
    sys.exit(2)
