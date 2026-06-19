# complete-project-files.ps1
# Script tổng hợp tạo các file còn thiếu cho dự án DYT_01

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "COMPLETING PROJECT FILES" -ForegroundColor Cyan
Write-Host "========================================"

# 1. Tạo file .env nếu chưa có
Write-Host "`n[1] CHECKING .ENV..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    Write-Host "Creating .env from .env.example..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "OK: .env created. Please edit with your actual values." -ForegroundColor Green
} else {
    Write-Host "OK: .env exists" -ForegroundColor Green
}

# 2. Tạo thư mục credentials nếu chưa có
Write-Host "`n[2] CHECKING CREDENTIALS FOLDER..." -ForegroundColor Yellow
if (-not (Test-Path "credentials")) {
    New-Item -ItemType Directory -Path "credentials" | Out-Null
    Write-Host "OK: credentials folder created" -ForegroundColor Green
} else {
    Write-Host "OK: credentials folder exists" -ForegroundColor Green
}

# 3. Tạo file start-system.ps1
Write-Host "`n[3] CREATING start-system.ps1..." -ForegroundColor Yellow
$startSystem = @'
# start-system.ps1
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "STARTING DYT_01 SYSTEM" -ForegroundColor Cyan
Write-Host "========================================"

if (-not (Test-Path ".env")) {
    Write-Host "ERROR: .env not found" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Select startup mode:" -ForegroundColor Yellow
Write-Host "  1. All services (API + Scheduler + Worker)"
Write-Host "  2. API only"
Write-Host "  3. Worker only"
Write-Host "  4. Scheduler only"
Write-Host ""
$choice = Read-Host "Enter your choice (1-4)"

switch ($choice) {
    "1" {
        Write-Host "Starting all services..." -ForegroundColor Green
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; python run_api.py"
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; python run_scheduler.py"
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; python run_worker.py"
        Write-Host "All services started in separate windows!" -ForegroundColor Green
    }
    "2" { python run_api.py }
    "3" { python run_worker.py }
    "4" { python run_scheduler.py }
    default { Write-Host "Invalid choice" -ForegroundColor Red }
}
'@
$startSystem | Out-File -FilePath "start-system.ps1" -Encoding UTF8
Write-Host "OK: start-system.ps1 created" -ForegroundColor Green

# 4. Tạo file quick-test.ps1
Write-Host "`n[4] CREATING quick-test.ps1..." -ForegroundColor Yellow
$quickTest = @'
# quick-test.ps1
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "QUICK SYSTEM TEST" -ForegroundColor Cyan
Write-Host "========================================"

if (-not (Test-Path ".env")) {
    Write-Host "ERROR: .env missing" -ForegroundColor Red
    exit 1
}

if (Test-Path "app.db") {
    $size = (Get-Item "app.db").Length / 1KB
    Write-Host "OK: app.db exists ($([math]::Round($size, 2)) KB)" -ForegroundColor Green
} else {
    Write-Host "WARN: app.db not found" -ForegroundColor Yellow
}

Write-Host "Creating test task..." -ForegroundColor Yellow
$taskId = python -c "
from src.db.session import SessionLocal
from src.db.models import Task
import json
from datetime import datetime
db = SessionLocal()
task = Task(
    title='Quick Test',
    task_type='echo_worker',
    category='test',
    payload=json.dumps({'message': 'Quick test at ' + datetime.now().isoformat()}),
    status='PENDING',
    worker_name='echo_worker'
)
db.add(task)
db.commit()
print(task.id)
db.close()
" 2>$null
$taskId = $taskId.Trim()
if ($taskId -match '^\d+$') {
    Write-Host "OK: Created task ID: $taskId" -ForegroundColor Green
} else {
    Write-Host "ERROR: Failed to create task" -ForegroundColor Red
}

if ($taskId) {
    Write-Host "Running worker..." -ForegroundColor Yellow
    python run_worker.py --run-once 2>&1 | Out-Null
    Write-Host "Worker executed" -ForegroundColor Green

    $result = python -c "
from src.db.session import SessionLocal
from src.db.models import Task
db = SessionLocal()
task = db.query(Task).filter(Task.id == $taskId).first()
if task:
    print(f'Status: {task.status}')
db.close()
" 2>$null
    if ($result -match "COMPLETED") {
        Write-Host "OK: Task completed successfully!" -ForegroundColor Green
    } else {
        Write-Host "WARN: Task status: $result" -ForegroundColor Yellow
    }
}
Write-Host "TEST COMPLETE" -ForegroundColor Cyan
'@
$quickTest | Out-File -FilePath "quick-test.ps1" -Encoding UTF8
Write-Host "OK: quick-test.ps1 created" -ForegroundColor Green

# 5. Tạo file run-worker-daemon.ps1 (chạy worker liên tục)
Write-Host "`n[5] CREATING run-worker-daemon.ps1..." -ForegroundColor Yellow
$workerDaemon = @'
# run-worker-daemon.ps1
Write-Host "Starting Worker Daemon..." -ForegroundColor Cyan
while ($true) {
    python run_worker.py --run-once
    Write-Host "Worker cycle completed. Waiting 5 seconds..." -ForegroundColor Gray
    Start-Sleep -Seconds 5
}
'@
$workerDaemon | Out-File -FilePath "run-worker-daemon.ps1" -Encoding UTF8
Write-Host "OK: run-worker-daemon.ps1 created" -ForegroundColor Green

# 6. Tạo file fix-import-errors.ps1 (đã có thể dùng lại)
Write-Host "`n[6] CREATING fix-import-errors.ps1..." -ForegroundColor Yellow
$fixImport = @'
# fix-import-errors.ps1
Write-Host "Fixing import errors..." -ForegroundColor Yellow
$orchFile = "src/orchestrator.py"
if (Test-Path $orchFile) {
    $content = Get-Content $orchFile -Raw
    if ($content -notmatch "def get_worker\(") {
        $newFunc = @"

def get_worker(name: str):
    try:
        from src.workers import WORKER_REGISTRY
        return WORKER_REGISTRY.get(name)
    except:
        return None
"@
        $content + $newFunc | Set-Content -Path $orchFile -Encoding UTF8
        Write-Host "Added get_worker to orchestrator.py" -ForegroundColor Green
    } else {
        Write-Host "get_worker already exists" -ForegroundColor Green
    }
}
'@
$fixImport | Out-File -FilePath "fix-import-errors.ps1" -Encoding UTF8
Write-Host "OK: fix-import-errors.ps1 created" -ForegroundColor Green

# 7. Tạo file .gitignore nếu chưa có hoặc cập nhật
Write-Host "`n[7] UPDATING .gitignore..." -ForegroundColor Yellow
$gitignore = @'
__pycache__/
*.pyc
*.pyo
.pytest_cache/
.coverage
htmlcov/
.env
.env.local
venv/
.venv/
env/
ENV/
*.db
*.db-shm
*.db-wal
*.sqlite
*.sqlite3
credentials/
*.auth.json
*.pem
*.key
*.crt
*.p12
*.log
*.tmp
*.temp
logs/
tmp/
temp/
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store
Thumbs.db
frontend/node_modules/
node_modules/
.npm/
.yarn/
package-lock.json
yarn.lock
config/.env.production
save_facebook_auth.py
scripts/save_facebook_auth.py
gemini-cli/
'@
$gitignore | Out-File -FilePath ".gitignore" -Encoding UTF8
Write-Host "OK: .gitignore updated" -ForegroundColor Green

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "✅ PROJECT FILES COMPLETED" -ForegroundColor Green
Write-Host "========================================"