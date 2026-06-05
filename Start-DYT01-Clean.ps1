# Start-DYT01-Clean.ps1
Write-Host "🚀 KHỞI ĐỘNG DYT_01 SAU DỌN DẸP" -ForegroundColor Cyan

# Kích hoạt venv
.\venv\Scripts\Activate.ps1

# Chạy API server
Write-Host "Starting API server..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'E:\DYT_01'; .\venv\Scripts\Activate.ps1; python run_api.py"

Start-Sleep -Seconds 3

# Chạy worker
Write-Host "Starting worker..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'E:\DYT_01'; .\venv\Scripts\Activate.ps1; python run_worker.py"

Write-Host "✅ Hệ thống đã khởi động!" -ForegroundColor Green
Write-Host "📊 API: http://localhost:8000/api/v1/docs" -ForegroundColor Cyan
