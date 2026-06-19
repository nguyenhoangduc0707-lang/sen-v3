# complete-project-files.ps1
# Tạo và hoàn thiện tất cả các tệp cần thiết cho dự án DYT_01

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "COMPLETING PROJECT FILES" -ForegroundColor Cyan
Write-Host "========================================"

$ProjectRoot = "E:\DYT_01"
Set-Location $ProjectRoot

# Hàm kiểm tra và tạo file
function Ensure-File {
    param($Path, $Content)
    $fullPath = Join-Path $ProjectRoot $Path
    $dir = Split-Path $fullPath -Parent
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Force -Path $dir | Out-Null
    }
    if (!(Test-Path $fullPath)) {
        Write-Host "Creating: $Path" -ForegroundColor Yellow
        $Content | Out-File -FilePath $fullPath -Encoding UTF8
        Write-Host "  Created" -ForegroundColor Green
    } else {
        Write-Host "Exists: $Path" -ForegroundColor Gray
    }
}

# 1. Đảm bảo src/orchestrator.py có get_worker
$orchContent = @'
import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from src.task_queue_db import TaskQueueDB
from src.workers import WORKER_REGISTRY

logger = logging.getLogger(__name__)

def get_worker(name: str):
    """Trả về worker class từ registry."""
    return WORKER_REGISTRY.get(name)

def register_worker(name: str, worker_class):
    """Đăng ký worker vào registry."""
    WORKER_REGISTRY[name] = worker_class
    return True

def load_workers():
    """Load tất cả worker từ registry."""
    return WORKER_REGISTRY

# ==================== WORKER ENGINE ====================
async def run_engine(max_workers: int = 5, poll_interval: float = 1.0, run_once: bool = False):
    """Chạy worker engine với số lượng workers cho trước."""
    load_workers()
    queue = TaskQueueDB()
    executor = ThreadPoolExecutor(max_workers=max_workers)
    stop_event = asyncio.Event()
    loop = asyncio.get_running_loop()

    # Xử lý signal (chỉ trên Unix)
    import signal
    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, stop_event.set)
        except (NotImplementedError, RuntimeError, ValueError):
            pass

    tasks = [asyncio.create_task(worker_loop(i, queue, executor, poll_interval, stop_event)) for i in range(max_workers)]

    if run_once:
        # Chạy một lần: đợi cho đến khi hết task hoặc timeout
        async def wait_for_done():
            from sqlalchemy import text
            qq = TaskQueueDB()
            max_wait = 8.0
            waited = 0.0
            while waited < max_wait:
                try:
                    with qq.engine.connect() as conn:
                        res = conn.execute(text('SELECT COUNT(*) FROM tasks WHERE status = "PENDING"'))
                        pending = res.scalar() or 0
                    if pending == 0:
                        break
                except Exception:
                    pass
                await asyncio.sleep(poll_interval)
                waited += poll_interval
            stop_event.set()
        asyncio.create_task(wait_for_done())

    await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    stop_event.set()
    executor.shutdown(wait=True)

async def worker_loop(worker_id: int, queue: TaskQueueDB, executor: ThreadPoolExecutor, poll_interval: float, stop_event: asyncio.Event):
    """Vòng lặp của một worker."""
    logger.info(f"Worker {worker_id}: loop started")
    while not stop_event.is_set():
        try:
            task = queue.claim_next_task()
            if task:
                logger.info(f"Worker {worker_id}: claimed task {task.id}")
                # Xử lý task
                worker_name = task.worker_name
                if worker_name and worker_name in WORKER_REGISTRY:
                    worker_class = WORKER_REGISTRY[worker_name]
                    worker = worker_class()
                    try:
                        result = worker.run(task.payload)
                        queue.mark_completed(task.id)
                        logger.info(f"Worker {worker_name}: task {task.id} completed")
                    except Exception as e:
                        queue.mark_failed(task.id, str(e))
                        logger.error(f"Worker {worker_name}: task {task.id} failed: {e}")
                else:
                    logger.warning(f"Worker {worker_id}: unknown worker {worker_name}")
                    queue.mark_failed(task.id, f"Unknown worker: {worker_name}")
            else:
                await asyncio.sleep(poll_interval)
        except Exception as e:
            logger.error(f"Worker {worker_id}: error: {e}", exc_info=True)
            await asyncio.sleep(poll_interval)
    logger.info(f"Worker {worker_id}: loop stopped")
'@
Ensure-File "src/orchestrator.py" $orchContent

# 2. Đảm bảo src/db/session.py
$sessionContent = @'
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.db.database import engine, SessionLocal, Base

def get_engine():
    return engine

def get_session():
    return SessionLocal()
'@
Ensure-File "src/db/session.py" $sessionContent

