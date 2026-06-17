# Script tự động setup môi trường cho Google GenAI với Gemini 3.5 Flash
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  GOOGLE GENAI - GEMINI 3.5 FLASH SETUP" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "🤖 Model mới nhất: gemini-3.5-flash" -ForegroundColor Green
Write-Host "📅 Knowledge cutoff: Tháng 1/2025" -ForegroundColor Green
Write-Host "⚡ Đặc điểm: Tốc độ cao, chi phí thấp" -ForegroundColor Green
Write-Host ""

# Kiểm tra pip và cài đặt thư viện
Write-Host "📦 Đang kiểm tra và cài đặt thư viện..." -ForegroundColor Yellow
$checkPackage = pip show google-genai 2>$null
if (-not $checkPackage) {
    Write-Host "Đang cài đặt google-genai..." -ForegroundColor Yellow
    pip install --upgrade google-genai
} else {
    Write-Host "✅ google-genai đã được cài đặt" -ForegroundColor Green
    pip install --upgrade google-genai
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  CẤU HÌNH AUTHENTICATION" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Chọn phương thức xác thực:" -ForegroundColor Yellow
Write-Host "1. API Key (đơn giản, dùng cho cá nhân) - Khuyến nghị" -ForegroundColor White
Write-Host "2. Vertex AI / OAuth2 (doanh nghiệp)" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Nhập lựa chọn (1 hoặc 2)"

if ($choice -eq "1") {
    Write-Host ""
    Write-Host "🔑 CẤU HÌNH API KEY" -ForegroundColor Cyan
    Write-Host "📍 Lấy API Key miễn phí tại: https://aistudio.google.com/app/apikey" -ForegroundColor Yellow
    $apiKey = Read-Host "Nhập Google API Key của bạn"
    
    # Set environment variable cho phiên hiện tại
    $env:GOOGLE_API_KEY = $apiKey
    Remove-Item Env:GOOGLE_GENAI_USE_ENTERPRISE -ErrorAction SilentlyContinue
    
    # Lưu vào User environment (tùy chọn)
    $savePermanent = Read-Host "Lưu permanent? (y/n)"
    if ($savePermanent -eq "y") {
        [System.Environment]::SetEnvironmentVariable('GOOGLE_API_KEY', $apiKey, 'User')
        Write-Host "✅ Đã lưu API key permanent" -ForegroundColor Green
    }
    
    Write-Host ""
    Write-Host "✅ Đã cấu hình API Key mode cho Gemini 3.5 Flash" -ForegroundColor Green
    
} elseif ($choice -eq "2") {
    Write-Host ""
    Write-Host "🔐 CẤU HÌNH VERTEX AI" -ForegroundColor Cyan
    
    $project = Read-Host "Nhập Google Cloud Project ID"
    $location = Read-Host "Nhập Location (mặc định: us-central1)"
    if ([string]::IsNullOrWhiteSpace($location)) { $location = "us-central1" }
    
    # Set environment variables
    $env:GOOGLE_CLOUD_PROJECT = $project
    $env:GOOGLE_CLOUD_LOCATION = $location
    $env:GOOGLE_GENAI_USE_ENTERPRISE = "True"
    Remove-Item Env:GOOGLE_API_KEY -ErrorAction SilentlyContinue
    
    # Lưu permanent
    $savePermanent = Read-Host "Lưu permanent? (y/n)"
    if ($savePermanent -eq "y") {
        [System.Environment]::SetEnvironmentVariable('GOOGLE_CLOUD_PROJECT', $project, 'User')
        [System.Environment]::SetEnvironmentVariable('GOOGLE_CLOUD_LOCATION', $location, 'User')
        [System.Environment]::SetEnvironmentVariable('GOOGLE_GENAI_USE_ENTERPRISE', 'True', 'User')
        Write-Host "✅ Đã lưu cấu hình permanent" -ForegroundColor Green
    }
    
    # OAuth2 login
    Write-Host ""
    Write-Host "🔄 Đang đăng nhập Google Cloud..." -ForegroundColor Yellow
    gcloud auth application-default login
    
    Write-Host "✅ Đã cấu hình Vertex AI mode cho Gemini 3.5 Flash" -ForegroundColor Green
} else {
    Write-Host "❌ Lựa chọn không hợp lệ" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  KIỂM TRA CẤU HÌNH VỚI GEMINI 3.5 FLASH" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
python test_genai_full.py

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  SETUP HOÀN TẤT!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "🚀 Các lệnh hữu ích:" -ForegroundColor Yellow
Write-Host "  • Chạy test nhanh: python test_simple.py"
Write-Host "  • Chạy test đầy đủ: python test_genai_full.py"
