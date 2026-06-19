# health-security-audit.ps1
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "SYSTEM HEALTH AND SECURITY AUDIT" -ForegroundColor Cyan
Write-Host "========================================"

$Report = @()
$Issues = @()
$Warnings = @()
$Pass = @()

# 1. Check .env file
Write-Host "`n[1] CHECKING .ENV FILE..." -ForegroundColor Yellow
if (Test-Path ".env") {
    $Pass += ".env file exists"
    Write-Host "OK: .env exists" -ForegroundColor Green
    $envContent = Get-Content ".env" -Raw -ErrorAction SilentlyContinue
    $requiredVars = @("DATABASE_URL", "JWT_SECRET_KEY", "FERNET_KEY", "GEMINI_API_KEY")
    $missingVars = @()
    foreach ($var in $requiredVars) {
        if ($envContent -notmatch "$var\s*=") {
            $missingVars += $var
        }
    }
    if ($missingVars.Count -gt 0) {
        $Warnings += "Missing environment variables: $($missingVars -join ', ')"
        Write-Host "WARN: Missing environment variables: $($missingVars -join ', ')" -ForegroundColor Yellow
    } else {
        $Pass += "All required environment variables set"
        Write-Host "OK: All required environment variables set" -ForegroundColor Green
    }
} else {
    $Issues += ".env file not found"
    Write-Host "ERROR: .env file not found (create from .env.example)" -ForegroundColor Red
}

# 2. Check sensitive files in Git
Write-Host "`n[2] CHECKING SENSITIVE FILES IN GIT..." -ForegroundColor Yellow
$sensitivePatterns = @("auth", "secret", "credential", "token", ".env", "*.pem", "*.key", "*.crt", "*.p12")
$trackedFiles = git ls-files 2>$null
$foundSensitive = @()
foreach ($pattern in $sensitivePatterns) {
    $matches = $trackedFiles | Select-String -Pattern $pattern
    if ($matches) {
        $foundSensitive += $matches
    }
}
if ($foundSensitive.Count -gt 0) {
    $Issues += "Sensitive files detected in Git: $($foundSensitive.Count) files"
    Write-Host "ERROR: Sensitive files detected in Git:" -ForegroundColor Red
    $foundSensitive | ForEach-Object { Write-Host "  - $_" -ForegroundColor Red }
} else {
    $Pass += "No sensitive files in Git"
    Write-Host "OK: No sensitive files in Git" -ForegroundColor Green
}

# 3. Check hardcoded secrets
Write-Host "`n[3] CHECKING HARDCODED SECRETS..." -ForegroundColor Yellow
$hardcodePatterns = @("JWT_SECRET_KEY\s*=\s*['""]?[A-Za-z0-9]{10,}['""]?", "FERNET_KEY\s*=\s*['""]?[A-Za-z0-9\-_]{40,}['""]?", "password\s*=\s*['""][^'""]+['""]", "api_key\s*=\s*['""][^'""]+['""]")
$foundHardcode = @()
foreach ($file in Get-ChildItem -Path src,web,scripts -Recurse -Filter "*.py" -ErrorAction SilentlyContinue) {
    $content = Get-Content $file.FullName -Raw -ErrorAction SilentlyContinue
    foreach ($pattern in $hardcodePatterns) {
        if ($content -match $pattern) {
            $foundHardcode += "$($file.FullName): $($matches[0])"
        }
    }
}
if ($foundHardcode.Count -gt 0) {
    $Issues += "Hardcoded secrets detected in code"
    Write-Host "ERROR: Hardcoded secrets detected:" -ForegroundColor Red
    $foundHardcode | ForEach-Object { Write-Host "  - $_" -ForegroundColor Red }
} else {
    $Pass += "No hardcoded secrets"
    Write-Host "OK: No hardcoded secrets" -ForegroundColor Green
}

# 4. Check dangerous functions
Write-Host "`n[4] CHECKING DANGEROUS FUNCTIONS..." -ForegroundColor Yellow
$dangerousFunctions = @("eval\(", "exec\(", "__import__\(", "subprocess\.call", "subprocess\.Popen", "os\.system", "os\.popen")
$foundDangerous = @()
foreach ($file in Get-ChildItem -Path src,web,scripts -Recurse -Filter "*.py" -ErrorAction SilentlyContinue) {
    $content = Get-Content $file.FullName -Raw -ErrorAction SilentlyContinue
    foreach ($func in $dangerousFunctions) {
        if ($content -match $func) {
            $foundDangerous += "$($file.FullName): $func"
        }
    }
}
if ($foundDangerous.Count -gt 0) {
    $Warnings += "Dangerous functions detected (review required)"
    Write-Host "WARN: Dangerous functions detected (review required):" -ForegroundColor Yellow
    $foundDangerous | ForEach-Object { Write-Host "  - $_" -ForegroundColor Yellow }
} else {
    $Pass += "No dangerous functions"
    Write-Host "OK: No dangerous functions" -ForegroundColor Green
}

