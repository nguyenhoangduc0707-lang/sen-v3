Write-Host "=== DỌN DẸP DỰ ÁN ===" -ForegroundColor Cyan
Write-Host ""

# 1. Xóa các file backup cũ
Write-Host "🗑️  Xóa các thư mục backup cũ..." -ForegroundColor Yellow
$backupDirs = Get-ChildItem -Path "E:\DYT_01" -Directory -Filter "backup_keys_*" -ErrorAction SilentlyContinue
foreach ($dir in $backupDirs) {
    Remove-Item -Path $dir.FullName -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "   Đã xóa: $($dir.Name)" -ForegroundColor Green
}

# 2. Xóa các file .pyc và __pycache__
Write-Host "`n🗑️  Xóa các file .pyc và __pycache__..." -ForegroundColor Yellow
Get-ChildItem -Path "E:\DYT_01" -Directory -Name "__pycache__" -Recurse -ErrorAction SilentlyContinue | ForEach-Object {
    Remove-Item -Path $_ -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "   Đã xóa: $_" -ForegroundColor Green
}

# 3. Xóa các file tạm thời
Write-Host "`n🗑️  Xóa các file tạm thời..." -ForegroundColor Yellow
$tempFiles = @("*.log", "*.tmp", "*.bak", "*.pyc")
foreach ($pattern in $tempFiles) {
    Get-ChildItem -Path "E:\DYT_01" -Filter $pattern -Recurse -ErrorAction SilentlyContinue | ForEach-Object {
        Remove-Item -Path $_.FullName -Force -ErrorAction SilentlyContinue
        Write-Host "   Đã xóa: $($_.Name)" -ForegroundColor Green
    }
}

# 4. Xóa các file test/debug không cần thiết
Write-Host "`n🗑️  Xóa các file test/debug..." -ForegroundColor Yellow
$debugFiles = @("debug_*.py", "test_*.py", "check_*.py", "fix_*.py", "temp_*.py", "create_*.py", "run_*.py")
foreach ($pattern in $debugFiles) {
    Get-ChildItem -Path "E:\DYT_01" -Filter $pattern -ErrorAction SilentlyContinue | ForEach-Object {
        Remove-Item -Path $_.FullName -Force -ErrorAction SilentlyContinue
        Write-Host "   Đã xóa: $($_.Name)" -ForegroundColor Green
    }
}

# 5. Xóa file .env cũ và tạo file .env mới sạch
Write-Host "`n🗑️  Xóa file .env cũ..." -ForegroundColor Yellow
if (Test-Path "E:\DYT_01\.env") {
    Remove-Item "E:\DYT_01\.env" -Force
    Write-Host "   Đã xóa .env cũ" -ForegroundColor Green
}

Write-Host "`n✅ HOÀN TẤT DỌN DẸP!" -ForegroundColor Green
