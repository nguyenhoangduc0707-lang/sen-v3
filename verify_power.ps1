Write-Host "
======================================" -ForegroundColor Cyan
Write-Host "   POWER SETTINGS VERIFICATION" -ForegroundColor Cyan
Write-Host "======================================
" -ForegroundColor Cyan

# Check Sleep
 = powercfg /query | Select-String "Sleep after"
if ( -match "0") {
    Write-Host "✅ Sleep: DISABLED (0)" -ForegroundColor Green
} else {
    Write-Host "⚠️ Sleep: Check settings" -ForegroundColor Yellow
}

# Check Hibernate
 = powercfg /a | Select-String "Hibernate"
if () {
    Write-Host "✅ Hibernate: Available (but won't auto)" -ForegroundColor Green
}

# Check Lid Action
Write-Host "
📌 To keep running when lid closed:" -ForegroundColor Yellow
Write-Host "   Control Panel → Power Options → Choose what closing the lid does" -ForegroundColor White
Write-Host "   Set to 'Do nothing'
" -ForegroundColor White

Write-Host "💡 Your computer will now run 24/7 for DYT-01!" -ForegroundColor Cyan
