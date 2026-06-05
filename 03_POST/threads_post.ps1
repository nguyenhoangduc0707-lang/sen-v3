# ============================================
# ĐĂNG BÀI LÊN THREADS - WONDER SUMMER 2026
# ============================================

param(
    [string]$content,
    [string]$imagePath,
    [switch]$auto
)

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "📝 ĐĂNG BÀI LÊN THREADS" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan

# Định nghĩa hashtag bắt buộc
$requiredHashtags = @("#WonderSummer2026", "#VinWonders", "#GreenCreator", "#HeLaPhaiDiVinWonders")
$hashtagString = $requiredHashtags -join " "

# Các mẫu nội dung
$templates = @(
    "Mình vừa có trải nghiệm tuyệt vời tại VinWonders! Cảm giác như đang ở thiên đường giải trí vậy. Ai đã từng đến đây rồi? $hashtagString",
    "Phải công nhận VinWonders mùa hè này đầu tư quá trời! Từ tàu lượn đến công viên nước, không có điểm dừng. Các bác đã thử chưa? $hashtagString",
    "Hè tới rồi, hè là phải đi VinWonders thôi! Ai đang có kế hoạch đi VinWonders mùa hè này? $hashtagString",
    "Một ngày ở VinWonders thực sự đáng nhớ! Từ sáng đến tối không lúc nào ngừng cười. Các bác đã thử chưa? $hashtagString",
    "Vừa trải nghiệm tàu lượn siêu tốc ở VinWonders xong, tim vẫn còn đập thình thịch! Ai đã thử chưa, cảm giác thế nào? $hashtagString"
)

# Tạo nội dung nếu chưa có
if (-not $content) {
    $content = $templates | Get-Random
}

Write-Host "`n📝 NỘI DUNG BÀI ĐĂNG:" -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor Gray
Write-Host $content -ForegroundColor White
Write-Host "----------------------------------------" -ForegroundColor Gray

Write-Host "`n🔖 HASHTAG:" -ForegroundColor Yellow
Write-Host $hashtagString -ForegroundColor Cyan

if ($imagePath -and (Test-Path $imagePath)) {
    Write-Host "`n🖼️ HÌNH ẢNH: $imagePath" -ForegroundColor Green
}

Write-Host "`n==========================================" -ForegroundColor Cyan

if ($auto) {
    Write-Host "🤖 CHẾ ĐỘ TỰ ĐỘNG:" -ForegroundColor Green
    # Copy nội dung vào clipboard
    $content | Set-Clipboard
    Write-Host "   ✅ Nội dung đã copy vào clipboard (Ctrl+V)" -ForegroundColor Green
    Write-Host "   🌐 Mở Threads tại: https://threads.net" -ForegroundColor Cyan
    Start-Process "https://threads.net"
} else {
    Write-Host "👉 HƯỚNG DẪN:" -ForegroundColor Yellow
    Write-Host "   1. Copy nội dung bên trên" -ForegroundColor White
    Write-Host "   2. Truy cập https://threads.net" -ForegroundColor White
    Write-Host "   3. Dán nội dung và đăng bài" -ForegroundColor White
}

Write-Host "`n✅ HOÀN TẤT!" -ForegroundColor Green
