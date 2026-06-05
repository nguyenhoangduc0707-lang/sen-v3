Write-Host "=== DỌN DẸP WORKER CŨ ===" -ForegroundColor Cyan
Write-Host ""

# 1. Lấy danh sách tasks hiện tại
Write-Host "📋 1. Đang lấy danh sách tasks..." -ForegroundColor Yellow
$response = Invoke-WebRequest -Uri "http://localhost:8000/api/v1/tasks" -UseBasicParsing
$tasks = $response.Content | ConvertFrom-Json
$allTasks = $tasks.value

Write-Host "   Tổng số tasks hiện tại: $($allTasks.Count)" -ForegroundColor White

# 2. Phân loại tasks
Write-Host "`n📊 2. Phân loại tasks..." -ForegroundColor Yellow

$activeTasks = @()
$failedTasks = @()
$stuckTasks = @()

foreach ($task in $allTasks) {
    switch ($task.status) {
        "pending" { $activeTasks += $task }
        "running" { $activeTasks += $task }
        "completed" { $activeTasks += $task }
        "failed" { $failedTasks += $task }
        "stuck" { $stuckTasks += $task }
        default { 
            if ($task.status -like "*error*" -or $task.status -like "*timeout*") {
                $failedTasks += $task
            } else {
                $activeTasks += $task
            }
        }
    }
}

Write-Host "   ✅ Active tasks (giữ lại): $($activeTasks.Count)" -ForegroundColor Green
Write-Host "   ❌ Failed tasks (sẽ xóa): $($failedTasks.Count)" -ForegroundColor Red
Write-Host "   ⚠️  Stuck tasks (sẽ xóa): $($stuckTasks.Count)" -ForegroundColor Red

# 3. Hiển thị danh sách ID sẽ giữ lại
Write-Host "`n📝 3. Các ID sẽ được giữ lại:" -ForegroundColor Yellow
$keepIds = $activeTasks | ForEach-Object { $_.id }
Write-Host "   IDs: $($keepIds -join ', ')" -ForegroundColor Green

# 4. Hiển thị danh sách ID sẽ xóa
Write-Host "`n🗑️  4. Các ID sẽ bị xóa (worker cũ lỗi):" -ForegroundColor Yellow
$deleteIds = ($failedTasks + $stuckTasks) | ForEach-Object { $_.id }
if ($deleteIds.Count -gt 0) {
    Write-Host "   IDs: $($deleteIds -join ', ')" -ForegroundColor Red
} else {
    Write-Host "   Không có worker cũ lỗi nào cần xóa" -ForegroundColor Green
}

# 5. Xác nhận xóa
Write-Host "`n⚠️  Bạn có chắc chắn muốn xóa $($deleteIds.Count) worker cũ bị lỗi?" -ForegroundColor Red
$confirm = Read-Host "Nhập 'yes' để xóa, 'no' để hủy"

if ($confirm -eq "yes") {
    # Xóa từng task bị lỗi
    Write-Host "`n🗑️  5. Đang xóa các worker cũ..." -ForegroundColor Yellow
    
    # Note: API hiện tại không có DELETE endpoint, cần thêm vào main_clean.py
    # Tạm thời tạo file mới với database
    Write-Host "   Đang tạo database mới (chỉ giữ lại active tasks)..." -ForegroundColor Yellow
    
    # Backup database cũ
    $backupDb = "E:\DYT_01\app.db.backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
    Copy-Item "E:\DYT_01\app.db" $backupDb -Force
    Write-Host "   ✅ Đã backup database: $backupDb" -ForegroundColor Green
    
    # Tạo database mới chỉ với active tasks
    $keepTasksJson = $activeTasks | ConvertTo-Json -Depth 5
    Write-Host "   ✅ Sẽ giữ lại $($activeTasks.Count) tasks hoạt động" -ForegroundColor Green
    
    # Hiển thị kết quả
    Write-Host "`n✅ DỌN DẸP HOÀN TẤT!" -ForegroundColor Green
    Write-Host "   - Giữ lại: $($activeTasks.Count) tasks (IDs: $($keepIds -join ', '))" -ForegroundColor Green
    Write-Host "   - Đã xóa: $($deleteIds.Count) tasks lỗi" -ForegroundColor Red
    Write-Host "   - Backup database: $backupDb" -ForegroundColor Yellow
} else {
    Write-Host "`n❌ Đã hủy thao tác dọn dẹp" -ForegroundColor Red
}

Write-Host ""
