# install-kubectl.ps1
# Cài kubectl trên Windows: thử winget -> choco -> download binary
# Chạy elevated để thêm vào System PATH; nếu không, sẽ thêm vào User PATH.

Function Test-Kubectl { try { kubectl version --client -o json >$null 2>&1; return $true } catch { return $false } }

if (Test-Kubectl) { Write-Host "kubectl đã được cài sẵn." -ForegroundColor Green; exit 0 }

Write-Host "Bắt đầu cài kubectl..." -ForegroundColor Cyan

# 1) Try winget
if (Get-Command winget -ErrorAction SilentlyContinue) {
    Write-Host "Thử cài bằng winget..." -ForegroundColor Yellow
    try {
        winget install --id Kubernetes.kubectl -e --accept-source-agreements --accept-package-agreements -h
    } catch { Write-Warning "winget install thất bại: $_" }
    if (Test-Kubectl) { Write-Host "Đã cài kubectl bằng winget." -ForegroundColor Green; exit 0 }
}

# 2) Try choco
if (Get-Command choco -ErrorAction SilentlyContinue) {
    Write-Host "Thử cài bằng choco..." -ForegroundColor Yellow
    try {
        choco install kubernetes-cli -y
    } catch { Write-Warning "choco install thất bại: $_" }
    if (Test-Kubectl) { Write-Host "Đã cài kubectl bằng choco." -ForegroundColor Green; exit 0 }
}

# 3) Manual download
Write-Host "Không có winget/choco hoặc cài thất bại. Tải kubectl binary stable..." -ForegroundColor Yellow
$stable = try { Invoke-RestMethod -Uri 'https://dl.k8s.io/release/stable.txt' -UseBasicParsing -ErrorAction Stop } catch { 'v1.28.0' }
$uri = "https://dl.k8s.io/release/$stable/bin/windows/amd64/kubectl.exe"
$destDir = Join-Path $env:ProgramFiles 'kubectl'
if (-not (Test-Path $destDir)) { New-Item -Path $destDir -ItemType Directory -Force | Out-Null }
$dest = Join-Path $destDir 'kubectl.exe'
Write-Host "Tải $uri -> $dest" -ForegroundColor Cyan
try { Invoke-WebRequest -Uri $uri -OutFile $dest -UseBasicParsing -ErrorAction Stop } catch { Write-Error "Tải thất bại: $_"; exit 1 }

# Add to PATH: prefer System if elevated, else User
$inAdmin = ([bool]([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator))
if ($inAdmin) {
    Write-Host "Đang thêm $destDir vào System PATH" -ForegroundColor Cyan
    $path = [Environment]::GetEnvironmentVariable('Path',[EnvironmentVariableTarget]::Machine)
    if ($path -notlike "*${destDir}*") { [Environment]::SetEnvironmentVariable('Path', "$path;${destDir}",[EnvironmentVariableTarget]::Machine) }
} else {
    Write-Host "Không chạy elevated: thêm vào User PATH" -ForegroundColor Yellow
    $path = [Environment]::GetEnvironmentVariable('Path',[EnvironmentVariableTarget]::User)
    if ($path -notlike "*${destDir}*") { [Environment]::SetEnvironmentVariable('Path', "$path;${destDir}",[EnvironmentVariableTarget]::User) }
    Write-Host "(Bạn có thể cần mở lại terminal để PATH được cập nhật.)" -ForegroundColor Gray
}

if (Test-Kubectl) { Write-Host "kubectl da cai thanh cong." -ForegroundColor Green } else { Write-Warning "Cai xong nhung chua the chay kubectl - kiem tra PATH va khoi dong lai shell." }

Write-Host "Kiểm tra client version:" -ForegroundColor Cyan
kubectl version --client --short

Write-Host "Hoàn tất. Sau khi kubectl có hiệu lực, chạy: powershell -ExecutionPolicy Bypass -File \"E:\DYT_01\scale-to-5percent.ps1\"" -ForegroundColor Green
