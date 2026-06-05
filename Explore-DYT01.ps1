<#
.SYNOPSIS
    Kham pha du an DYT_01 - Phien ban khong loi cau truc
#>

Set-Location C:\DYT_01
Write-Host "=== BAT DAU KHAM PHA DU AN DYT_01 ===" -ForegroundColor Cyan
Write-Host "Thoi gian: $(Get-Date)" -ForegroundColor Gray
Write-Host ""

# 1. Cay thu muc
Write-Host "1. CAY THU MUC [100 dong dau]" -ForegroundColor Green
tree /F | Select-Object -First 100
Write-Host "`n--- De xem day du, go: tree /F | more ---`n" -ForegroundColor Gray

# 2. Liet ke file
Write-Host "2. DANH SACH FILE THEO LOAI" -ForegroundColor Green
Write-Host "--- File Python [tru venv va __pycache__] ---" -ForegroundColor Yellow
Get-ChildItem -Recurse -File -Filter *.py | Where-Object { $_.FullName -notmatch "\\venv\\|\\__pycache__\\" } | Select-Object -ExpandProperty FullName -First 50
Write-Host "... [hien thi 50 dong dau]" -ForegroundColor Gray

Write-Host "`n--- File cau hinh [.env, .json, .yaml, .ini] ---" -ForegroundColor Yellow
Get-ChildItem -Recurse -File -Include *.env,*.json,*.yaml,*.yml,*.ini,*.cfg | Select-Object -ExpandProperty FullName
Write-Host ""

# 3. Doc file quan trong
Write-Host "3. NOI DUNG FILE QUAN TRONG [tom tat]" -ForegroundColor Green
$importantFiles = @(
    @{Path="README_CONFIG.md"; MaxLines=30; Desc="README_CONFIG.md"},
    @{Path=".env"; MaxLines=20; Desc="Bien moi truong [an mot phan]"},
    @{Path="requirements.txt"; MaxLines=50; Desc="Python dependencies chinh"}
)
foreach ($f in $importantFiles) {
    Write-Host "--- $($f.Desc) ---" -ForegroundColor Yellow
    if (Test-Path $f.Path) {
        Get-Content $f.Path -Head $f.MaxLines -ErrorAction SilentlyContinue
        $lineCount = (Get-Content $f.Path | Measure-Object).Count
        if ($lineCount -gt $f.MaxLines) {
            Write-Host "... [chi hien thi $($f.MaxLines) dong dau]" -ForegroundColor Gray
        }
    } else {
        Write-Host "Khong tim thay file: $($f.Path)" -ForegroundColor Red
    }
    Write-Host ""
}

# 4. Entry points
Write-Host "4. DIEM ENTRY CHINH [cac file Python co main]" -ForegroundColor Green
Select-String -Path "*.py",".\src\*.py",".\tasks\*.py",".\scripts\*.py" -Pattern 'if __name__\s*==\s*["\']__main__["\']' -List | Select-Object -ExpandProperty Filename -Unique
Write-Host "`nNoi dung mot so file chinh:" -ForegroundColor Yellow
foreach ($entry in @("main.py","manage.py","run_api.py","run_worker.py","run_picker_v2.py")) {
    if (Test-Path $entry) {
        Write-Host "=== $entry [20 dong dau] ===" -ForegroundColor Cyan
        Get-Content $entry -Head 20
        Write-Host ""
    }
}

# 5. Database migrations
Write-Host "5. DATABASE MIGRATIONS" -ForegroundColor Green
if (Test-Path ".\alembic\versions") {
    Write-Host "--- Cac migration da co ---" -ForegroundColor Yellow
    Get-ChildItem .\alembic\versions -Filter *.py | Select-Object Name
    Write-Host "`n--- Noi dung alembic.ini ---" -ForegroundColor Yellow
    Get-Content alembic.ini -Head 30
} else {
    Write-Host "Khong tim thay thu muc alembic\versions" -ForegroundColor Red
}

# 6. Agent va AI
Write-Host "6. CAC AGENT VA XU LY AI" -ForegroundColor Green
$agentFiles = Get-ChildItem -Recurse -File -Include *agent*.py,*comparator*.py,*grader*.py,*improvement*.py | Where-Object { $_.FullName -notmatch "\\venv\\" }
foreach ($af in $agentFiles) {
    Write-Host "- $($af.Name) : $($af.FullName)" -ForegroundColor Yellow
    Write-Host "  10 dong dau tien:" -ForegroundColor Gray
    Get-Content $af.FullName -Head 10
    Write-Host ""
}

# 7. Tim cau hinh nham
Write-Host "7. TIM CAU HINH NHAM [API_KEY, DATABASE_URL, ...]" -ForegroundColor Green
$patterns = @("DATABASE_URL","API_KEY","SECRET","PASSWORD","TOKEN")
foreach ($pat in $patterns) {
    Write-Host "--- Tim '$pat' ---" -ForegroundColor Yellow
    Select-String -Path "*.py",".\src\*.py",".\scripts\*.py" -Pattern $pat -CaseSensitive:$false | Select-Object Filename, LineNumber, Line -First 5
    Write-Host ""
}

# 8. Log gan day
Write-Host "8. LOG GAN DAY" -ForegroundColor Green
if (Test-Path ".\logs") {
    $recentLogs = Get-ChildItem .\logs -File | Sort-Object LastWriteTime -Descending | Select-Object -First 3
    foreach ($log in $recentLogs) {
        Write-Host "--- $($log.Name) [20 dong cuoi] ---" -ForegroundColor Yellow
        Get-Content $log.FullName -Tail 20
        Write-Host ""
    }
} else {
    Write-Host "Thu muc logs khong ton tai hoac trong" -ForegroundColor Red
}

# 9. Thong ke nhanh
Write-Host "9. THONG KE NHANH" -ForegroundColor Green
$pyCount = (Get-ChildItem -Recurse -File -Filter *.py | Where-Object { $_.FullName -notmatch "\\venv\\" }).Count
$jsCount = (Get-ChildItem -Recurse -File -Include *.js,*.jsx,*.ts,*.tsx | Measure-Object).Count
$dbCount = (Get-ChildItem .\alembic\versions -Filter *.py -ErrorAction SilentlyContinue).Count
Write-Host "File Python [tru venv] : $pyCount"
Write-Host "File frontend [js/jsx/ts/tsx] : $jsCount"
Write-Host "Database migrations : $dbCount"
Write-Host "Main entry points: main.py, manage.py, run_api.py, run_worker.py, run_picker_v2.py"
Write-Host "Xem README_CONFIG.md de biet huong dan cau hinh."

# 10. Cay thu muc kich thuoc
Write-Host "`n10. CAY THU MUC KEM DUNG LUONG [chi thu muc]" -ForegroundColor Green
function Get-DirTreeWithSize($Path = ".", $Indent = "") {
    Get-ChildItem $Path -Directory -ErrorAction SilentlyContinue | ForEach-Object {
        $sizeKB = [math]::Round((Get-ChildItem $_.FullName -Recurse -File -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1KB, 2)
        $sizeStr = if ($sizeKB -gt 1024) { "{0:N2} MB" -f ($sizeKB/1024) } else { "{0:N2} KB" -f $sizeKB }
        "$Indent+ $($_.Name) [$sizeStr]"
        Get-DirTreeWithSize $_.FullName "$Indent  "
    }
}
Get-DirTreeWithSize
Write-Host "`n=== KET THUC ===" -ForegroundColor Cyan