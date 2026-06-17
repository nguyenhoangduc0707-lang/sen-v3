# start-all.ps1
Write-Host "Starting SEN V3 Full System..." -ForegroundColor Cyan
Write-Host "Starting API Server..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit -Command cd '$PSScriptRoot'; .\start-api.ps1"
Start-Sleep -Seconds 2
Write-Host "Starting Worker..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit -Command cd '$PSScriptRoot'; .\start-worker.ps1"
Write-Host "System started! API: http://localhost:8001/docs" -ForegroundColor Green
