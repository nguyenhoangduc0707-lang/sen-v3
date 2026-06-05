# DEPLOY.ps1  â€”  Script nÃ¢ng cáº¥p SEN V3 (cháº¡y tá»« C:\DYT_01)
# Cháº¡y: .\DEPLOY.ps1
# YÃªu cáº§u: venv Ä‘Ã£ táº¡o sáºµn táº¡i C:\DYT_01\venv

$ErrorActionPreference = "Stop"
$ROOT = "C:\DYT_01"
$UPGRADE_DIR = "$PSScriptRoot"

Write-Host "`n[1/5] Backup file gá»‘c..." -ForegroundColor Cyan
$ts = Get-Date -Format "yyyyMMdd_HHmm"
Copy-Item "$ROOT\content_creation_agent.py" "$ROOT\content_creation_agent.py.bak_$ts" -ErrorAction SilentlyContinue
Copy-Item "$ROOT\src\workers\content_worker.py" "$ROOT\src\workers\content_worker.py.bak_$ts" -ErrorAction SilentlyContinue
Write-Host "  âœ… Backup xong" -ForegroundColor Green

Write-Host "`n[2/5] Copy file nÃ¢ng cáº¥p..." -ForegroundColor Cyan
Copy-Item "$UPGRADE_DIR\content_creation_agent.py" "$ROOT\content_creation_agent.py" -Force
Copy-Item "$UPGRADE_DIR\content_worker.py"         "$ROOT\src\workers\content_worker.py" -Force
Copy-Item "$UPGRADE_DIR\test_ai.py"                "$ROOT\test_ai.py" -Force
Write-Host "  âœ… Copy xong" -ForegroundColor Green

Write-Host "`n[3/5] CÃ i dependencies..." -ForegroundColor Cyan
& "$ROOT\venv\Scripts\pip.exe" install google-genai python-dotenv --quiet
Write-Host "  âœ… Dependencies OK" -ForegroundColor Green

Write-Host "`n[4/5] Kiá»ƒm tra GEMINI_API_KEY trong .env..." -ForegroundColor Cyan
$envContent = Get-Content "$ROOT\.env" -Raw -ErrorAction SilentlyContinue
if ($envContent -match "GEMINI_API_KEY=gemini_real_xxxxx") {
    Write-Host "  âœ… Key cÃ³ váº» há»£p lá»‡" -ForegroundColor Green
} else {
    Write-Host "  âš ï¸  GEMINI_API_KEY cÃ³ thá»ƒ chÆ°a há»£p lá»‡" -ForegroundColor Yellow
    Write-Host "  â†’ Láº¥y key táº¡i: https://aistudio.google.com/apikey" -ForegroundColor Yellow
    Write-Host "  â†’ Cáº­p nháº­t trong file: $ROOT\.env" -ForegroundColor Yellow
}

Write-Host "`n[5/5] Cháº¡y test..." -ForegroundColor Cyan
Set-Location $ROOT
& "$ROOT\venv\Scripts\python.exe" test_ai.py

Write-Host "`nâœ… DEPLOY XONG! Khá»Ÿi Ä‘á»™ng láº¡i worker Ä‘á»ƒ Ã¡p dá»¥ng:" -ForegroundColor Green
Write-Host "   python run_worker.py" -ForegroundColor White

