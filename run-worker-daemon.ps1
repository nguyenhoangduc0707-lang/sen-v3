# run-worker-daemon.ps1
Write-Host "Starting Worker Daemon..." -ForegroundColor Cyan
while ($true) {
    python run_worker.py --run-once
    Write-Host "Worker cycle completed. Waiting 5 seconds..." -ForegroundColor Gray
    Start-Sleep -Seconds 5
}
