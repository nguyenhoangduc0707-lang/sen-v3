# Prevent Sleep Script
Write-Host "🛡️ Preventing Windows from sleeping..." -ForegroundColor Green

# Tắt sleep
powercfg /change standby-timeout-ac 0
powercfg /change standby-timeout-dc 0

# Tắt hibernate
powercfg /hibernate off

# Hiển thị trạng thái
Write-Host "
✅ Current power settings:" -ForegroundColor Yellow
powercfg /query | Select-String "Sleep after"

Write-Host "
💡 Computer will now run 24/7" -ForegroundColor Cyan
Write-Host "⚠️  Make sure to save work before restart" -ForegroundColor Red
