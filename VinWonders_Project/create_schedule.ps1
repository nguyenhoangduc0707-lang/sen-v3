# ============================================
# LỊCH ĐĂNG BÀI VINWONDERS - WONDER SUMMER 2026
# ============================================

$schedule = @()

# Các loại bài đăng theo ngày trong tuần
$weeklySchedule = @{
    "Monday" = @{type = "Opinion"; hashtag = "#GocNhinCaNhan"}
    "Tuesday" = @{type = "Debate"; hashtag = "#TranhLuan"}
    "Wednesday" = @{type = "FOMO"; hashtag = "#MuonDiNgay"}
    "Thursday" = @{type = "Storytelling"; hashtag = "#ChuyenKe"}
    "Friday" = @{type = "Thrilling"; hashtag = "#CamGiacManh"}
    "Saturday" = @{type = "FOMO"; hashtag = "#CuoiTuanVuiVe"}
    "Sunday" = @{type = "Opinion"; hashtag = "#ChiaSeThat"}
}

# Tạo lịch từ 13/04 đến 31/08
$startDate = Get-Date "2026-04-13"
$endDate = Get-Date "2026-08-31"
$currentDate = $startDate

while ($currentDate -le $endDate) {
    $dayOfWeek = $currentDate.DayOfWeek.ToString()
    $scheduleItem = $weeklySchedule[$dayOfWeek]
    
    if ($scheduleItem) {
        $schedule += [PSCustomObject]@{
            Date = $currentDate.ToString("dd/MM/yyyy")
            DayOfWeek = $dayOfWeek
            Type = $scheduleItem.type
            Hashtag = $scheduleItem.hashtag
            Status = "Pending"
            Link = ""
            Views = 0
            Comments = 0
        }
    }
    $currentDate = $currentDate.AddDays(1)
}

# Xuất ra CSV
$schedulePath = "E:\DYT_01\VinWonders_Project\05_Management\Schedules\Wonder_Summer_2026_Schedule.csv"
$schedule | Export-Csv -Path $schedulePath -NoTypeInformation -Encoding UTF8 -Force

Write-Host "✅ Đã tạo lịch đăng bài từ 13/04 - 31/08/2026" -ForegroundColor Green
Write-Host "📁 Lưu tại: $schedulePath" -ForegroundColor Cyan
Write-Host "📊 Tổng số bài: $($schedule.Count) bài" -ForegroundColor Yellow
