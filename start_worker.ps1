# start_worker.ps1
# Terminal 2: Worker xử lý immediate tasks (content_creator, echo, shopee...)

# Fix encoding tiếng Việt
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001 | Out-Null | Out-Null

$dir = $PSScriptRoot
if (-not $dir) { $dir = Get-Location }

$Host.UI.RawUI.WindowTitle = 'DYT Core - 2: Worker (immediate tasks)'

Write-Host '=== DYT Core - Terminal 2: Worker ===' -ForegroundColor Cyan
Write-Host 'Xử lý task ngay (content, echo, shopee...). Dùng --run-once để drain nhanh test.' -ForegroundColor White

cd $dir

# Hỗ trợ truyền --run-once từ start_core.ps1
if ($args -contains '--run-once') {
    python run_worker.py --run-once
} else {
    python run_worker.py
}