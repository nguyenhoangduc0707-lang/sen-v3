Write-Host "
🔍 Checking Power Settings..." -ForegroundColor Cyan

# Kiểm tra sleep settings
 = powercfg /query | Select-String "Standby (S3) Timeout" -Context 2,0
 = powercfg /query | Select-String "Standby (S3) Timeout" -Context 0,2

Write-Host "
📊 Current Sleep Settings:" -ForegroundColor Yellow
powercfg /query | Select-String "Sleep after"

Write-Host "
💡 Recommendations:" -ForegroundColor Green
Write-Host "   ✅ Sleep after: Should be 0 (Never)"
Write-Host "   ✅ Hibernate: Should be off"
Write-Host "   ✅ Display can turn off (still runs)"

Write-Host "
⚠️  Remember:" -ForegroundColor Red
Write-Host "   - Close laptop lid carefully (set 'Do nothing' in Power Options)"
Write-Host "   - Keep power adapter plugged in"
Write-Host "   - Restart computer after changes"
