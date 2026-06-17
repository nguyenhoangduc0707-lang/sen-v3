# quick_fix.ps1
# Script sửa nhanh các lỗi phổ biến

Write-Host "🔧 Quick Fix Script - AI_OS_KERNEL_V3" -ForegroundColor Cyan

# 1. Clear cache
Write-Host "`n[1] Clearing Python cache..." -ForegroundColor Yellow
Get-ChildItem -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force
Write-Host "   ✅ Cache cleared"

# 2. Check port
Write-Host "`n[2] Checking port 8010..." -ForegroundColor Yellow
$portCheck = netstat -ano | Select-String ":8010"
if ($portCheck) {
    Write-Host "   ⚠️ Port in use, killing process..." -ForegroundColor Yellow
    $pid = ($portCheck -split '\s+')[-1]
    Stop-Process -Id $pid -Force
    Start-Sleep -Seconds 2
}
Write-Host "   ✅ Port 8010 is free"

# 3. Restart server
Write-Host "`n[3] Restarting server..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'E:\AI_OS_KERNEL_V3\AI_OS_KERNEL_V3'; python main.py"

Start-Sleep -Seconds 5

# 4. Test
Write-Host "`n[4] Testing server..." -ForegroundColor Yellow
try {
    $test = Invoke-RestMethod -Uri "http://127.0.0.1:8010/health" -TimeoutSec 5
    Write-Host "   ✅ Server is running!" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Server failed to start" -ForegroundColor Red
}

Write-Host "`n✅ Quick fix completed!" -ForegroundColor Green
