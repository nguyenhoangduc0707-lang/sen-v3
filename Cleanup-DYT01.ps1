# ============================================
# Script: Cleanup-DYT01.ps1
# Mô tả: Kiểm tra và dọn dẹp rác trong dự án DYT_01
# ============================================

param(
    [switch]$DryRun = $false,  # Chạy thử (chỉ hiển thị, không xóa)
    [switch]$CleanPython = $true,
    [switch]$CleanNode = $true,
    [switch]$CleanDatabase = $false  # Thận trọng với database
)

Write-Host "=== DỌN DẸP DỰ ÁN DYT_01 ===" -ForegroundColor Cyan
Write-Host "Thời gian: $(Get-Date)" -ForegroundColor Gray
Write-Host ""

# 1. KIỂM TRA CẤU TRÚC DỰ ÁN
Write-Host "[1/6] KIỂM TRA CẤU TRÚC DỰ ÁN..." -ForegroundColor Yellow
Write-Host "✓ Thư mục hiện tại: $(Get-Location)" -ForegroundColor Green

# Kiểm tra file quan trọng
$importantFiles = @(".env", "requirements.txt", "main.py", "manage.py")
foreach ($file in $importantFiles) {
    if (Test-Path $file) {
        Write-Host "  ✓ $file tồn tại" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $file KHÔNG tồn tại" -ForegroundColor Red
    }
}

# 2. THỐNG KÊ DUNG LƯỢNG HIỆN TẠI
Write-Host ""
Write-Host "[2/6] THỐNG KÊ DUNG LƯỢNG HIỆN TẠI..." -ForegroundColor Yellow

function Get-FolderSize {
    param([string]$Path)
    if (Test-Path $Path) {
        $size = (Get-ChildItem -Path $Path -Recurse -ErrorAction SilentlyContinue | 
                 Measure-Object -Property Length -Sum).Sum
        return [math]::Round($size / 1MB, 2)
    }
    return 0
}

$foldersToCheck = @{
    "__pycache__" = "Python cache files"
    ".pytest_cache" = "Pytest cache"
    "htmlcov" = "Coverage reports"
    "node_modules" = "Node modules"
    "venv" = "Virtual environment"
    "logs" = "Log files"
    ".github" = "GitHub workflows"
}

$totalBefore = 0
foreach ($folder in $foldersToCheck.Keys) {
    $size = Get-FolderSize $folder
    $totalBefore += $size
    Write-Host "  $folder : $size MB" -ForegroundColor Gray
}

# 3. DỌN DẸP PYTHON CACHE
Write-Host ""
Write-Host "[3/6] DỌN DẸP PYTHON CACHE..." -ForegroundColor Yellow

if ($CleanPython) {
    # Xóa __pycache__ folders
    $pyCacheDirs = Get-ChildItem -Path . -Directory -Recurse -Filter "__pycache__" -ErrorAction SilentlyContinue
    Write-Host "  Tìm thấy $($pyCacheDirs.Count) thư mục __pycache__" -ForegroundColor Gray
    
    if ($DryRun) {
        Write-Host "  [DRY RUN] Sẽ xóa các thư mục:" -ForegroundColor Cyan
        $pyCacheDirs | ForEach-Object { Write-Host "    - $($_.FullName)" -ForegroundColor Gray }
    } else {
        $pyCacheDirs | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
        Write-Host "  ✓ Đã xóa __pycache__ folders" -ForegroundColor Green
    }
    
    # Xóa .pyc files
    $pycFiles = Get-ChildItem -Path . -File -Recurse -Filter "*.pyc" -ErrorAction SilentlyContinue
    Write-Host "  Tìm thấy $($pycFiles.Count) file .pyc" -ForegroundColor Gray
    
    if (!$DryRun) {
        $pycFiles | Remove-Item -Force -ErrorAction SilentlyContinue
        Write-Host "  ✓ Đã xóa .pyc files" -ForegroundColor Green
    }
    
    # Xóa .pytest_cache
    if (Test-Path ".pytest_cache") {
        if ($DryRun) {
            Write-Host "  [DRY RUN] Sẽ xóa .pytest_cache" -ForegroundColor Cyan
        } else {
            Remove-Item -Path ".pytest_cache" -Recurse -Force
            Write-Host "  ✓ Đã xóa .pytest_cache" -ForegroundColor Green
        }
    }
    
    # Xóa htmlcov
    if (Test-Path "htmlcov") {
        if ($DryRun) {
            Write-Host "  [DRY RUN] Sẽ xóa htmlcov" -ForegroundColor Cyan
        } else {
            Remove-Item -Path "htmlcov" -Recurse -Force
            Write-Host "  ✓ Đã xóa htmlcov" -ForegroundColor Green
        }
    }
    
    # Xóa .coverage
    if (Test-Path ".coverage") {
        if ($DryRun) {
            Write-Host "  [DRY RUN] Sẽ xóa .coverage" -ForegroundColor Cyan
        } else {
            Remove-Item -Path ".coverage" -Force
            Write-Host "  ✓ Đã xóa .coverage" -ForegroundColor Green
        }
    }
}

# 4. DỌN DẸP NODE_MODULES
Write-Host ""
Write-Host "[4/6] DỌN DẸP NODE_MODULES..." -ForegroundColor Yellow

