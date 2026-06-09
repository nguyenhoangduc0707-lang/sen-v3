# start_scheduled.ps1
# Terminal 3: Scheduled poster - đăng FB đúng giờ theo lịch đã optimize từ data nội bộ (COMPLETED tasks làm proxy conversion)

# Fix encoding tiếng Việt
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001 | Out-Null | Out-Null

$dir = $PSScriptRoot
if (-not $dir) { $dir = Get-Location }

$Host.UI.RawUI.WindowTitle = 'DYT Core - 3: Scheduled Poster (FB đúng giờ)'

Write-Host '=== DYT Core - Terminal 3: Scheduled Poster ===' -ForegroundColor Cyan
Write-Host 'Tự động post các task facebook_autoposter có scheduled_at <= now().' -ForegroundColor White
Write-Host 'Chỉ 2 page thật: affiliate_fashion_cosmetics + motivational_postcard' -ForegroundColor White

cd $dir

# Nhắc nhở auth (rất quan trọng)
if (-not (Test-Path "facebook_auth.json")) {
    Write-Host "`n⚠️  CHƯA CÓ facebook_auth.json !" -ForegroundColor Red
    Write-Host "   Chạy: python save_facebook_auth.py  (hoặc test_facebook_auth.py)" -ForegroundColor Yellow
    Write-Host "   Sau đó chạy lại script này." -ForegroundColor Yellow
    Read-Host "Nhấn Enter để tiếp tục (sẽ fail nếu không có auth)..."
}

python run_scheduled_posts.py