Write-Host "`n"
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "      🔒 KIỂM TRA BẢO MẬT TOÀN BỘ DỰ ÁN 🔒" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""

# 1. Kiểm tra file .env (file cấu hình quan trọng nhất)
Write-Host "📋 1. KIỂM TRA FILE CẤU HÌNH" -ForegroundColor Yellow
Write-Host "   File .env:" -ForegroundColor Gray
if (Test-Path "E:\DYT_01\.env") {
    $envContent = Get-Content "E:\DYT_01\.env" -ErrorAction SilentlyContinue
    foreach ($line in $envContent) {
        if ($line -match "=" -and $line -notmatch "^#") {
            $key = ($line -split "=")[0]
            $value = ($line -split "=")[1]
            if ($value -and $value -ne "" -and $value -notmatch "your_|default|changeme|test") {
                $masked = if ($value.Length -gt 10) { "$($value.Substring(0,5))*****" } else { "*****" }
                Write-Host "      ✅ $key = $masked" -ForegroundColor Green
            } elseif ($value -match "your_|default|changeme|test") {
                Write-Host "      ⚠️  $key = $value (CẦN THAY ĐỔI)" -ForegroundColor Red
            }
        }
    }
} else {
    Write-Host "      ⚠️  Chưa có file .env!" -ForegroundColor Red
}

# 2. Tìm các file chứa API key/hardcoded secret
Write-Host "`n📋 2. TÌM KEY CỨNG TRONG CODE" -ForegroundColor Yellow
$searchPatterns = @("API_KEY", "SECRET_KEY", "TOKEN", "PASSWORD", "ACCESS_KEY", "PRIVATE_KEY")
$foundIssues = @()

foreach ($pattern in $searchPatterns) {
    $results = Select-String -Path "E:\DYT_01\*.py" -Pattern $pattern -Exclude "venv*", "__pycache__*", "backup*", "debug_*", "test_*", "check_*", "create_*" -ErrorAction SilentlyContinue
    foreach ($result in $results) {
        $line = $result.Line.Trim()
        if ($line -notmatch "#.*$pattern" -and $line -notmatch "print" -and $line -notmatch "logger") {
            if ($line -match "=.*['`"][^'`"]+['`"]") {
                $foundIssues += "   ⚠️  $($result.Filename): $pattern found"
                Write-Host "      ⚠️  $($result.Filename): dòng $($result.LineNumber)" -ForegroundColor Red
            }
        }
    }
}

if ($foundIssues.Count -eq 0) {
    Write-Host "      ✅ Không tìm thấy key cứng trong code" -ForegroundColor Green
}

# 3. Kiểm tra file .gitignore
Write-Host "`n📋 3. KIỂM TRA .GITIGNORE" -ForegroundColor Yellow
if (Test-Path "E:\DYT_01\.gitignore") {
    $gitignore = Get-Content "E:\DYT_01\.gitignore" -ErrorAction SilentlyContinue
    $hasEnv = $gitignore | Select-String ".env"
    $hasVenv = $gitignore | Select-String "venv"
    $hasPycache = $gitignore | Select-String "__pycache__"
    
    if ($hasEnv) { Write-Host "      ✅ .env được bảo vệ" -ForegroundColor Green }
    else { Write-Host "      ❌ .env CHƯA được thêm vào .gitignore!" -ForegroundColor Red }
    
    if ($hasVenv) { Write-Host "      ✅ venv được bảo vệ" -ForegroundColor Green }
    else { Write-Host "      ⚠️  venv chưa được thêm vào .gitignore" -ForegroundColor Yellow }
    
    if ($hasPycache) { Write-Host "      ✅ __pycache__ được bảo vệ" -ForegroundColor Green }
    else { Write-Host "      ⚠️  __pycache__ chưa được thêm vào .gitignore" -ForegroundColor Yellow }
} else {
    Write-Host "      ❌ Chưa có file .gitignore!" -ForegroundColor Red
}

# 4. Kiểm tra các nguồn mở (open sources)
Write-Host "`n📋 4. KIỂM TRA CÁC NGUỒN MỞ (requirements)" -ForegroundColor Yellow
if (Test-Path "E:\DYT_01\requirements.txt") {
    $requirements = Get-Content "E:\DYT_01\requirements.txt" -ErrorAction SilentlyContinue
    Write-Host "      Các thư viện chính:" -ForegroundColor Gray
    $requirements | Select-Object -First 10 | ForEach-Object {
        Write-Host "        - $_" -ForegroundColor Gray
    }
} else {
    Write-Host "      ⚠️  Không tìm thấy requirements.txt" -ForegroundColor Yellow
}

# 5. Kiểm tra notebooklm (Google Colab/Jupyter)
Write-Host "`n📋 5. KIỂM TRA NOTEBOOKLM" -ForegroundColor Yellow
$notebookFiles = Get-ChildItem -Path "E:\DYT_01" -Recurse -Include "*.ipynb" -Exclude "venv*", "__pycache__*" -ErrorAction SilentlyContinue
if ($notebookFiles) {
    Write-Host "      Tìm thấy $($notebookFiles.Count) notebook(s):" -ForegroundColor Yellow
    foreach ($nb in $notebookFiles) {
        Write-Host "        - $($nb.Name)" -ForegroundColor Gray
        # Kiểm tra notebook có chứa key không
        $nbContent = Get-Content $nb.FullName -Raw -ErrorAction SilentlyContinue
        if ($nbContent -match "API_KEY|SECRET|PASSWORD|TOKEN") {
            Write-Host "          ⚠️  Notebook này có thể chứa key!" -ForegroundColor Red
        }
    }
} else {
    Write-Host "      ✅ Không tìm thấy notebook files" -ForegroundColor Green
}

# 6. Kiểm tra port đang mở
Write-Host "`n📋 6. KIỂM TRA PORT ĐANG CHẠY" -ForegroundColor Yellow
$ports = @(8000, 3000, 5000, 8080)
foreach ($port in $ports) {
    $portCheck = netstat -an | Select-String ":$port " | Select-String "LISTENING"
    if ($portCheck) {
        Write-Host "      ⚠️  Port $port đang được sử dụng" -ForegroundColor Yellow
    }
}

# 7. Tổng kết bảo mật
Write-Host "`n" + "=" * 60 -ForegroundColor Cyan
Write-Host "         📊 TỔNG KẾT BẢO MẬT" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""
Write-Host "🔐 Khuyến nghị:" -ForegroundColor Yellow
Write-Host "   1. Tạo file .env riêng cho production" -ForegroundColor White
Write-Host "   2. Không commit file .env lên Git" -ForegroundColor White
Write-Host "   3. Sử dụng biến môi trường thay vì hardcode" -ForegroundColor White
Write-Host "   4. Đổi JWT_SECRET_KEY thành key dài 32+ ký tự" -ForegroundColor White
Write-Host "   5. Chạy server với DEBUG=False trong production" -ForegroundColor White
Write-Host ""

