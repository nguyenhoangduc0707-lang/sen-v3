# ============================================
# MASTER CONTROLLER - DỰ ÁN VINWONDERS
# ============================================

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "🏖️ MASTER CONTROLLER - DỰ ÁN VINWONDERS" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan

Write-Host "`n📋 CHỌN MODULE CẦN CHẠY:" -ForegroundColor Yellow
Write-Host ""
Write-Host "   [1] CORE - Chạy lần đầu"
Write-Host "   [2] CONTENT - Sắp xếp nội dung"
Write-Host "   [3] CAMPAIGN - Tạo lịch đăng bài"
Write-Host "   [4] POST - Đăng bài lên Threads"
Write-Host "   [5] AFFILIATE - Tạo link affiliate"
Write-Host "   [6] MONITOR - Xem thống kê"
Write-Host "   [7] REPORT - Báo cáo doanh thu"
Write-Host "   [0] EXIT - Thoát"
Write-Host ""

$choice = Read-Host "Nhập lựa chọn (0-7)"

switch ($choice) {
    "1" { 
        Write-Host "`n🚀 CHẠY SETUP..." -ForegroundColor Cyan
        & "E:\DYT_01\00_CORE\setup.ps1"
    }
    "2" { 
        Write-Host "`n🚀 SẮP XẾP NỘI DUNG..." -ForegroundColor Cyan
        & "E:\DYT_01\01_CONTENT\organize.ps1"
    }
    "3" { 
        Write-Host "`n🚀 TẠO LỊCH ĐĂNG BÀI..." -ForegroundColor Cyan
        & "E:\DYT_01\02_CAMPAIGN\schedule.ps1"
    }
    "4" { 
        Write-Host "`n🚀 ĐĂNG BÀI LÊN THREADS..." -ForegroundColor Cyan
        & "E:\DYT_01\03_POST\threads_post.ps1" -auto
    }
    "5" { 
        Write-Host "`n🚀 TẠO LINK AFFILIATE..." -ForegroundColor Cyan
        & "E:\DYT_01\04_AFFILIATE\links.ps1"
    }
    "6" { 
        Write-Host "`n🚀 XEM THỐNG KÊ..." -ForegroundColor Cyan
        & "E:\DYT_01\05_MONITOR\views.ps1"
    }
    "7" { 
        Write-Host "`n🚀 BÁO CÁO DOANH THU..." -ForegroundColor Cyan
        & "E:\DYT_01\05_MONITOR\report.ps1"
    }
    "0" { Write-Host "`n👋 TẠM BIỆT!" -ForegroundColor Magenta }
    default { Write-Host "`n❌ LỰA CHỌN KHÔNG HỢP LỆ!" -ForegroundColor Red }
}
