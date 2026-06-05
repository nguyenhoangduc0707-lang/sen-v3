# reset.ps1
Clear-Host
Write-Host "🧹 RESET POWERSHELL" -ForegroundColor Cyan
Remove-Item (Get-PSReadlineOption).HistorySavePath -ErrorAction SilentlyContinue
Clear-History
Write-Host "✅ Đã xóa lịch sử và reset" -ForegroundColor Green
cd E:\DYT_01
Write-Host "📍 Đã về thư mục dự án" -ForegroundColor Yellow
