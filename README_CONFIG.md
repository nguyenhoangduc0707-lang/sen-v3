SEN V3 - Configuration Guide

Canonical stack:
- API: FastAPI in web/main.py
- Worker engine: run_worker.py with SQLAlchemy DB queue
- Database: SQLAlchemy models in src/db/models.py and Alembic migrations
- Frontend: React app in frontend/src/App.jsx

1. Create .env from .env.example
   cp .env.example .env
   Edit JWT_SECRET_KEY, ENCRYPTION_KEY, DATABASE_URL, and optional API keys.

2. Install Python dependencies
   python -m pip install -r requirements.txt

3. Initialize DB
   python scripts/init_db.py --admin-user admin --admin-password admin123

4. Check configuration
   python scripts/check_config.py

5. List workers
   python main.py --list-workers

6. Run API server
   python run_api.py
   Open: http://localhost:8000/api/v1/docs

7. Run worker engine
   python run_worker.py --max-workers 5

8. Run frontend
   npm start

NotebookLM CLI setup:
- Install and sync project context:
  .\setup_notebooklm_cli.ps1
- Refresh local NotebookLM source files only:
  python update_notebooklm.py
- Upload current context to the configured NotebookLM notebook:
  python notebooklm_client.py
- Default notebook:
  https://notebooklm.google.com/notebook/5e64f86d-3f1b-44bd-a5c0-067fd839e3a5

Frontend env:
- REACT_APP_API_BASE_URL=http://localhost:8000/api/v1
- REACT_APP_GEMINI_API_KEY=gemini_real_xxxxx

Do not commit real secrets. Use environment variables or a secrets manager outside development.

