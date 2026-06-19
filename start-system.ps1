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
