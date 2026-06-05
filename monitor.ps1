while ($true) {
    Clear-Host
    Write-Host "=== MONITOR DYT_01 API ===" -ForegroundColor Cyan
    Write-Host "Thời gian: $(Get-Date)" -ForegroundColor Yellow
    
    $health = Invoke-WebRequest -Uri "http://localhost:8000/api/v1/health" -UseBasicParsing -ErrorAction SilentlyContinue
    Write-Host "Health: $($health.Content)" -ForegroundColor Green
    
    $tasks = Invoke-WebRequest -Uri "http://localhost:8000/api/v1/tasks" -UseBasicParsing -ErrorAction SilentlyContinue
    $tasksData = $tasks.Content | ConvertFrom-Json
    Write-Host "Số lượng tasks: $($tasksData.Count)" -ForegroundColor Cyan
    
    Start-Sleep -Seconds 10
}
