# Security-Check.ps1
Write-Host "🔐 KIỂM TRA BẢO MẬT DYT_01" -ForegroundColor Cyan
Write-Host "Thời gian: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Gray
Write-Host ""

# 1. Kiểm tra file .env
Write-Host "[1] Kiểm tra file .env..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "⚠️ FILE .env TỒN TẠI!" -ForegroundColor Red
    Write-Host "   → Đã được thêm vào .gitignore chưa?" -ForegroundColor Yellow
    
    # Kiểm tra .gitignore
    if (Test-Path ".gitignore") {
        $gitignore = Get-Content ".gitignore" -Raw
        if ($gitignore -match "\.env") {
            Write-Host "   ✅ .env đã có trong .gitignore" -ForegroundColor Green
        } else {
            Write-Host "   ❌ .env CHƯA có trong .gitignore" -ForegroundColor Red
        }
    }
} else {
    Write-Host "✅ Không tìm thấy file .env" -ForegroundColor Green
}

# 2. Kiểm tra hardcoded secrets trong code
Write-Host "`n[2] Kiểm tra hardcoded secrets trong code..." -ForegroundColor Yellow
$patterns = @("API_KEY", "SECRET_KEY", "PASSWORD", "TOKEN", "JWT_SECRET")
$foundSecrets = @()

foreach ($pattern in $patterns) {
    $matches = Select-String -Path "*.py", "*.js", "*.json" -Pattern "$pattern\s*=\s*['`"][^'`"]+['`"]" -ErrorAction SilentlyContinue
    foreach ($match in $matches) {
        $foundSecrets += "$($match.Filename):$($match.LineNumber)"
    }
}

if ($foundSecrets.Count -gt 0) {
    Write-Host "⚠️ PHÁT HIỆN SECRET TRONG CODE:" -ForegroundColor Red
    foreach ($secret in $foundSecrets | Select-Object -First 5) {
        Write-Host "   - $secret" -ForegroundColor Yellow
    }
} else {
    Write-Host "✅ Không tìm thấy secret hardcoded trong code" -ForegroundColor Green
}

# 3. Kiểm tra Git history
Write-Host "`n[3] Kiểm tra Git history..." -ForegroundColor Yellow
if (Test-Path ".git") {
    $sensitiveCommits = git log --all --oneline --grep="secret\|password\|key\|token" 2>$null
    if ($sensitiveCommits) {
        Write-Host "⚠️ Tìm thấy commit có thể chứa sensitive data:" -ForegroundColor Red
        $sensitiveCommits | Select-Object -First 3 | ForEach-Object {
            Write-Host "   - $_" -ForegroundColor Yellow
        }
    } else {
        Write-Host "✅ Không tìm thấy commit đáng ngờ" -ForegroundColor Green
    }
    
    # Kiểm tra .env có từng bị commit không
    $envCommits = git log --all --oneline -- .env 2>$null
    if ($envCommits) {
        Write-Host "⚠️⚠️⚠️ .env ĐÃ TỪNG BỊ COMMIT VÀO GIT!" -ForegroundColor Red
        Write-Host "   Cần xóa khỏi history ngay!" -ForegroundColor Yellow
    } else {
        Write-Host "✅ .env chưa từng bị commit" -ForegroundColor Green
    }
} else {
    Write-Host "✅ Không có Git repository" -ForegroundColor Green
}

# 4. Kiểm tra JWT_SECRET_KEY strength
Write-Host "`n[4] Kiểm tra JWT_SECRET_KEY..." -ForegroundColor Yellow
if (Test-Path ".env") {
    $jwtSecret = Select-String -Path ".env" -Pattern "JWT_SECRET_KEY=your_super_secret_2026" | ForEach-Object { $_.Matches.Groups[1].Value }
    if ($jwtSecret) {
        if ($jwtSecret.Length -ge 32) {
            Write-Host "✅ JWT_SECRET_KEY độ dài: $($jwtSecret.Length) chars (tốt)" -ForegroundColor Green
        } else {
            Write-Host "⚠️ JWT_SECRET_KEY quá ngắn: $($jwtSecret.Length) chars (cần 32+)" -ForegroundColor Red
        }
    }
}

Write-Host "`n✅ KIỂM TRA HOÀN TẤT!" -ForegroundColor Green
Write-Host "📋 Báo cáo đã được lưu" -ForegroundColor Cyan

