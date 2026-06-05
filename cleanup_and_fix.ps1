# cleanup_and_fix.ps1
Write-Host "DỌN DẸP DỰ ÁN DYT_01" -ForegroundColor Green
Set-Location E:\DYT_01

# Xóa cache Python
Get-ChildItem -Path . -Include "__pycache__" -Recurse -Force | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Get-ChildItem -Path . -Filter "*.pyc" -Recurse -Force | Remove-Item -Force -ErrorAction SilentlyContinue

# Tạo thư mục cần thiết
New-Item -ItemType Directory -Force -Path "media/images" | Out-Null
New-Item -ItemType Directory -Force -Path "logs/archive" | Out-Null

Write-Host "✅ Dọn dẹp xong!" -ForegroundColor Green