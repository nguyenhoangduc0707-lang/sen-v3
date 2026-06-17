# start-api.ps1
Write-Host "Starting SEN V3 API Server..." -ForegroundColor Cyan
$env:FERNET_KEY = "WphX9F3TeO5B4N4EcBhxd1ehvI9NhgHPz1mH2cPi9QI="
$env:JWT_SECRET_KEY = "xK9mP2nQ5rS8tU1wX4zA7cD0fG3jJ6lM9oR2sU5vY8"
uvicorn web.main:app --reload --host 0.0.0.0 --port 8001