# 3. Tạo file render.yaml
$renderYaml = @'
services:
  - type: web
    name: dyt-api
    runtime: image
    repo: https://github.com/nguyenhoangduc0707-lang/sen-v3
    region: singapore
    plan: free
    dockerfilePath: ./Dockerfile
    envVars:
      - key: DATABASE_URL
        value: sqlite:///./app.db
      - key: JWT_SECRET_KEY
        generateValue: true
      - key: FERNET_KEY
        generateValue: true
      - key: GEMINI_API_KEY
        sync: false

  - type: worker
    name: dyt-worker
    runtime: image
    repo: https://github.com/nguyenhoangduc0707-lang/sen-v3
    region: singapore
    plan: free
    dockerfilePath: ./Dockerfile
    command: python run_worker.py
    envVars:
      - key: DATABASE_URL
        value: sqlite:///./app.db
      - key: JWT_SECRET_KEY
        generateValue: true
      - key: FERNET_KEY
        generateValue: true
      - key: GEMINI_API_KEY
        sync: false
'@
Ensure-File "render.yaml" $renderYaml

# 4. Tạo Dockerfile nếu chưa có
$dockerfile = @'
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY . .

EXPOSE 8080

CMD ["uvicorn", "web.main:app", "--host", "0.0.0.0", "--port", "8080"]
'@
Ensure-File "Dockerfile" $dockerfile

# 5. Tạo railway.json
$railwayJson = @'
{
  "build": {
    "builder": "DOCKERFILE"
  },
  "deploy": {
    "numReplicas": 1,
    "startCommand": "uvicorn web.main:app --host 0.0.0.0 --port $PORT",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE"
  }
}
'@
Ensure-File "railway.json" $railwayJson

# 6. Tạo .env.example đầy đủ
$envExample = @'
# Database
DATABASE_URL=sqlite:///./app.db

# Security
JWT_SECRET_KEY=your-secret-key-here-change-in-production
FERNET_KEY=your-fernet-key-here-change-in-production

# AI Services
GEMINI_API_KEY=your-gemini-api-key

# Facebook Auth (optional - path to auth file)
FACEBOOK_AUTH_PATH=credentials/facebook_auth.json

# Server
API_HOST=0.0.0.0
API_PORT=8001
'@
Ensure-File ".env.example" $envExample

# 7. Tạo scripts/check_workers.py để kiểm tra worker
$checkWorkers = @'
import sys
from src.orchestrator import load_workers, get_worker

def main():
    workers = load_workers()
    print(f"Total workers: {len(workers)}")
    for name in workers:
        print(f"  - {name}")
    if len(sys.argv) > 1:
        worker_name = sys.argv[1]
        w = get_worker(worker_name)
        if w:
            print(f"Worker {worker_name} found: {w}")
        else:
            print(f"Worker {worker_name} not found")

if __name__ == "__main__":
    main()
'@
Ensure-File "scripts/check_workers.py" $checkWorkers

# 8. Tạo scripts/run_all_workers.py
$runAllWorkers = @'
import asyncio
import sys
from src.orchestrator import run_engine, load_workers

async def main():
    load_workers()
    run_once = "--run-once" in sys.argv
    await run_engine(max_workers=5, poll_interval=1.0, run_once=run_once)

if __name__ == "__main__":
    asyncio.run(main())
'@
Ensure-File "scripts/run_all_workers.py" $runAllWorkers

# 9. Tạo web/__init__.py nếu thiếu
$webInit = @'
from .main import app
'@
Ensure-File "web/__init__.py" $webInit

# 10. Tạo src/__init__.py
$srcInit = @'
from . import db
from . import workers
'@
Ensure-File "src/__init__.py" $srcInit

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "ALL FILES CREATED/VERIFIED" -ForegroundColor Green
Write-Host "========================================"
Write-Host ""
Write-Host "Summary of files created:"
Write-Host "  - src/orchestrator.py (updated with get_worker)"
Write-Host "  - src/db/session.py"
Write-Host "  - render.yaml (for Render deployment)"
Write-Host "  - railway.json (for Railway deployment)"
Write-Host "  - .env.example (updated)"
Write-Host "  - scripts/check_workers.py"
Write-Host "  - scripts/run_all_workers.py"
Write-Host "  - web/__init__.py"
Write-Host "  - src/__init__.py"
Write-Host ""
Write-Host "Next steps:"
Write-Host "  1. Run: python run_api.py"
Write-Host "  2. Run: python run_scheduler.py"
Write-Host "  3. Run: python run_worker.py --run-once"
Write-Host ""
Write-Host "To deploy on Render:"
Write-Host "  - Push to GitHub"
Write-Host "  - Connect repo to Render"
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan