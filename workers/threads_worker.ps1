# ============================================
# VINWONDERS THREADS WORKER
# HASHTAG BẮT BUỘC: #WonderSummer2026 #VinWonders
# ============================================

$rewardPerPost = 150000
$maxPostsPerMonth = 30
$maxEarning = $rewardPerPost * $maxPostsPerMonth

# HASHTAG BẮT BUỘC (THEO YÊU CẦU CHƯƠNG TRÌNH)
$requiredHashtags = @(
    "#WonderSummer2026",
    "#VinWonders", 
    "#GreenCreator",
    "#HeLaPhaiDiVinWonders"
)

$optionalHashtags = @(
    "#ViralThreads",
    "#WonderSummer",
    "#DuLichHe2026",
    "#Vinpearl",
    "#SummerVibes"
)

# Tổng hợp hashtag
$allHashtags = $requiredHashtags + $optionalHashtags
$hashtagString = " " + ($allHashtags -join " ")

Write-Host "`n==========================================" -ForegroundColor Cyan
Write-Host "🏖️ VINWONDERS THREADS WORKER" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "💰 Thưởng: $($rewardPerPost.ToString('N0'))đ/bài"
Write-Host "📝 Tối đa: $maxPostsPerMonth bài/tháng"
Write-Host "💵 Tối đa: $($maxEarning.ToString('N0'))đ/tháng"
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "🔖 HASHTAG BẮT BUỘC:" -ForegroundColor Yellow
foreach ($ht in $requiredHashtags) {
    Write-Host "   $ht" -ForegroundColor Green
}
Write-Host "==========================================`n" -ForegroundColor Cyan

# Template nội dung (đã bao gồm hashtag)
$templates = @(
    @{
        type = "opinion"
        content = @(
            "Mình vừa ở VinWonders về, phải nói là quá đã luôn các bác ơi! Có ai như mình không, cứ đến hè là lại muốn đi công viên giải trí?$hashtagString",
            "Vừa trải nghiệm tàu lượn siêu tốc ở VinWonders xong, tim vẫn còn đập thình thịch! Ai đã thử chưa, cảm giác thế nào?$hashtagString",
            "Phải công nhận VinWonders mùa hè này đầu tư quá trời! Cảm giác như đang ở resort 5 sao luôn ý. Ai đã từng đến đây chưa?$hashtagString",
            "Một ngày ở VinWonders thực sự đáng nhớ! Từ tàu lượn đến công viên nước, không có điểm dừng. Các bác đã thử chưa?$hashtagString"
        )
    },
    @{
        type = "debate"
        content = @(
            "Tranh luận nè: Đi VinWonders mùa hè nên chơi công viên nước trước hay công viên giải trí trước? Vote đi các bác!$hashtagString",
            "Mùa hè này: VinWonders Đà Nẵng hay VinWonders Phú Quốc? Bên nào đáng trải nghiệm hơn?$hashtagString",
            "Sáng đi VinWonders hay chiều đi VinWonders? Mọi người chọn giờ nào để chơi cho đã?$hashtagString",
            "Đi VinWonders một mình hay đi với hội bạn? Cảm giác nào tuyệt hơn các bác nhỉ?$hashtagString"
        )
    },
    @{
        type = "fomo"
        content = @(
            "Hè tới rồi, hè là phải đi VinWonders thôi! Nghe nói mùa hè này có event siêu hot, không đi thì phí quá!$hashtagString",
            "Cả tuần nay cứ thấy bạn bè check-in VinWonders, chắc phải xách balo lên và đi thôi! Ai đi cùng không?$hashtagString",
            "Tin nóng: Wonder Summer 2026 đang diễn ra! Ai chưa đi thì nhanh chân kẻo lỡ hè nha!$hashtagString",
            "Nhìn ảnh bạn bè đi VinWonders mà thèm quá! Hè này nhất định phải đi mới được!$hashtagString"
        )
    },
    @{
        type = "storytelling"
        content = @(
            "Chuyện là hôm qua mình đi VinWonders, lúc đầu tính chơi có 2 tiếng thôi mà cuối cả ngày mới về. Đã quá các bác ạ!$hashtagString",
            "Kỷ niệm đáng nhớ nhất ở VinWonders là lúc... kể mà không hết chuyện. Ai muốn nghe không?$hashtagString",
            "Mình đã khám phá hết VinWonders mất 2 ngày liền. Tip nhỏ: nên đi từ sáng sớm để chơi được nhiều trò nha!$hashtagString"
        )
    }
)

