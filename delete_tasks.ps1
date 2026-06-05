Write-Host "=== XÓA TASK THEO ID ===" -ForegroundColor Cyan
Write-Host "Danh sách tasks hiện tại:" -ForegroundColor Yellow

$tasks = Invoke-WebRequest -Uri "http://localhost:8000/api/v1/tasks" -UseBasicParsing
$tasksData = $tasks.Content | ConvertFrom-Json
$tasksData.value | Format-Table id, title, status -AutoSize

$idsToDelete = Read-Host "`nNhập các ID cần xóa (cách nhau bằng dấu phẩy, ví dụ: 1,3,5)"

if ($idsToDelete) {
    $ids = $idsToDelete -split "," | ForEach-Object { $_.Trim() }
    Write-Host "`nSẽ xóa các ID: $($ids -join ', ')" -ForegroundColor Red
    $confirm = Read-Host "Xác nhận xóa? (yes/no)"
    
    if ($confirm -eq "yes") {
        # Note: Cần có DELETE endpoint, hiện tại dùng cách reset database
        Write-Host "`n⚠️  Hiện tại API chưa có DELETE endpoint" -ForegroundColor Yellow
        Write-Host "Đề xuất: Dừng server, xóa database, chạy lại" -ForegroundColor Cyan
        
        $reset = Read-Host "Muốn reset toàn bộ database? (yes/no)"
        if ($reset -eq "yes") {
            # Dừng server (yêu cầu thủ công)
            Write-Host "`n1. Nhấn Ctrl+C để dừng server" -ForegroundColor Yellow
            Write-Host "2. Chạy lệnh: Remove-Item E:\DYT_01\app.db -Force" -ForegroundColor Yellow
            Write-Host "3. Chạy lại: python main_clean.py" -ForegroundColor Yellow
            Write-Host "4. Tạo lại các task cần giữ" -ForegroundColor Yellow
        }
    }
}
