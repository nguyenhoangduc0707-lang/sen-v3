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
