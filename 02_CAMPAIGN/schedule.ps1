# ============================================
# TẠO LỊCH ĐĂNG BÀI - CHẠY 1 LẦN/THÁNG
# ============================================

param(
    [int]$month = (Get-Date).Month,
    [int]$year = (Get-Date).Year
)

# Định nghĩa đường dẫn gốc
$global:ROOT = "E:\DYT_01"
$global:VIN_ROOT = "$global:ROOT\VinWonders_Project"

Write-Host "`n==========================================" -ForegroundColor Cyan
Write-Host "📅 TẠO LỊCH ĐĂNG BÀI - $month/$year" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan

# Các loại bài đăng theo ngày
$postTypes = @(
    @{name="Opinion"; desc="Quan điểm cá nhân"; icon="💭"},
    @{name="Debate"; desc="Tạo tranh luận"; icon="🗣️"},
    @{name="FOMO"; desc="Kích thích trải nghiệm"; icon="🔥"},
    @{name="Storytelling"; desc="Kể chuyện"; icon="📖"},
    @{name="Thrilling"; desc="Cảm giác mạnh"; icon="🎢"}
)

# Đảm bảo thư mục tồn tại
$scheduleDir = "$global:VIN_ROOT\05_Management\Schedules"
if (-not (Test-Path $scheduleDir)) {
    New-Item -ItemType Directory -Path $scheduleDir -Force | Out-Null
    Write-Host "📁 Đã tạo thư mục: $scheduleDir" -ForegroundColor Yellow
}

# Tạo lịch trong tháng
$startDate = Get-Date -Year $year -Month $month -Day 1
$endDate = $startDate.AddMonths(1).AddDays(-1)

$schedule = @()
$postIndex = 0

for ($date = $startDate; $date -le $endDate; $date = $date.AddDays(1)) {
    $postType = $postTypes[$postIndex % $postTypes.Count]
    
    $schedule += [PSCustomObject]@{
        Date = $date.ToString("yyyy-MM-dd")
        DayOfWeek = $date.DayOfWeek.ToString()
        PostType = $postType.name
        Icon = $postType.icon
        Description = $postType.desc
        Hashtags = "#WonderSummer2026 #VinWonders #GreenCreator #HeLaPhaiDiVinWonders"
        Status = "Pending"
        Link = ""
        Views = 0
        Comments = 0
    }
    $postIndex++
}

# Lưu ra CSV
$schedulePath = "$scheduleDir\schedule_$($year)_$($month).csv"
$schedule | Export-Csv -Path $schedulePath -NoTypeInformation -Encoding UTF8 -Force

Write-Host "`n📊 THỐNG KÊ:" -ForegroundColor Cyan
Write-Host "   Tháng: $month/$year" -ForegroundColor White
Write-Host "   Số ngày: $($schedule.Count)" -ForegroundColor White
Write-Host "   Số bài: $($schedule.Count)" -ForegroundColor White
Write-Host "   Thu nhập dự kiến: $($schedule.Count * 150000)đ" -ForegroundColor Green

Write-Host "`n📁 Lịch đã lưu: $schedulePath" -ForegroundColor Yellow
Write-Host "`n✅ TẠO LỊCH HOÀN TẤT!" -ForegroundColor Green