# Hàm kiểm tra hashtag
function Test-Hashtags {
    param([string]$content)
    
    $missingHashtags = @()
    foreach ($ht in $requiredHashtags) {
        if ($content -notlike "*$ht*") {
            $missingHashtags += $ht
        }
    }
    
    if ($missingHashtags.Count -gt 0) {
        return @{
            valid = $false
            missing = $missingHashtags
        }
    }
    
    return @{valid = $true}
}

# Hàm tạo nội dung ngẫu nhiên
function Generate-Post {
    $randomType = Get-Random -Minimum 0 -Maximum $templates.Count
    $template = $templates[$randomType]
    $randomContent = Get-Random -Minimum 0 -Maximum $template.content.Count
    return $template.content[$randomContent]
}

# Hàm tạo lịch đăng bài
function Create-ContentCalendar {
    param([int]$days = 30)
    
    $calendar = @()
    $postTypes = @("opinion", "debate", "fomo", "storytelling")
    
    for ($i = 0; $i -lt $days; $i++) {
        $postDate = (Get-Date).AddDays($i)
        $content = Generate-Post
        
        $calendar += [PSCustomObject]@{
            Day = $i + 1
            Date = $postDate.ToString("dd/MM/yyyy")
            Hashtags = ($requiredHashtags -join " ")
            Content = $content
            CharCount = $content.Length
        }
    }
    
    return $calendar
}

# Hiển thị menu
function Show-Menu {
    Write-Host "`n==========================================" -ForegroundColor Cyan
    Write-Host "📋 CHỌN CHỨC NĂNG:" -ForegroundColor Yellow
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host "1. Tạo nội dung bài đăng (có hashtag)"
    Write-Host "2. Tạo lịch đăng bài 30 ngày"
    Write-Host "3. Kiểm tra hashtag bài viết"
    Write-Host "4. Xem checklist & hashtag bắt buộc"
    Write-Host "5. Xuất lịch đăng bài ra file CSV"
    Write-Host "0. Thoát"
    Write-Host "==========================================" -ForegroundColor Cyan
}

# Checklist yêu cầu
$checklist = @(
    "✅ Tài khoản Threads phải công khai",
    "✅ Trung bình 500+ views/5 bài gần nhất",
    "✅ Ảnh/video tự chụp tại VinWonders",
    "✅ Có thông điệp 'Hè là phải đi VinWonders'",
    "✅ 🔖 BẮT BUỘC: #WonderSummer2026",
    "✅ 🔖 BẮT BUỘC: #VinWonders",
    "✅ 🔖 BẮT BUỘC: #GreenCreator",
    "✅ 🔖 BẮT BUỘC: #HeLaPhaiDiVinWonders",
    "✅ Nội dung tự nhiên, không seeding",
    "✅ Gửi bài trong vòng 5 ngày sau khi đăng",
    "✅ Bài đạt tối thiểu 1.000 views/5 ngày",
    "✅ Bài dạng debate cần 10+ comments"
)

