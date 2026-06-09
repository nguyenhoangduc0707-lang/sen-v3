# DYT-01 / SEN V3 - Affiliate Campaign Automation System

Modern, secure, async-first marketing automation platform for affiliate networks + social media posting (Facebook, TikTok, etc.).

## Features

- **Core Workers**
  - Facebook Worker (Graph API + token refresh + image upload)
  - Affiliate Worker (AccessTrade + commission tracking)
  - Scheduler Worker (automatic task enqueue from `scheduled_tasks`)

- **Async Task Queue** (high performance, SKIP LOCKED on Postgres)
- **Encrypted credential storage** (Facebook tokens, cookies)
- **Role-based access** (Admin / Member / User)
- **Commission splitting** (Admin passive income + Member active income)
- **Scheduling system** (create, list, pause, resume, delete schedules via API)

## Quick Start

### 1. Setup Environment

```powershell
cd E:\DYT_01

# Create virtualenv (recommended)
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright (for legacy fallback if needed)
playwright install chromium
```

### 2. Configure .env

Copy the example and fill real values:

```powershell
copy .env.example .env
```

**Important keys:**
- `FERNET_KEY` (generate with: `python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"`)
- `JWT_SECRET_KEY` (min 32 chars)
- `ACCESS_TRADE_ACCESS_KEY`
- `FACEBOOK_APP_ID` / `FACEBOOK_APP_SECRET` (optional, per-account also supported)
- `DATABASE_URL` (default: sqlite)

### 3. Initialize Database

```powershell
python start.py init-db
```

This creates tables + seeds a default admin user.

### 4. Run the System (Recommended)

Open 3 terminals:

**Terminal 1 - API**
```powershell
python start.py api
```

**Terminal 2 - Workers**
```powershell
python start.py worker --type facebook
python start.py worker --type affiliate
```

**Terminal 3 - Scheduler**
```powershell
python start.py scheduler
```

Or run everything together:
```powershell
python start.py all
```

## API

- Swagger UI: http://localhost:8000/docs (after starting API)
- See `API.md` for full endpoint list.

## Project Structure (Cleaned)

```
src/
├── workers/               # FacebookWorker, AffiliateWorker, SchedulerWorker
├── task_queue_db_async.py # High-performance async queue
├── db/
│   ├── models.py
│   └── crud.py
├── utils/encryption.py
└── accesstrade_client.py

web/
├── main.py
├── routers/               # auth, facebook, affiliate, scheduler, ...
└── dependencies.py

start.py                   # Unified launcher (api / worker / scheduler / all)
scripts/migrate_*.py       # Migration helpers (optional)
```

## Next Steps after Setup

1. Add Facebook accounts via `POST /facebook/accounts` (admin only)
2. Create schedules via `POST /schedules`
3. Watch the Scheduler enqueue tasks automatically
4. Workers pick them up and execute

## Migration from Old Scripts

See [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) for step-by-step instructions on moving from the old standalone scripts (pre-Phase 1) to the new worker + scheduler architecture.

## Running with Docker (Recommended for Production)

```bash
docker-compose up -d --build
```

See `docker-compose.yml` and [DEPLOYMENT.md](DEPLOYMENT.md) for details.

## License

Internal project.

---

**Status**: Phase 4 completed. System ready for production use.
