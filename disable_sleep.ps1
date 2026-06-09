Write-Host "🛡️ Disabling Sleep Mode..." -ForegroundColor Cyan

# Tắt sleep
powercfg -setacvalueindex scheme_current sub_sleep standby-timeout-ac 0
powercfg -setdcvalueindex scheme_current sub_sleep standby-timeout-dc 0

# Tắt hibernate
powercfg -h off

# Áp dụng thay đổi
powercfg -setactive scheme_current

Write-Host "✅ Sleep has been disabled!" -ForegroundColor Green
Write-Host "
Current settings:" -ForegroundColor Yellow
powercfg /query | findstr "Sleep after"