if ($CleanNode) {
    if (Test-Path "node_modules") {
        $nodeSize = Get-FolderSize "node_modules"
        Write-Host "  node_modules hiện tại: $nodeSize MB" -ForegroundColor Gray
        
        if ($DryRun) {
            Write-Host "  [DRY RUN] Sẽ xóa node_modules" -ForegroundColor Cyan
        } else {
            Remove-Item -Path "node_modules" -Recurse -Force -ErrorAction SilentlyContinue
            Write-Host "  ✓ Đã xóa node_modules (tiết kiệm $nodeSize MB)" -ForegroundColor Green
        }
    } else {
        Write-Host "  Không tìm thấy node_modules" -ForegroundColor Gray
    }
    
    # Xóa package-lock.json (optional, nhưng có thể tạo lại)
    if (Test-Path "package-lock.json") {
        if (!$DryRun) {
            Remove-Item -Path "package-lock.json" -Force
            Write-Host "  ✓ Đã xóa package-lock.json" -ForegroundColor Green
        }
    }
}

# 5. DỌN DẸP LOGS
Write-Host ""
Write-Host "[5/6] DỌN DẸP LOGS..." -ForegroundColor Yellow

if (Test-Path "logs") {
    $logFiles = Get-ChildItem -Path "logs" -File -Filter "*.log" -ErrorAction SilentlyContinue
    Write-Host "  Tìm thấy $($logFiles.Count) file log" -ForegroundColor Gray
    
    if ($DryRun) {
        Write-Host "  [DRY RUN] Sẽ xóa các file log cũ hơn 30 ngày" -ForegroundColor Cyan
    } else {
        $oldLogs = Get-ChildItem -Path "logs" -File -Filter "*.log" | Where-Object { 
            $_.LastWriteTime -lt (Get-Date).AddDays(-30) 
        }
        $oldLogs | Remove-Item -Force
        Write-Host "  ✓ Đã xóa $($oldLogs.Count) file log cũ" -ForegroundColor Green
        
        # Xóa logs rỗng
        Get-ChildItem -Path "logs" -Directory | Where-Object { 
            (Get-ChildItem $_.FullName -File).Count -eq 0 
        } | Remove-Item -Force
    }
}

# 6. DỌN DẸP TEMP FILES
Write-Host ""
Write-Host "[6/6] DỌN DẸP FILE TẠM..." -ForegroundColor Yellow

$tempPatterns = @("*.tmp", "*.bak", "*.log", "*.py~", "*.swp")
foreach ($pattern in $tempPatterns) {
    $tempFiles = Get-ChildItem -Path . -File -Filter $pattern -Recurse -ErrorAction SilentlyContinue
    if ($tempFiles.Count -gt 0) {
        Write-Host "  Tìm thấy $($tempFiles.Count) file $pattern" -ForegroundColor Gray
        if (!$DryRun) {
            $tempFiles | Remove-Item -Force -ErrorAction SilentlyContinue
        }
    }
}

# Xóa thư mục __pycache__ trong src và web
$srcDirs = @("src", "web", "tests", "affiliate", "tasks")
foreach ($dir in $srcDirs) {
    if (Test-Path $dir) {
        $cacheDirs = Get-ChildItem -Path $dir -Directory -Recurse -Filter "__pycache__" -ErrorAction SilentlyContinue
        if ($cacheDirs.Count -gt 0 -and !$DryRun) {
            $cacheDirs | Remove-Item -Recurse -Force
            Write-Host "  ✓ Đã dọn cache trong $dir" -ForegroundColor Green
        }
    }
}

# BÁO CÁO KẾT QUẢ
Write-Host ""
Write-Host "=== KẾT QUẢ DỌN DẸP ===" -ForegroundColor Cyan

$totalAfter = 0
foreach ($folder in $foldersToCheck.Keys) {
    $size = Get-FolderSize $folder
    $totalAfter += $size
}

$saved = $totalBefore - $totalAfter

Write-Host "Dung lượng trước khi dọn: $totalBefore MB" -ForegroundColor Yellow
Write-Host "Dung lượng sau khi dọn: $totalAfter MB" -ForegroundColor Yellow
Write-Host "Đã tiết kiệm: $saved MB" -ForegroundColor Green

if ($DryRun) {
    Write-Host ""
    Write-Host "⚠️  ĐÂY LÀ CHẠY THỬ (DRY RUN)" -ForegroundColor Yellow
    Write-Host "Để thực thi thực tế, chạy lệnh: .\Cleanup-DYT01.ps1 -DryRun `$false" -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "✓ Dọn dẹp hoàn tất!" -ForegroundColor Green
    
    # Hiển thị cảnh báo nếu database bị ảnh hưởng
    if ($CleanDatabase) {
        Write-Host "⚠️  Đã bật flag CleanDatabase - Hãy kiểm tra database của bạn!" -ForegroundColor Red
    }
}

# TẠO BÁO CÁO
$report = @"
=== DỌN DẸP DYT_01 ===
Thời gian: $(Get-Date)
Dry Run: $DryRun
Dung lượng tiết kiệm: $saved MB

Các thư mục đã dọn:
- __pycache__: Đã xóa
- .pytest_cache: Đã xóa
- htmlcov: Đã xóa
- logs: Đã dọn log cũ
- node_modules: Đã xóa
"@

$report | Out-File -FilePath "cleanup_report_$(Get-Date -Format 'yyyyMMdd_HHmmss').txt"
Write-Host "✓ Báo cáo đã được lưu" -ForegroundColor Gray