# 5. Check SQL injection patterns
Write-Host "`n[5] CHECKING SQL INJECTION PATTERNS..." -ForegroundColor Yellow
$sqlPatterns = @("execute\s*\(\s*['""]SELECT", "execute\s*\(\s*['""]INSERT", "execute\s*\(\s*['""]UPDATE", "execute\s*\(\s*['""]DELETE", "text\s*\(\s*['""]")
$foundSQL = @()
foreach ($file in Get-ChildItem -Path src,web -Recurse -Filter "*.py" -ErrorAction SilentlyContinue) {
    $content = Get-Content $file.FullName -Raw -ErrorAction SilentlyContinue
    foreach ($pattern in $sqlPatterns) {
        if ($content -match $pattern) {
            $foundSQL += "$($file.FullName): $pattern"
        }
    }
}
if ($foundSQL.Count -gt 0) {
    $Warnings += "Raw SQL detected (consider using ORM)"
    Write-Host "WARN: Raw SQL detected (consider using ORM):" -ForegroundColor Yellow
    $foundSQL | ForEach-Object { Write-Host "  - $_" -ForegroundColor Yellow }
} else {
    $Pass += "No raw SQL detected"
    Write-Host "OK: No raw SQL detected" -ForegroundColor Green
}

# 6. Check dependencies
Write-Host "`n[6] CHECKING DEPENDENCIES..." -ForegroundColor Yellow
if (Test-Path "requirements.txt") {
    $req = Get-Content "requirements.txt"
    $criticalPackages = @("fastapi", "uvicorn", "sqlalchemy", "cryptography", "PyJWT", "bcrypt", "passlib")
    $foundCritical = @()
    foreach ($line in $req) {
        if ($line -match "^(?<package>[a-zA-Z0-9\-_]+)==(?<version>[\d\.]+)") {
            $pkg = $matches['package']
            $ver = $matches['version']
            if ($pkg -in $criticalPackages) {
                $foundCritical += "$pkg==$ver"
            }
        }
    }
    if ($foundCritical.Count -gt 0) {
        $Warnings += "Critical dependencies found (check for updates)"
        Write-Host "WARN: Critical dependencies found (check for updates):" -ForegroundColor Yellow
        $foundCritical | ForEach-Object { Write-Host "  - $_" -ForegroundColor Yellow }
    } else {
        $Pass += "Dependencies checked"
        Write-Host "OK: Dependencies checked" -ForegroundColor Green
    }
} else {
    $Warnings += "requirements.txt not found"
    Write-Host "WARN: requirements.txt not found" -ForegroundColor Yellow
}

# 7. Check CORS configuration
Write-Host "`n[7] CHECKING CORS..." -ForegroundColor Yellow
$corsFiles = Get-ChildItem -Path web,src -Recurse -Filter "*.py" -ErrorAction SilentlyContinue | Select-String -Pattern "CORSMiddleware|allow_origins"
if ($corsFiles) {
    $Pass += "CORS configuration found"
    Write-Host "OK: CORS configuration found" -ForegroundColor Green
    $corsContent = $corsFiles | ForEach-Object { $_.Line }
    if ($corsContent -match "allow_origins\s*=\s*\[\s*['""]\*['""]\s*\]") {
        $Issues += "CORS allows all origins (allow_origins=['*'])"
        Write-Host "ERROR: CORS allows all origins (allow_origins=['*'])" -ForegroundColor Red
    } else {
        $Pass += "CORS does not allow '*'"
        Write-Host "OK: CORS does not allow '*'" -ForegroundColor Green
    }
} else {
    $Warnings += "CORS configuration not found"
    Write-Host "WARN: CORS configuration not found" -ForegroundColor Yellow
}

# 8. Check logging
Write-Host "`n[8] CHECKING LOGGING..." -ForegroundColor Yellow
$loggingFiles = Get-ChildItem -Path src,web -Recurse -Filter "*.py" -ErrorAction SilentlyContinue | Select-String -Pattern "logging\.basicConfig|logger\s*="
if ($loggingFiles) {
    $Pass += "Logging configuration found"
    Write-Host "OK: Logging configuration found" -ForegroundColor Green
} else {
    $Warnings += "Logging configuration incomplete"
    Write-Host "WARN: Logging configuration incomplete" -ForegroundColor Yellow
}

# 9. Check database
Write-Host "`n[9] CHECKING DATABASE..." -ForegroundColor Yellow
if (Test-Path "app.db") {
    $dbSize = (Get-Item "app.db").Length / 1MB
    Write-Host "OK: app.db exists, size: $([math]::Round($dbSize, 2)) MB" -ForegroundColor Green
    $Pass += "Database exists"
} else {
    $Warnings += "app.db not found (may not be created yet)"
    Write-Host "WARN: app.db not found (may not be created yet)" -ForegroundColor Yellow
}

# Summary
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "AUDIT SUMMARY" -ForegroundColor Cyan
Write-Host "========================================"
Write-Host "PASS: $($Pass.Count)" -ForegroundColor Green
Write-Host "WARNINGS: $($Warnings.Count)" -ForegroundColor Yellow
Write-Host "ISSUES: $($Issues.Count)" -ForegroundColor Red

if ($Issues.Count -gt 0) {
    Write-Host "`nCRITICAL ISSUES TO FIX:" -ForegroundColor Red
    $Issues | ForEach-Object { Write-Host "  - $_" -ForegroundColor Red }
} else {
    Write-Host "`nNO CRITICAL ISSUES FOUND" -ForegroundColor Green
}

if ($Warnings.Count -gt 0) {
    Write-Host "`nWARNINGS TO REVIEW:" -ForegroundColor Yellow
    $Warnings | ForEach-Object { Write-Host "  - $_" -ForegroundColor Yellow }
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "AUDIT COMPLETE" -ForegroundColor Cyan
Write-Host "========================================"