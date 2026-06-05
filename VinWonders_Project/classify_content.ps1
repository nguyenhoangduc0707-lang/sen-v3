# ============================================
# PHÂN LOẠI NỘI DUNG TỰ ĐỘNG
# ============================================

param(
    [string]$sourceFolder = "E:\DYT_01\VinWonders_Project\01_Content",
    [string]$destRoot = "E:\DYT_01\VinWonders_Project"
)

Write-Host "`n==========================================" -ForegroundColor Cyan
Write-Host "🏷️ PHÂN LOẠI NỘI DUNG VINWONDERS" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan

# Định nghĩa từ khóa phân loại
$keywords = @{
    "Water_Park" = @("nước", "bơi", "trượt", "wave", "pool", "water", "bể bơi", "công viên nước")
    "Amusement_Park" = @("tàu lượn", "roller", "coaster", "vòng quay", "ferris", "cảm giác mạnh")
    "Aquarium" = @("cá", "thủy cung", "penguin", "hải cẩu", "aquarium", "đại dương")
    "Shows_Entertainment" = @("show", "biểu diễn", "nhạc", "múa", "firework", "pháo hoa")
    "Food_Beverage" = @("ăn", "uống", "nhà hàng", "quán", "food", "drink", "buffet")
    "Shopping" = @("mua sắm", "shop", "quà lưu niệm", "souvenir")
}

# Hàm phân loại file
function Classify-File {
    param([string]$filePath)
    
    $fileName = (Get-Item $filePath).BaseName.ToLower()
    $classified = @()
    
    foreach ($category in $keywords.Keys) {
        foreach ($keyword in $keywords[$category]) {
            if ($fileName -match $keyword) {
                $classified += $category
                break
            }
        }
    }
    
    if ($classified.Count -eq 0) {
        return "Others"
    }
    return $classified[0]
}

# Xử lý video
$videoFiles = Get-ChildItem -Path "$sourceFolder\Vin_video\*" -Include *.mp4,*.mov,*.avi -ErrorAction SilentlyContinue
Write-Host "`n🎬 ĐANG PHÂN LOẠI VIDEO..." -ForegroundColor Yellow

foreach ($video in $videoFiles) {
    $category = Classify-File -filePath $video.FullName
    $destPath = "$destRoot\02_Themes\$category"
    
    if (-not (Test-Path $destPath)) {
        New-Item -ItemType Directory -Path $destPath -Force | Out-Null
    }
    
    # Copy (không move để giữ bản gốc)
    Copy-Item -Path $video.FullName -Destination "$destPath\" -Force
    Write-Host "   📹 Đã phân loại: $($video.Name) -> $category" -ForegroundColor Gray
}

# Xử lý hình ảnh
$imageFiles = Get-ChildItem -Path "$sourceFolder\Vin_hinh_anh\*" -Include *.jpg,*.jpeg,*.png,*.gif -ErrorAction SilentlyContinue
Write-Host "`n🖼️ ĐANG PHÂN LOẠI HÌNH ẢNH..." -ForegroundColor Yellow

foreach ($image in $imageFiles) {
    $category = Classify-File -filePath $image.FullName
    $destPath = "$destRoot\02_Themes\$category"
    
    if (-not (Test-Path $destPath)) {
        New-Item -ItemType Directory -Path $destPath -Force | Out-Null
    }
    
    Copy-Item -Path $image.FullName -Destination "$destPath\" -Force
    Write-Host "   🖼️ Đã phân loại: $($image.Name) -> $category" -ForegroundColor Gray
}

Write-Host "`n✅ PHÂN LOẠI HOÀN TẤT!" -ForegroundColor Green

# Hiển thị thống kê
Write-Host "`n📊 THỐNG KÊ:" -ForegroundColor Cyan
foreach ($category in $keywords.Keys) {
    $destPath = "$destRoot\02_Themes\$category"
    if (Test-Path $destPath) {
        $fileCount = (Get-ChildItem -Path $destPath -File).Count
        Write-Host "   $category : $fileCount files" -ForegroundColor White
    }
}
