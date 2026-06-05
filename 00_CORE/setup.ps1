# ============================================
# SETUP MÔI TRƯỜNG - CHẠY 1 LẦN ĐẦU
# ============================================

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "🔧 SETUP DỰ ÁN VINWONDERS" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan

# Tạo thư mục cần thiết
Write-Host "`n📁 TẠO THƯ MỤC..." -ForegroundColor Yellow

$folders = @(
    "E:\DYT_01\VinWonders_Project\01_Content\Vin_video\Raw",
    "E:\DYT_01\VinWonders_Project\01_Content\Vin_video\Edited",
    "E:\DYT_01\VinWonders_Project\01_Content\Vin_hinh_anh\Raw",
    "E:\DYT_01\VinWonders_Project\01_Content\Vin_hinh_anh\Edited",
    "E:\DYT_01\VinWonders_Project\02_Themes",
    "E:\DYT_01\VinWonders_Project\03_Locations",
    "E:\DYT_01\VinWonders_Project\04_Campaigns\Wonder_Summer_2026",
    "E:\DYT_01\VinWonders_Project\05_Management\Schedules",
    "E:\DYT_01\VinWonders_Project\05_Management\Analytics",
    "E:\DYT_01\VinWonders_Project\05_Management\Affiliate_Links",
    "E:\DYT_01\VinWonders_Project\06_Templates"
)

foreach ($folder in $folders) {
    New-Item -ItemType Directory -Path $folder -Force | Out-Null
}
Write-Host "✅ Đã tạo $($folders.Count) thư mục" -ForegroundColor Green

Write-Host "`n✅ SETUP HOÀN TẤT!" -ForegroundColor Green
Write-Host "👉 TIẾP THEO: Điền thông tin vào 00_CORE/personal_config.ps1" -ForegroundColor Yellow