# Main loop
do {
    Show-Menu
    $choice = Read-Host "`nNhập lựa chọn"
    
    switch ($choice) {
        "1" {
            Write-Host "`n📝 NỘI DUNG BÀI ĐĂNG MẪU (CÓ HASHTAG):" -ForegroundColor Green
            Write-Host "==========================================" -ForegroundColor Green
            
            for ($i = 1; $i -le 3; $i++) {
                $post = Generate-Post
                Write-Host "`n[$i] $post" -ForegroundColor White
                
                # Kiểm tra hashtag
                $check = Test-Hashtags -content $post
                if ($check.valid) {
                    Write-Host "   ✅ Hashtag đầy đủ" -ForegroundColor Green
                } else {
                    Write-Host "   ❌ Thiếu hashtag: $($check.missing -join ', ')" -ForegroundColor Red
                }
            }
            
            Write-Host "`n🔖 Hashtag bắt buộc: $($requiredHashtags -join ', ')" -ForegroundColor Yellow
            Write-Host "👉 Copy nội dung trên và đăng lên Threads!" -ForegroundColor Cyan
        }
        
        "2" {
            Write-Host "`n📅 LỊCH ĐĂNG BÀI 30 NGÀY:" -ForegroundColor Green
            Write-Host "==========================================" -ForegroundColor Green
            $calendar = Create-ContentCalendar -days 30
            $calendar | Format-Table Day, Date, CharCount -AutoSize
            Write-Host "`n💡 Nên đăng 1-2 bài/ngày để đạt tối đa 30 bài/tháng" -ForegroundColor Yellow
            Write-Host "🔖 #WonderSummer2026 #VinWonders #GreenCreator #HeLaPhaiDiVinWonders" -ForegroundColor Cyan
        }
        
        "3" {
            Write-Host "`n🔍 KIỂM TRA HASHTAG BÀI VIẾT:" -ForegroundColor Green
            Write-Host "==========================================" -ForegroundColor Green
            $testContent = Read-Host "Nhập nội dung bài viết cần kiểm tra"
            
            $check = Test-Hashtags -content $testContent
            if ($check.valid) {
                Write-Host "`n✅ Bài viết ĐẦY ĐỦ hashtag bắt buộc!" -ForegroundColor Green
            } else {
                Write-Host "`n❌ Bài viết THIẾU hashtag:" -ForegroundColor Red
                foreach ($ht in $check.missing) {
                    Write-Host "   - $ht" -ForegroundColor Yellow
                }
                Write-Host "`n🔖 Thêm các hashtag trên vào bài viết!" -ForegroundColor Cyan
            }
        }
        
        "4" {
            Write-Host "`n✅ CHECKLIST TRƯỚC KHI ĐĂNG BÀI:" -ForegroundColor Green
            Write-Host "==========================================" -ForegroundColor Green
            
            Write-Host "`n🔖 HASHTAG BẮT BUỘC:" -ForegroundColor Magenta
            foreach ($ht in $requiredHashtags) {
                Write-Host "   ✅ $ht" -ForegroundColor Yellow
            }
            
            Write-Host "`n📋 YÊU CẦU KHÁC:" -ForegroundColor Magenta
            foreach ($item in $checklist) {
                Write-Host $item -ForegroundColor White
            }
            
            Write-Host "`n🔗 Link đăng ký Green Creator:" -ForegroundColor Yellow
            Write-Host "   https://shorten.asia/mn1acK6X" -ForegroundColor Cyan
            
            Write-Host "`n📝 Format hashtag mẫu:" -ForegroundColor Magenta
            Write-Host "   #WonderSummer2026 #VinWonders #GreenCreator #HeLaPhaiDiVinWonders #ViralThreads" -ForegroundColor Cyan
        }
        
        "5" {
            $filename = "E:\DYT_01\workers\threads_calendar_$(Get-Date -Format 'yyyyMMdd_HHmmss').csv"
            $calendar = Create-ContentCalendar -days 30
            $calendar | Export-Csv -Path $filename -NoTypeInformation -Encoding UTF8
            Write-Host "`n✅ Đã xuất lịch đăng bài ra file: $filename" -ForegroundColor Green
            Write-Host "🔖 Nhớ thêm hashtag #WonderSummer2026 #VinWonders vào mỗi bài!" -ForegroundColor Yellow
        }
        
        "0" {
            Write-Host "`n👋 Tạm biệt! Chúc bạn kiếm thật nhiều tiền từ Wonder Summer 2026!" -ForegroundColor Magenta
            Write-Host "🔖 Đừng quên hashtag #WonderSummer2026 #VinWonders #GreenCreator" -ForegroundColor Cyan
        }
        
        default {
            Write-Host "`n❌ Lựa chọn không hợp lệ!" -ForegroundColor Red
        }
    }
    
    if ($choice -ne "0") {
        Write-Host "`nNhấn phím bất kỳ để tiếp tục..."
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    }
    
} while ($choice -ne "0")
