# ============================================
# SẮP XẾP NỘI DUNG - CHẠY KHI THÊM FILE MỚI
# ============================================

param(
    [string]$source = "$global:VIN_ROOT\01_Content"
)

Write-Host "`n==========================================" -ForegroundColor Cyan
Write-Host "📁 SẮP XẾP NỘI DUNG" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan

# Định nghĩa từ khóa theo chủ đề
$categories = @{
    "Water_Park" = @("nước", "bơi", "trượt", "wave", "pool", "water", "bể bơi")
    "Amusement_Park" = @("tàu lượn", "roller", "coaster", "vòng quay", "ferris")
    "Aquarium" = @("cá", "thủy cung", "penguin", "hải cẩu", "aquarium")
    "Shows_Entertainment" = @("show", "biểu diễn", "nhạc", "múa", "firework")
    "Food_Beverage" = @("ăn", "uống", "nhà hàng", "food", "drink", "buffet")
}

$stats = @{}
$totalFiles = 0

# Xử lý video
$videoFiles = Get-ChildItem -Path "$source\Vin_video\Raw" -Include *.mp4,*.mov,*.avi -ErrorAction SilentlyContinue
Write-Host "`n🎬 XỬ LÝ VIDEO ($($videoFiles.Count) file)..." -ForegroundColor Yellow

foreach ($video in $videoFiles) {
    $classified = $false
    foreach ($cat in $categories.Keys) {
        foreach ($keyword in $categories[$cat]) {
            if ($video.BaseName.ToLower() -match $keyword) {
                $dest = "$global:VIN_ROOT\02_Themes\$cat"
                New-Item -ItemType Directory -Path $dest -Force | Out-Null
                Copy-Item -Path $video.FullName -Destination "$dest\" -Force
                $stats[$cat] = $stats[$cat] + 1
                $classified = $true
                Write-Host "   📹 $($video.Name) -> $cat" -ForegroundColor Gray
                break
            }
        }
        if ($classified) { break }
    }
    if (-not $classified) {
        Write-Host "   📹 $($video.Name) -> Others" -ForegroundColor Gray
        $stats["Others"] = $stats["Others"] + 1
    }
    $totalFiles++
}

# Xử lý hình ảnh
$imageFiles = Get-ChildItem -Path "$source\Vin_hinh_anh\Raw" -Include *.jpg,*.jpeg,*.png,*.gif -ErrorAction SilentlyContinue
Write-Host "`n🖼️ XỬ LÝ HÌNH ẢNH ($($imageFiles.Count) file)..." -ForegroundColor Yellow

foreach ($image in $imageFiles) {
    $classified = $false
    foreach ($cat in $categories.Keys) {
        foreach ($keyword in $categories[$cat]) {
            if ($image.BaseName.ToLower() -match $keyword) {
                $dest = "$global:VIN_ROOT\02_Themes\$cat"
                New-Item -ItemType Directory -Path $dest -Force | Out-Null
                Copy-Item -Path $image.FullName -Destination "$dest\" -Force
                $stats[$cat] = $stats[$cat] + 1
                $classified = $true
                Write-Host "   🖼️ $($image.Name) -> $cat" -ForegroundColor Gray
                break
            }
        }
        if ($classified) { break }
    }
    if (-not $classified) {
        Write-Host "   🖼️ $($image.Name) -> Others" -ForegroundColor Gray
        $stats["Others"] = $stats["Others"] + 1
    }
    $totalFiles++
}

Write-Host "`n📊 THỐNG KÊ:" -ForegroundColor Cyan
foreach ($cat in $stats.Keys | Sort-Object) {
    Write-Host "   $cat : $($stats[$cat]) files" -ForegroundColor White
}
Write-Host "   TỔNG: $totalFiles files" -ForegroundColor Green

# Lưu báo cáo
$reportPath = "$global:VIN_ROOT\05_Management\Reports\organize_report_$(Get-Date -Format 'yyyyMMdd_HHmmss').txt"
$stats.GetEnumerator() | Out-File $reportPath
Write-Host "`n📄 Báo cáo lưu tại: $reportPath" -ForegroundColor Yellow

Write-Host "`n✅ SẮP XẾP HOÀN TẤT!" -ForegroundColor Green
