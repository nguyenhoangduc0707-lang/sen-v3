# finalize-project.ps1
# Script dọn dẹp, cập nhật và đồng bộ toàn bộ dự án
# Chạy lần cuối trước khi đi ngủ

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "FINALIZE PROJECT - SAFE SYNC" -ForegroundColor Cyan
Write-Host "========================================"

# 1. Kiểm tra .gitignore
Write-Host ""
Write-Host "[1] CHECKING .GITIGNORE..." -ForegroundColor Yellow

$gitignoreContent = @"
# Sensitive files - NEVER COMMIT
.env
.env.local
.env.production
config/.env.production
credentials/
*.auth.json
*.auth
*.pem
*.key
*.crt
*.p12
*.secret
*.token
*.cookie
*.session
*.storage_state
secrets/

# Facebook auth
facebook_auth.json
scripts/save_facebook_auth.py
save_facebook_auth.py

# Database
*.db
*.db-shm
*.db-wal
*.sqlite
*.sqlite3

# Python
__pycache__/
*.pyc
*.pyo
.pytest_cache/
.coverage
htmlcov/
venv/
.venv/
env/
ENV/

# Logs
*.log
*.tmp
*.temp
logs/
tmp/
temp/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store
Thumbs.db

# Node / Frontend
frontend/node_modules/
node_modules/
.npm/
.yarn/
package-lock.json
yarn.lock

# Cloud
cloud_sql_credentials.json
service_account.json

# Git submodule
gemini-cli/

# Backup files
*.bak
*.backup
"@

# Đảm bảo .gitignore có nội dung đầy đủ
$current = Get-Content ".gitignore" -Raw -ErrorAction SilentlyContinue
if ($current -notmatch "credentials/") {
    $gitignoreContent | Out-File -FilePath ".gitignore" -Encoding UTF8 -Append
    Write-Host "OK: Updated .gitignore" -ForegroundColor Green
} else {
    Write-Host "OK: .gitignore already complete" -ForegroundColor Green
}

# 2. Xóa file nhạy cảm khỏi Git cache
Write-Host ""
Write-Host "[2] REMOVING SENSITIVE FILES FROM GIT..." -ForegroundColor Yellow
$sensitiveFiles = @(
    "config/.env.production",
    ".env",
    "credentials/facebook_auth.json",
    "facebook_auth.json",
    "save_facebook_auth.py",
    "scripts/save_facebook_auth.py"
)

foreach ($file in $sensitiveFiles) {
    if (Test-Path $file) {
        git rm --cached $file 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  Removed: $file" -ForegroundColor Green
        } else {
            Write-Host "  Not tracked: $file" -ForegroundColor Gray
        }
    }
}

# 3. Xóa gemini-cli submodule (nếu có)
Write-Host ""
Write-Host "[3] CHECKING GEMINI-CLI SUBMODULE..." -ForegroundColor Yellow
if (Test-Path "gemini-cli\.git") {
    Write-Host "Removing gemini-cli submodule..." -ForegroundColor Yellow
    git rm --cached gemini-cli 2>$null
    Remove-Item -Recurse -Force "gemini-cli" -ErrorAction SilentlyContinue
    Write-Host "OK: Removed gemini-cli submodule" -ForegroundColor Green
} else {
    Write-Host "OK: No gemini-cli submodule" -ForegroundColor Green
}

# 4. Add tất cả thay đổi
Write-Host ""
Write-Host "[4] ADDING CHANGES..." -ForegroundColor Yellow
git add .
Write-Host "OK: Changes staged" -ForegroundColor Green

# 5. Kiểm tra trạng thái
Write-Host ""
Write-Host "[5] CHECKING STATUS..." -ForegroundColor Yellow
git status --short

# 6. Commit
Write-Host ""
Write-Host "[6] COMMITTING..." -ForegroundColor Yellow
$commitMsg = "Finalize project: cleanup, security fix, sync all changes"
git commit -m $commitMsg
if ($LASTEXITCODE -eq 0) {
    Write-Host "OK: Committed successfully" -ForegroundColor Green
} else {
    Write-Host "WARN: No changes to commit" -ForegroundColor Yellow
}

# 7. Push lên remote
Write-Host ""
Write-Host "[7] PUSHING TO REMOTE..." -ForegroundColor Yellow
git push
if ($LASTEXITCODE -eq 0) {
    Write-Host "OK: Pushed to remote" -ForegroundColor Green
} else {
    Write-Host "ERROR: Push failed. Please check connection." -ForegroundColor Red
}

# 8. Kiểm tra file nhạy cảm còn sót
Write-Host ""
Write-Host "[8] FINAL SECURITY CHECK..." -ForegroundColor Yellow
$remaining = git ls-files | Select-String -Pattern "auth|secret|key|credential|token"
if ($remaining) {
    Write-Host "WARN: Still tracking sensitive files:" -ForegroundColor Yellow
    $remaining | ForEach-Object { Write-Host "  - $_" -ForegroundColor Yellow }
} else {
    Write-Host "OK: No sensitive files in Git" -ForegroundColor Green
}

# Summary
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "PROJECT FINALIZED SUCCESSFULLY!" -ForegroundColor Green
Write-Host "========================================"
Write-Host "All changes synced. Project is clean and safe." -ForegroundColor Yellow
Write-Host ""
Write-Host "You can now safely go to sleep. Good night!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan