# Cấu hình namespace cần xử lý
$ns = 'DYT'

# Kiểm tra sự tồn tại của lệnh kubectl trên máy hiện tại
if (-not (Get-Command kubectl -ErrorAction SilentlyContinue)) { 
    Write-Warning "Không tìm thấy lệnh 'kubectl' trên máy này. Vui lòng chạy script trên máy đã cài đặt kubectl."
    exit 
}

Write-Host "Đang lấy danh sách các Deployments từ namespace: [$ns]..." -ForegroundColor Cyan

# Lấy dữ liệu danh sách deployment dạng JSON
$json = kubectl get deployments -n $ns -o json 2>$null
if (-not $json) {
    Write-Error "Không thể kết nối hoặc không tìm thấy namespace: $ns"
    exit
}

$items = $json | ConvertFrom-Json
if (-not $items.items -or $items.items.Count -eq 0) {
    Write-Warning "Không tìm thấy Deployment nào trong namespace: $ns"
    exit
}

Write-Host "Tìm thấy $($items.items.Count) deployments. Bắt đầu tính toán và scale..." -ForegroundColor Green
Write-Host "--------------------------------------------------------"

# Duyệt qua từng deployment để xử lý
foreach ($d in $items.items) {
    $name = $d.metadata.name
    $replicas = $d.spec.replicas
    
    # Nếu số replica mặc định bị null hoặc bằng 0, tính là 1
    if (-not $replicas -or $replicas -eq 0) { 
        $replicas = 1 
    }
    
    # Tính toán 5% số lượng replica (làm tròn lên)
    $new = [math]::Ceiling($replicas * 0.05)
    
    # Đảm bảo tối thiểu luôn có 1 replica hoạt động (tránh sập service)
    if ($new -lt 1) { 
        $new = 1 
    }
    
    # Hiển thị thông tin log ra màn hình
    Write-Host ("Đang Scale {0}: Từ {1} -> xuống {2} replicas" -f $name, $replicas, $new) -ForegroundColor Yellow
    
    # Thực hiện lệnh scale
    kubectl scale deployment/$name -n $ns --replicas=$new 2>&1 | ForEach-Object { 
        Write-Host ("  [Kết quả]: {0}" -f $_) -ForegroundColor Gray 
    }
}

Write-Host "--------------------------------------------------------"
Write-Host "HOÀN THÀNH!" -ForegroundColor Green
