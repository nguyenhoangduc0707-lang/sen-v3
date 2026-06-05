# ============================================
# TỰ ĐỘNG COPY ẢNH VÀO BÀI ĐĂNG
# ============================================

$campaignRoot = "E:\DYT_01\ACFC_CAMPAIGN"

$mappings = @(
    @{brand = "CalvinKlein"; postFolder = "01_CalvinKlein_Double5"}
    @{brand = "TommyHilfiger"; postFolder = "02_TommyHilfiger_Double5"}
    @{brand = "Mango"; postFolder = "03_Mango_Double5"}
    @{brand = "Guess"; postFolder = "04_Guess_Double5"}
    @{brand = "CottonOn"; postFolder = "05_CottonOn_SpecialOffer"}
)

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "🖼️ COPY ẢNH VÀO BÀI ĐĂNG" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan

foreach ($map in $mappings) {
    $source = Join-Path $campaignRoot "03_Hinh_anh_san_sang\$($map.brand)"
    $dest = Join-Path $campaignRoot "01_Bai_dang_soan_san\$($map.postFolder)\anh_video"
    
    if (Test-Path $source) {
        $files = Get-ChildItem -Path $source -File
        if ($files.Count -gt 0) {
            Copy-Item -Path "$source\*" -Destination $dest -Force
            Write-Host "✅ Đã copy $($files.Count) ảnh cho $($map.brand)" -ForegroundColor Green
        } else {
            Write-Host "⚠️ Chưa có ảnh trong thư mục $($map.brand)" -ForegroundColor Yellow
        }
    } else {
        Write-Host "❌ Không tìm thấy thư mục: $source" -ForegroundColor Red
        Write-Host "   → Hãy tạo thư mục và copy ảnh vào đó trước" -ForegroundColor Yellow
    }
}

Write-Host "`n✅ HOÀN TẤT!" -ForegroundColor Green
