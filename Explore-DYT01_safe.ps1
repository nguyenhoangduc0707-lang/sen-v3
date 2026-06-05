Set-Location C:\DYT_01
Write-Host "=== BAT DAU KHAM PHA ===" -ForegroundColor Cyan
tree /F | Select-Object -First 100
Write-Host "--- File Python ---"
Get-ChildItem -Recurse -File -Filter *.py | Where-Object { $_.FullName -notmatch "venv|__pycache__" } | Select-Object -First 30 FullName
Write-Host "--- Cac file entry point (if __name__...) ---"
Select-String -Path "*.py" -Pattern 'if __name__\s*==\s*"__main__"' -List | Select-Object Filename
Write-Host "--- Noi dung .env ---"
Get-Content .env -ErrorAction SilentlyContinue
Write-Host "=== KET THUC ==="
