# git-update-safe.ps1
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Kiem tra bao mat truoc khi commit" -ForegroundColor Cyan
Write-Host "========================================"

# 1. Kiem tra file nhay cam
Write-Host "`n[1] Kiem tra file nhay cam trong Git..."
$sensitive = @("facebook_auth.json", "credentials/facebook_auth.json", ".env", "*.auth.json", "*.secret")
$tracked = git ls-files
$found = @()
foreach ($s in $sensitive) {
    if ($tracked -match $s) {
        $found += $s
    }
}
if ($found.Count -gt 0) {
    Write-Host "WARNING: Phat hien file nhay cam dang duoc track:" -ForegroundColor Red
    $found | ForEach-Object { Write-Host "  - $_" }
    Write-Host "De xoa khoi Git (giu lai local):" -ForegroundColor Yellow
    foreach ($f in $found) {
        Write-Host "  git rm --cached $f"
    }
} else {
    Write-Host "OK: Khong phat hien file nhay cam nao" -ForegroundColor Green
}

# 2. Kiem tra .gitignore
Write-Host "`n[2] Kiem tra .gitignore..."
if (Test-Path .gitignore) {
    $content = Get-Content .gitignore -Raw
    $patterns = @("credentials/", "*.auth.json", ".env", "*.db", "sen_v3.db", "app.db")
    $missing = @()
    foreach ($p in $patterns) {
        if ($content -notmatch $p) {
            $missing += $p
        }
    }
    if ($missing.Count -gt 0) {
        Write-Host "WARNING: Thieu cac pattern sau:" -ForegroundColor Yellow
        $missing | ForEach-Object { Write-Host "  - $_" }
    } else {
        Write-Host "OK: .gitignore da day du" -ForegroundColor Green
    }
} else {
    Write-Host "WARNING: Khong tim thay .gitignore" -ForegroundColor Yellow
}

# 3. Hien thi trang thai Git
Write-Host "`n[3] Trang thai Git hien tai:"
git status

# 4. Hoi commit
Write-Host "`nBan muon add va commit tat ca thay doi? (y/n)"
$choice = Read-Host
if ($choice -eq "y") {
    git add .
    $msg = Read-Host "Nhap commit message"
    if ($msg -eq "") { $msg = "Update project" }
    git commit -m $msg
    Write-Host "Da commit: $msg" -ForegroundColor Green
    Write-Host "Ban co muon push len remote? (y/n)"
    $push = Read-Host
    if ($push -eq "y") {
        git push
        Write-Host "Da push" -ForegroundColor Green
    }
}

Write-Host "`nHOAN TAT!" -ForegroundColor Cyan