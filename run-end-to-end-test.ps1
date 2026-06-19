# run-end-to-end-test.ps1
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "END-TO-END SYSTEM TEST" -ForegroundColor Cyan
Write-Host "========================================"

$ErrorActionPreference = "Continue"
$TestResults = @()
$AllPassed = $true

# 1. Check .env
Write-Host ""
Write-Host "[1] CHECKING .ENV..." -ForegroundColor Yellow
if (Test-Path ".env") {
    $envContent = Get-Content ".env" -Raw
    $required = @("DATABASE_URL", "JWT_SECRET_KEY", "FERNET_KEY", "GEMINI_API_KEY")
    $missing = @()
    foreach ($var in $required) {
        if ($envContent -notmatch "$var\s*=") {
            $missing += $var
        }
    }
    if ($missing.Count -gt 0) {
        Write-Host "ERROR: Missing variables: $($missing -join ', ')" -ForegroundColor Red
        $AllPassed = $false
    } else {
        Write-Host "OK: .env is complete" -ForegroundColor Green
        $TestResults += "ENV_OK"
    }
} else {
    Write-Host "ERROR: .env not found" -ForegroundColor Red
    $AllPassed = $false
}

# 2. Check database
Write-Host ""
Write-Host "[2] CHECKING DATABASE..." -ForegroundColor Yellow
if (Test-Path "app.db") {
    $size = (Get-Item "app.db").Length / 1KB
    Write-Host "OK: app.db exists (size: $([math]::Round($size, 2)) KB)" -ForegroundColor Green
    $TestResults += "DB_OK"
} else {
    Write-Host "WARN: app.db not found" -ForegroundColor Yellow
}

# 3. Create test task
Write-Host ""
Write-Host "[3] CREATING TEST TASK..." -ForegroundColor Yellow
$taskId = $null
try {
    $output = python -c @"
from src.db.session import SessionLocal
from src.db.models import Task
import json
from datetime import datetime

db = SessionLocal()
task = Task(
    title='E2E Test Task',
    task_type='echo_worker',
    category='test',
    payload=json.dumps({'message': 'E2E test at ' + datetime.now().isoformat()}),
    status='PENDING',
    priority=1,
    worker_name='echo_worker'
)
db.add(task)
db.commit()
print(task.id)
db.close()
"@ 2>&1
    $taskId = $output.Trim()
    if ($taskId -match '^\d+$') {
        Write-Host "OK: Created task ID: $taskId" -ForegroundColor Green
        $TestResults += "TASK_CREATED"
    } else {
        Write-Host "ERROR: Failed to create task: $output" -ForegroundColor Red
        $AllPassed = $false
    }
} catch {
    Write-Host "ERROR: $_" -ForegroundColor Red
    $AllPassed = $false
}

# 4. Run worker one-shot
if ($taskId) {
    Write-Host ""
    Write-Host "[4] RUNNING WORKER ONE-SHOT..." -ForegroundColor Yellow
    try {
        $workerOutput = python run_worker.py --run-once 2>&1
        Write-Host "OK: Worker executed" -ForegroundColor Green
        $TestResults += "WORKER_RAN"
    } catch {
        Write-Host "ERROR: Worker failed: $_" -ForegroundColor Red
        $AllPassed = $false
    }
}

# 5. Check task result
if ($taskId) {
    Write-Host ""
    Write-Host "[5] CHECKING TASK RESULT..." -ForegroundColor Yellow
    try {
        $result = python -c @"
from src.db.session import SessionLocal
from src.db.models import Task
db = SessionLocal()
task = db.query(Task).filter(Task.id == $taskId).first()
if task:
    print(f'Status: {task.status}')
    if task.last_error:
        print(f'Error: {task.last_error}')
db.close()
"@ 2>&1
        Write-Host $result -ForegroundColor Gray
        if ($result -match "Status: COMPLETED") {
            Write-Host "OK: Task completed successfully" -ForegroundColor Green
            $TestResults += "TASK_COMPLETED"
        } else {
            Write-Host "WARN: Task not completed or has error" -ForegroundColor Yellow
            $AllPassed = $false
        }
    } catch {
        Write-Host "ERROR: Check failed: $_" -ForegroundColor Red
        $AllPassed = $false
    }
}

# 6. Check API health
Write-Host ""
Write-Host "[6] CHECKING API HEALTH..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8001/health" -Method GET -TimeoutSec 5 -ErrorAction SilentlyContinue
    if ($response.StatusCode -eq 200) {
        Write-Host "OK: API health check passed" -ForegroundColor Green
        $TestResults += "API_HEALTHY"
    } else {
        Write-Host "WARN: API returned status: $($response.StatusCode)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "WARN: API not running (run: python run_api.py)" -ForegroundColor Yellow
}

# Summary
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "TEST SUMMARY" -ForegroundColor Cyan
Write-Host "========================================"
$TestResults | ForEach-Object { Write-Host "  OK: $_" -ForegroundColor Green }

if ($AllPassed) {
    Write-Host ""
    Write-Host "ALL TESTS PASSED!" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "SOME TESTS FAILED" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "DONE" -ForegroundColor Cyan
Write-Host "========================================"