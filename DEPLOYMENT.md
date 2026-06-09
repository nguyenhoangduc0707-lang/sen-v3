# DYT-01 Deployment Guide

## Development (Local)

See README.md → Quick Start.

## Production Recommendations

### Using Docker Compose (Recommended for quick start)

We provide a ready-to-use `docker-compose.yml`:

```bash
# 1. Copy and configure environment
cp .env.example .env
# Edit .env with real secrets + set DATABASE_URL for Postgres

# 2. Build and run
docker-compose up -d --build

# 3. Check logs
docker-compose logs -f api scheduler worker-facebook
```

See the `docker-compose.yml` file in the root for the full stack (API + 3 workers + Postgres).

### 1. Environment (non-Docker)

- Use PostgreSQL instead of SQLite (`DATABASE_URL=postgresql+asyncpg://...`)
- Set strong secrets:
  - `FERNET_KEY` (32-byte base64)
  - `JWT_SECRET_KEY` (≥32 chars, random)
- Disable reload: `python start.py api --no-reload`

### 2. Running in Production

Recommended: Use separate processes or Docker.

**Option A: Systemd / Supervisor**
- One service for API
- One or more for workers (`--type facebook`, `--type affiliate`)
- One for scheduler

**Option B: Docker Compose** (example)

```yaml
version: "3.8"
services:
  api:
    build: .
    command: python start.py api --no-reload
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql+asyncpg://...
      - FERNET_KEY=...
  worker-facebook:
    build: .
    command: python start.py worker --type facebook
  worker-affiliate:
    build: .
    command: python start.py worker --type affiliate
  scheduler:
    build: .
    command: python start.py scheduler
```

### 3. Database

- Run migrations: `alembic upgrade head`
- Regular backups of `sen_v3.db` (or Postgres dump)
- Consider connection pool tuning in `src/db/database.py` or `task_queue_db_async.py`

### 4. Security

- Never commit real `.env`, `facebook_auth*.json`, or cookies
- Use HTTPS in production (reverse proxy: Nginx / Caddy)
- Restrict CORS to your frontend domain only
- Rotate Facebook tokens regularly (the worker supports auto-refresh)

### 5. Monitoring (Basic)

- Health: `GET /health`
- Queue status: `GET /api/v1/queue/tasks`
- Add Prometheus metrics later (see Priority 3)

### 6. Scaling Tips

- Run multiple worker instances for the same type (they all pull from the same async queue)
- Increase `MAX_CONCURRENT_WORKERS` in config
- Use PostgreSQL + proper indexing on `scheduled_at`, `status`, `priority`

---

**Current recommended stack (after Phase 4):**
- Python 3.11+
- PostgreSQL 15+
- Async workers + Scheduler
- Uvicorn (or Gunicorn + Uvicorn workers)
- Reverse proxy in front

The system is now clean, documented, and ready for production deployment.
