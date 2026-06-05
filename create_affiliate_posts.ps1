# create_affiliate_posts.ps1
Write-Host "Dang tao bai viet affiliate..." -ForegroundColor Green

$links = @(
    "https://shorten.asia/3cSC6EUX",
    "https://shorten.asia/PjYek8R8",
    "https://shorten.asia/MxvRDqNg"
)

$campaigns = @(
    "1.6 Opening Sale",
    "6.6 Mid Year Mega Sale", 
    "15.6 Mid-month Sale",
    "25.6 Payday Sale"
)

$count = 0
foreach ($campaign in $campaigns) {
    foreach ($link in $links) {
        $count++
        
        $content = @"
========================================
Bai viet $count - $campaign
========================================

SHOPEE MEGA SALE 6.6

- Giam gia den 50%
- Freeship 0D toan quoc
- Voucher Xtra len den 6 trieu dong
- Mua truoc tra sau 0%

Dang ky ngay hom nay:
$link

#Shopee6_6 #MegaSale #Affiliate

"@
        
        $filename = "post_${count}_$($campaign -replace ' ', '_').txt"
        $content | Out-File -FilePath $filename -Encoding UTF8
        Write-Host "Da tao: $filename" -ForegroundColor Yellow
    }
}

Write-Host "`nHoan tat! Da tao $count bai viet" -ForegroundColor Green
Write-Host "Xem cac file: dir post_*.txt" -ForegroundColor Cyan