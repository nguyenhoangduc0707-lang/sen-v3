# check-project.ps1
$ErrorActionPreference = "Continue"
Set-Location E:\DYT_01

Write-Host ""
Write-Host "===== START PROJECT CHECK =====" -ForegroundColor Cyan

if (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host "Activating venv..." -ForegroundColor Yellow
    & "venv\Scripts\Activate.ps1"
}

if (Test-Path ".env") {
    Write-Host "[OK] .env exists" -ForegroundColor Green
} else {
    Write-Host "[WARN] .env missing" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Running flake8..." -ForegroundColor Yellow
flake8 . --count --statistics
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] flake8 passed" -ForegroundColor Green
} else {
    Write-Host "[FAIL] flake8 found issues" -ForegroundColor Red
}

Write-Host ""
Write-Host "Running mypy..." -ForegroundColor Yellow
mypy src tests --ignore-missing-imports
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] mypy passed" -ForegroundColor Green
} else {
    Write-Host "[FAIL] mypy found issues" -ForegroundColor Red
}

Write-Host ""
Write-Host "Running pytest..." -ForegroundColor Yellow
$testFiles = Get-ChildItem -Path tests -Filter "test_*.py" -Recurse -ErrorAction SilentlyContinue
if ($testFiles.Count -eq 0) {
    Write-Host "[SKIP] No test files found" -ForegroundColor Yellow
} else {
    pytest tests -v --tb=short --cov=src --cov-report=term
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] pytest passed" -ForegroundColor Green
    } else {
        Write-Host "[FAIL] pytest failed" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Running alembic..." -ForegroundColor Yellow
alembic current
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] alembic ok" -ForegroundColor Green
} else {
    Write-Host "[FAIL] alembic issue" -ForegroundColor Red
}

Write-Host ""
Write-Host "===== PROJECT CHECK COMPLETED =====" -ForegroundColor Cyan
