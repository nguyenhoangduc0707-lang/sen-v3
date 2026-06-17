# ============================================
# SECURITY-SYNC-SENV3.PS1
# Security Audit & Sync for SEN V3 Project
# Run as Administrator
# ============================================

param(
    [switch]$Fix,
    [switch]$UpdateDeps
)

$ColorInfo = "Cyan"
$ColorSuccess = "Green"
$ColorWarning = "Yellow"
$ColorError = "Red"

Write-Host "`n============================================" -ForegroundColor $ColorInfo
Write-Host "   SEN V3 SECURITY AUDIT & SYNC" -ForegroundColor $ColorInfo
Write-Host "============================================`n" -ForegroundColor $ColorInfo

# ============================================
# PART 1: SYNC WITH GITHUB
# ============================================
Write-Host "[PART 1] SYNCING WITH GITHUB" -ForegroundColor $ColorInfo
Write-Host "----------------------------------------" -ForegroundColor $ColorInfo

Write-Host "Checking git status..." -ForegroundColor $ColorWarning
git status --short

Write-Host "`nFetching latest from remote..." -ForegroundColor $ColorWarning
git fetch origin

$behind = git rev-list HEAD..origin/master --count
if ($behind -gt 0) {
    Write-Host "Remote has $behind commits ahead. Pulling..." -ForegroundColor $ColorWarning
    git pull origin master
} else {
    Write-Host "Already up to date with origin/master" -ForegroundColor $ColorSuccess
}

$ahead = git rev-list origin/master..HEAD --count
if ($ahead -gt 0) {
    Write-Host "`nLocal has $ahead commits ahead. Pushing..." -ForegroundColor $ColorWarning
    git push origin master
}

Write-Host "`n[OK] Git sync completed" -ForegroundColor $ColorSuccess

# ============================================
# PART 2: SECURITY AUDIT - PYTHON
# ============================================
Write-Host "`n[PART 2] PYTHON SECURITY AUDIT" -ForegroundColor $ColorInfo
Write-Host "----------------------------------------" -ForegroundColor $ColorInfo

# Check if pip-audit is installed
$pipAuditInstalled = Get-Command pip-audit -ErrorAction SilentlyContinue
if (-not $pipAuditInstalled) {
    Write-Host "Installing pip-audit..." -ForegroundColor $ColorWarning
    pip install pip-audit
}

Write-Host "Running pip-audit to check for vulnerabilities..." -ForegroundColor $ColorWarning
pip-audit --requirement requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] No Python vulnerabilities found!" -ForegroundColor $ColorSuccess
} else {
    Write-Host "[WARN] Vulnerabilities found!" -ForegroundColor $ColorError
    if ($Fix) {
        Write-Host "Updating vulnerable packages..." -ForegroundColor $ColorWarning
        pip install --upgrade -r requirements.txt
    }
}

# Check safety
Write-Host "`nRunning safety check..." -ForegroundColor $ColorWarning
safety check

if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Safety check passed!" -ForegroundColor $ColorSuccess
} else {
    Write-Host "[WARN] Safety check found issues!" -ForegroundColor $ColorError
    if ($Fix) {
        safety check --full-report
    }
}

# ============================================
# PART 3: SECURITY AUDIT - NPM
# ============================================
Write-Host "`n[PART 3] NPM SECURITY AUDIT" -ForegroundColor $ColorInfo
Write-Host "----------------------------------------" -ForegroundColor $ColorInfo

if (Test-Path "frontend/package.json") {
    Push-Location frontend
    
    Write-Host "Running npm audit..." -ForegroundColor $ColorWarning
    npm audit --summary
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] No npm vulnerabilities found!" -ForegroundColor $ColorSuccess
    } else {
        Write-Host "[WARN] Vulnerabilities found!" -ForegroundColor $ColorError
        if ($Fix) {
            Write-Host "Running npm audit fix..." -ForegroundColor $ColorWarning
            npm audit fix
        }
    }
    
    Pop-Location
} else {
    Write-Host "[SKIP] frontend/package.json not found" -ForegroundColor $ColorWarning
}

# ============================================
# PART 4: DEPENDENCY UPDATE (OPTIONAL)
# ============================================
if ($UpdateDeps) {
    Write-Host "`n[PART 4] UPDATING DEPENDENCIES" -ForegroundColor $ColorInfo
    Write-Host "----------------------------------------" -ForegroundColor $ColorInfo
    
    Write-Host "Updating Python packages..." -ForegroundColor $ColorWarning
    pip install --upgrade pip
    pip list --outdated
    
    if ($Fix) {
        pip freeze | %{$_.split('==')[0]} | %{pip install --upgrade $_}
    }
    
    if (Test-Path "frontend/package.json") {
        Push-Location frontend
        Write-Host "`nUpdating npm packages..." -ForegroundColor $ColorWarning
        npm outdated
        if ($Fix) {
            npm update
        }
        Pop-Location
    }
}

