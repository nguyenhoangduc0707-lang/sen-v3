# start_core.ps1
# Script start TẤT CẢ Core ổn định (production-like) - 1 lệnh mở 3 terminal
# Chạy từ thư mục gốc project (Windows PowerShell):
#   powershell -ExecutionPolicy Bypass -File .\start_core.ps1
#
# Terminal 1: API (FastAPI + /api/v1/queue/enqueue)
# Terminal 2: Worker (xử lý immediate tasks)
# Terminal 3: Scheduled Poster (đăng FB đúng giờ theo lịch đã optimize)

param(
    [switch]$DryRun,
    [switch]$WorkerOnce   # Thêm: chạy worker ở chế độ drain một lần (hữu ích test)
)

# Fix encoding cho tiếng Việt hiển thị đúng (PHẢI đặt NGAY sau param())
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001 | Out-Null | Out-Null


$projectRoot = $PSScriptRoot
if (-not $projectRoot) { $projectRoot = Get-Location }

Write-Host "================================================================" -ForegroundColor Green
Write-Host "  Starting DYT-01 / SEN V3 Core (production-like) - 3 terminals" -ForegroundColor Green
Write-Host "  Project: $projectRoot" -ForegroundColor Yellow
Write-Host "================================================================" -ForegroundColor Green

if ($DryRun) {
    Write-Host "[DRY] Would start 3 windows using the modular start_*.ps1 files. Skipping." -ForegroundColor Yellow
} else {
    # Use the small dedicated scripts (easier to edit individually later)
    $apiScript = Join-Path $projectRoot 'start_api.ps1'
    $workerScript = Join-Path $projectRoot 'start_worker.ps1'
    $schedScript = Join-Path $projectRoot 'start_scheduled.ps1'

    # Terminal 1: API
    Start-Process powershell -ArgumentList "-NoExit", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", $apiScript
    Start-Sleep -Milliseconds 600

    # Terminal 2: Worker (có thể truyền --run-once nếu muốn drain nhanh)
    $workerArgs = @("-NoExit", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", $workerScript)
    if ($WorkerOnce) { $workerArgs += "--run-once" }
    Start-Process powershell -ArgumentList $workerArgs
    Start-Sleep -Milliseconds 600

    # Terminal 3: Scheduled (FB đúng giờ)
    Start-Process powershell -ArgumentList "-NoExit", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", $schedScript

    Write-Host "`n✅ Đã mở 3 cửa sổ PowerShell (bằng start_*.ps1)." -ForegroundColor Green
    if ($WorkerOnce) {
        Write-Host "   (Worker đang chạy ở chế độ --run-once - drain 1 lần rồi thoát)" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "1. API       : http://localhost:8000/docs   (POST /api/v1/queue/enqueue để đưa task vào queue)" -ForegroundColor White
Write-Host "2. Worker    : Xử lý task immediate (content_creator, ...). Dùng --run-once để drain nhanh." -ForegroundColor White
Write-Host "3. Scheduled : Tự poll và post FB đúng giờ (scheduled_at) cho các fanpage." -ForegroundColor White

Write-Host ""
Write-Host "=== Lệnh hay dùng sau khi Core chạy ===" -ForegroundColor Cyan
Write-Host "  # Xem trước lịch 3 ngày cho 2 page thật của bạn (không enqueue):" -ForegroundColor White
Write-Host "  python schedule_optimized_posts.py --fanpage_key affiliate_fashion_cosmetics --days 3 --dry_run" -ForegroundColor Gray
Write-Host "  python schedule_optimized_posts.py --fanpage_key motivational_postcard --days 3 --dry_run" -ForegroundColor Gray
Write-Host ""
Write-Host "  # Schedule thật (enqueue vào queue với scheduled_at) cho 3 ngày:" -ForegroundColor White
Write-Host "  python schedule_optimized_posts.py --fanpage_key affiliate_fashion_cosmetics --days 3" -ForegroundColor Gray
Write-Host "  python schedule_optimized_posts.py --fanpage_key motivational_postcard --days 3" -ForegroundColor Gray
Write-Host ""
Write-Host "  # Xem hiệu suất & tối ưu conversion từ data nội bộ:" -ForegroundColor White
Write-Host "  python analyze_performance.py" -ForegroundColor Gray
Write-Host ""
Write-Host "  # Test nhanh enqueue + process:" -ForegroundColor White
Write-Host "  python enqueue_task.py content_creator '{\"campaign_info\":{\"name\":\"Test\"},\"theme\":\"affiliate\",\"fanpage_key\":\"affiliate_fashion_cosmetics\"}'" -ForegroundColor Gray
Write-Host "  python process_pending.py" -ForegroundColor Gray

Write-Host ""
Write-Host "=== Lưu ý quan trọng ===" -ForegroundColor Magenta
Write-Host "- Cập nhật best_posting_times trong config/fanpages.json từ Insights của page để tối ưu tốt hơn." -ForegroundColor White
Write-Host "- Data nội bộ (COMPLETED tasks) sẽ tự động override config khi đủ mẫu (>=5)." -ForegroundColor White
Write-Host "- Muốn đăng thật FB: cần facebook_auth.json (chạy script login 1 lần)." -ForegroundColor White
Write-Host "- AI Tech & banking sẵn sàng (chỉ cần điền URL thật vào config khi có)." -ForegroundColor White
Write-Host "- Conversion tracking: sau này log clicks/sales → optimizer sẽ dùng để tối ưu chính xác hơn." -ForegroundColor White

Write-Host ""
Write-Host "Core đã sẵn sàng chạy ổn định. Chạy script này mỗi khi muốn mở lại 3 terminal." -ForegroundColor Green
Write-Host "Xem chi tiết: CORE_START_GUIDE.md" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Green
