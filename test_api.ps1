Write-Host "=== TEST API DYT_01 ===" -ForegroundColor Cyan

# 1. Health check
Write-Host "`n1. Health Check:" -ForegroundColor Yellow
try {
    $health = Invoke-WebRequest -Uri "http://localhost:8000/api/v1/health" -UseBasicParsing -ErrorAction Stop
    Write-Host $health.Content -ForegroundColor Green
} catch {
    Write-Host "Lỗi: $($_.Exception.Message)" -ForegroundColor Red
}

# 2. Lấy danh sách tasks
Write-Host "`n2. Danh sách tasks:" -ForegroundColor Yellow
try {
    $tasks = Invoke-WebRequest -Uri "http://localhost:8000/api/v1/tasks" -UseBasicParsing -ErrorAction Stop
    Write-Host $tasks.Content -ForegroundColor Green
} catch {
    Write-Host "Lỗi: $($_.Exception.Message)" -ForegroundColor Red
}

# 3. Tạo task mới
Write-Host "`n3. Tạo task mới:" -ForegroundColor Yellow
try {
    $newTask = Invoke-WebRequest -Uri "http://localhost:8000/api/v1/tasks?title=PowerShell%20Task&task_type=test" -Method POST -UseBasicParsing -ErrorAction Stop
    Write-Host $newTask.Content -ForegroundColor Green
} catch {
    Write-Host "Lỗi: $($_.Exception.Message)" -ForegroundColor Red
}

# 4. Xem lại danh sách tasks sau khi tạo
Write-Host "`n4. Danh sách tasks sau khi tạo:" -ForegroundColor Yellow
try {
    $tasksAfter = Invoke-WebRequest -Uri "http://localhost:8000/api/v1/tasks" -UseBasicParsing -ErrorAction Stop
    Write-Host $tasksAfter.Content -ForegroundColor Green
} catch {
    Write-Host "Lỗi: $($_.Exception.Message)" -ForegroundColor Red
}

# 5. Đăng nhập
Write-Host "`n5. Đăng nhập:" -ForegroundColor Yellow
try {
    $body = @{username="admin"; password="admin"} | ConvertTo-Json
    $login = Invoke-WebRequest -Uri "http://localhost:8000/api/v1/auth/login" -Method POST -Body $body -ContentType "application/json" -UseBasicParsing -ErrorAction Stop
    Write-Host $login.Content -ForegroundColor Green
} catch {
    Write-Host "Lỗi: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n✅ Test hoàn tất!" -ForegroundColor Green
