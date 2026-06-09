$ErrorActionPreference = "Stop"
$target = "E:\DYT_01\src\workers\facebook_autoposter.py"
$fixFile = "E:\DYT_01\facebook_autoposter_fix.py"

Write-Host "=== APPLY FACEBOOK_AUTOPOSTER FIX v2.2 ===" -ForegroundColor Cyan

# 1. Backup
$backup = "$target.bak_20260605_235503"
Copy-Item $target $backup
Write-Host "[OK] Backed up to: $backup" -ForegroundColor Green

# 2. Apply
Copy-Item $fixFile $target -Force
Write-Host "[OK] Applied fix to: $target" -ForegroundColor Green
