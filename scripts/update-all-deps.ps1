# update-all-deps.ps1
Write-Host "Updating all dependencies..." -ForegroundColor Cyan

# Backup current requirements
Copy-Item requirements.txt requirements.txt.backup

# Update pip first
python -m pip install --upgrade pip

# Update critical packages
$critical = @(
    "fastapi",
    "playwright", 
    "SQLAlchemy",
    "uvicorn",
    "pydantic",
    "pydantic-settings",
    "alembic",
    "google-generativeai",
    "groq",
    "python-jose",
    "python-multipart",
    "python-dotenv",
    "structlog"
)

foreach ($pkg in $critical) {
    Write-Host "Updating $pkg..." -ForegroundColor Yellow
    pip install --upgrade $pkg
}

# Update all remaining packages
Write-Host "`nUpdating all packages..." -ForegroundColor Cyan
pip list --outdated --format=json | ConvertFrom-Json | ForEach-Object {
    Write-Host "Updating $($_.name)..." -ForegroundColor Yellow
    pip install --upgrade $_.name
}

# Generate new requirements.txt
pip freeze > requirements.txt
Write-Host "`nUpdated requirements.txt generated" -ForegroundColor Green

# Update Playwright browsers
playwright install
Write-Host "Playwright browsers updated" -ForegroundColor Green

Write-Host "`nAll dependencies updated!" -ForegroundColor Green