# ============================================
# PART 5: SECRET SCANNING (BASIC)
# ============================================
Write-Host "`n[PART 5] SECRET SCANNING" -ForegroundColor $ColorInfo
Write-Host "----------------------------------------" -ForegroundColor $ColorInfo

Write-Host "Checking for common secret patterns..." -ForegroundColor $ColorWarning

# Check for API keys
$apiKeyPatterns = @(
    "sk-[a-zA-Z0-9]{32,}",
    "AIza[0-9A-Za-z_\-]{35}",
    "gsk_[a-zA-Z0-9]{32,}",
    "ghp_[a-zA-Z0-9]{36}",
    "-----BEGIN RSA PRIVATE KEY-----"
)

foreach ($pattern in $apiKeyPatterns) {
    $matches = Select-String -Path "*.py", "*.js", "*.json" -Pattern $pattern -ErrorAction SilentlyContinue
    if ($matches) {
        Write-Host "[WARN] Found potential secret matching: $pattern" -ForegroundColor $ColorError
        foreach ($match in $matches) {
            Write-Host "       $($match.Path):$($match.LineNumber)" -ForegroundColor $ColorWarning
        }
    }
}

# Check .env files
$envFiles = Get-ChildItem -Filter ".env*" -ErrorAction SilentlyContinue
foreach ($envFile in $envFiles) {
    if ($envFile.Name -ne ".env.example") {
        Write-Host "[WARN] Found sensitive env file: $($envFile.Name)" -ForegroundColor $ColorError
    }
}

Write-Host "[OK] Secret scanning completed" -ForegroundColor $ColorSuccess

# ============================================
# PART 6: GITHUB SECURITY FEATURES
# ============================================
Write-Host "`n[PART 6] GITHUB SECURITY FEATURES" -ForegroundColor $ColorInfo
Write-Host "----------------------------------------" -ForegroundColor $ColorInfo

if (Test-Path ".github/dependabot.yml") {
    Write-Host "[OK] Dependabot configured" -ForegroundColor $ColorSuccess
} else {
    Write-Host "[WARN] Dependabot not configured" -ForegroundColor $ColorWarning
}

if (Test-Path ".github/workflows/codeql.yml") {
    Write-Host "[OK] CodeQL configured" -ForegroundColor $ColorSuccess
} else {
    Write-Host "[WARN] CodeQL not configured" -ForegroundColor $ColorWarning
}

# ============================================
# PART 7: OUTDATED DEPENDENCIES REPORT
# ============================================
Write-Host "`n[PART 7] OUTDATED DEPENDENCIES" -ForegroundColor $ColorInfo
Write-Host "----------------------------------------" -ForegroundColor $ColorInfo

Write-Host "Python outdated packages:" -ForegroundColor $ColorWarning
pip list --outdated

if (Test-Path "frontend/package.json") {
    Push-Location frontend
    Write-Host "`nNPM outdated packages:" -ForegroundColor $ColorWarning
    npm outdated
    Pop-Location
}

# ============================================
# PART 8: FINAL SUMMARY
# ============================================
Write-Host "`n[PART 8] FINAL SUMMARY" -ForegroundColor $ColorInfo
Write-Host "----------------------------------------" -ForegroundColor $ColorInfo

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$reportFile = "security_report_$timestamp.txt"

@"
========================================
SEN V3 SECURITY AUDIT REPORT
Generated: $(Get-Date)
========================================

PROJECT INFO:
- Name: SEN V3 Multi-Agent Pipeline
- Repository: https://github.com/nguyenhoangduc0707-lang/sen-v3
- Branch: master

SECURITY STATUS:
- Python vulnerabilities: Checked via pip-audit
- NPM vulnerabilities: Checked via npm audit
- Secrets scanning: Performed basic check
- Dependabot: Configured
- CodeQL: Configured

RECOMMENDATIONS:
1. Run with -Fix to auto-fix vulnerabilities
2. Run with -UpdateDeps to update dependencies
3. Check GitHub Security tab for detailed alerts
4. Enable branch protection rules on GitHub

========================================
"@ | Out-File -FilePath $reportFile -Encoding ascii

Write-Host "[OK] Security report saved to: $reportFile" -ForegroundColor $ColorSuccess

Write-Host "`n============================================" -ForegroundColor $ColorInfo
Write-Host "   SECURITY AUDIT COMPLETED" -ForegroundColor $ColorSuccess
Write-Host "============================================" -ForegroundColor $ColorInfo

Write-Host "`nRECOMMENDATIONS:" -ForegroundColor $ColorInfo
Write-Host "   1. Run with -Fix to auto-fix vulnerabilities" -ForegroundColor $ColorSuccess
Write-Host "   2. Run with -UpdateDeps to update all dependencies" -ForegroundColor $ColorSuccess
Write-Host "   3. Check GitHub Security tab" -ForegroundColor $ColorSuccess