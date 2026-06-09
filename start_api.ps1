# start_api.ps1
# Terminal 1: FastAPI (enqueue tại /api/v1/queue/enqueue + /api/v1/queue/tasks)

# Fix encoding tiếng Việt
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001 | Out-Null | Out-Null

$dir = $PSScriptRoot
if (-not $dir) { $dir = Get-Location }

$Host.UI.RawUI.WindowTitle = 'DYT Core - 1: API (8000)'

Write-Host '=== DYT Core - Terminal 1: API ===' -ForegroundColor Cyan
Write-Host 'Swagger UI : http://localhost:8000/docs' -ForegroundColor White
Write-Host 'Enqueue    : POST /api/v1/queue/enqueue' -ForegroundColor White

cd $dir
python run_api.py