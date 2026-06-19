# deploy-gcp-complete.ps1
# Script tự động deploy DYT_01 lên Google Cloud

param(
    [string]$ProjectId = "cosmic-attic-473011-m8",
    [string]$Region = "asia-southeast1",
    [string]$ImageName = "dyt-api"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🚀 DEPLOY DYT_01 LEN GOOGLE CLOUD" -ForegroundColor Cyan
Write-Host "========================================"

# 1. Kiểm tra xác thực
Write-Host "`n[1] Kiem tra xac thuc gcloud..." -ForegroundColor Yellow
$authCheck = gcloud auth list --filter=status:ACTIVE --format="value(account)"
if (-not $authCheck) {
    Write-Host "Chua dang nhap. Moi ban dang nhap..." -ForegroundColor Yellow
    gcloud auth login
}

# 2. Set project
Write-Host "`n[2] Dat project: $ProjectId" -ForegroundColor Yellow
gcloud config set project $ProjectId

# 3. Bật billing (quan trọng!)
Write-Host "`n[3] Kiem tra billing..." -ForegroundColor Yellow
$billingInfo = gcloud billing accounts list --format="value(name)" | Select-Object -First 1
if (-not $billingInfo) {
    Write-Host "ERROR: Khong tim thay billing account. Ban can:" -ForegroundColor Red
    Write-Host "  1. Truy cap https://console.cloud.google.com/billing" -ForegroundColor Yellow
    Write-Host "  2. Tao billing account (can co the tin dung)" -ForegroundColor Yellow
    Write-Host "  3. Link billing account voi project $ProjectId" -ForegroundColor Yellow
    Write-Host "`nSau do chay lai script." -ForegroundColor Yellow
    exit 1
}
Write-Host "Da tim thay billing account: $billingInfo" -ForegroundColor Green
gcloud billing accounts list --format="value(name)" | ForEach-Object {
    gcloud billing projects link $ProjectId --billing-account=$_
}

# 4. Bật các API cần thiết
Write-Host "`n[4] Bat cac API can thiet..." -ForegroundColor Yellow
$apis = @(
    "run.googleapis.com",
    "artifactregistry.googleapis.com",
    "containerregistry.googleapis.com",
    "cloudtasks.googleapis.com",
    "cloudscheduler.googleapis.com",
    "sqladmin.googleapis.com",
    "cloudbuild.googleapis.com"
)
foreach ($api in $apis) {
    Write-Host "  Bat $api..." -ForegroundColor Yellow
    gcloud services enable $api --project=$ProjectId
}

# 5. Build Docker image
Write-Host "`n[5] Build Docker image..." -ForegroundColor Yellow
$imageTag = "gcr.io/$ProjectId/$ImageName"
gcloud builds submit --tag $imageTag --project=$ProjectId

if ($LASTEXITCODE -ne 0) {
    Write-Host "Build that bai" -ForegroundColor Red
    exit 1
}

# 6. Deploy API service
Write-Host "`n[6] Deploy API service..." -ForegroundColor Yellow
gcloud run deploy dyt-api `
    --image $imageTag `
    --region $Region `
    --allow-unauthenticated `
    --platform managed `
    --project=$ProjectId `
    --set-env-vars "DATABASE_URL=sqlite:///./app.db" `
    --memory 512Mi

# 7. Deploy Worker service
Write-Host "`n[7] Deploy Worker service..." -ForegroundColor Yellow
gcloud run deploy dyt-worker `
    --image $imageTag `
    --region $Region `
    --no-allow-unauthenticated `
    --platform managed `
    --project=$ProjectId `
    --set-env-vars "DATABASE_URL=sqlite:///./app.db" `
    --memory 512Mi

# 8. Tạo Cloud Tasks queue
Write-Host "`n[8] Tao Cloud Tasks queue..." -ForegroundColor Yellow
gcloud tasks queues create dyt-tasks-queue `
    --location $Region `
    --project=$ProjectId

# 9. Lấy URL API và tạo Cloud Scheduler
Write-Host "`n[9] Tao Cloud Scheduler job..." -ForegroundColor Yellow
$API_URL = gcloud run services describe dyt-api --region $Region --platform managed --project=$ProjectId --format='value(status.url)'
Write-Host "API URL: $API_URL" -ForegroundColor Green

gcloud scheduler jobs create http dyt-scheduler `
    --schedule="*/5 * * * *" `
    --uri="$API_URL/scheduler/check-tasks" `
    --http-method=GET `
    --location $Region `
    --project=$ProjectId

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "✅ DEPLOY HOAN TAT!" -ForegroundColor Green
Write-Host "API URL: $API_URL" -ForegroundColor Cyan
Write-Host "Swagger UI: $API_URL/docs" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan