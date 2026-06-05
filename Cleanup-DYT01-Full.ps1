# Cleanup-DYT01-Full.ps1
Write-Host "🧹 DỌN DẸP DYT_01 - FULL" -ForegroundColor Cyan

# 1. Dừng processes
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force

# 2. Xóa cache
Get-ChildItem -Path . -Directory -Recurse -Filter "__pycache__" -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force
Get-ChildItem -Path . -File -Recurse -Filter "*.pyc" -ErrorAction SilentlyContinue | Remove-Item -Force

# 3. Xóa test artifacts
Remove-Item -Path ".pytest_cache" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "htmlcov" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path ".coverage" -Force -ErrorAction SilentlyContinue

# 4. Xóa node_modules
Remove-Item -Path "node_modules" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "package-lock.json" -Force -ErrorAction SilentlyContinue

# 5. Dọn log cũ
Get-ChildItem -Path "logs" -Filter "*.log" -ErrorAction SilentlyContinue | Where-Object { 
    $_.LastWriteTime -lt (Get-Date).AddDays(-7)
} | Remove-Item -Force

# 6. Xóa file tạm
Get-ChildItem -Path . -File -Recurse -Include "*.tmp","*.bak","*.log","*.py~" -ErrorAction SilentlyContinue | Remove-Item -Force

Write-Host "✅ Dọn dẹp hoàn tất!" -ForegroundColor Green
