@echo off
echo Starting SEN V3 with FastAPI backend + React frontend...
cd /d C:\DYT_01
call venv\Scripts\activate.bat
start "Backend" cmd /k "uvicorn web.main:app --reload --port 8000"
start "Frontend" cmd /k "cd frontend && npm run dev"
start "Worker" cmd /k "python run_worker.py"
echo Backend: http://localhost:8000/docs
echo Frontend: http://localhost:5173
pause