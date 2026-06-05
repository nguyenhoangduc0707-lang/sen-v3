# Backup toàn bộ dự án VinWonders
$backupFolder = "E:\DYT_01_BACKUP\VinWonders_$(Get-Date -Format 'yyyyMMdd')"
Copy-Item -Path "E:\DYT_01\VinWonders_Project" -Destination $backupFolder -Recurse -Force
Write-Host "✅ Đã backup tại: $backupFolder"
