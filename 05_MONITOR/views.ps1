# ============================================
# XEM THỐNG KÊ
# ============================================

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "📊 THỐNG KÊ DỰ ÁN" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan

# Đọc file lịch nếu có
$scheduleFiles = Get-ChildItem "E:\DYT_01\VinWonders_Project\05_Management\Schedules\*.csv" -ErrorAction SilentlyContinue

if ($scheduleFiles) {
    $latestSchedule = $scheduleFiles | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    $data = Import-Csv $latestSchedule.FullName
    
    $total = $data.Count
    $posted = ($data | Where-Object { $_.Status -eq "Posted" }).Count
    $pending = ($data | Where-Object { $_.Status -eq "Pending" }).Count
    
    Write-Host "`n📋 LỊCH ĐĂNG BÀI:" -ForegroundColor Yellow
    Write-Host "   Tổng số bài: $total" -ForegroundColor White
    Write-Host "   Đã đăng: $posted" -ForegroundColor Green
    Write-Host "   Chờ đăng: $pending" -ForegroundColor Yellow
    Write-Host "   Thu nhập dự kiến: $($total * 150000)đ" -ForegroundColor Cyan
} else {
    Write-Host "`n⚠️ Chưa có lịch đăng bài. Hãy chạy CAMPAIGN trước!" -ForegroundColor Yellow
}

Write-Host "`n✅ HOÀN TẤT!" -ForegroundColor Green
