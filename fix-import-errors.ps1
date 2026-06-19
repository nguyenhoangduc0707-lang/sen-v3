# fix-import-errors.ps1
Write-Host "Fixing import errors..." -ForegroundColor Yellow
$orchFile = "src/orchestrator.py"
if (Test-Path $orchFile) {
    $content = Get-Content $orchFile -Raw
    if ($content -notmatch "def get_worker\(") {
        $newFunc = @"

def get_worker(name: str):
    try:
        from src.workers import WORKER_REGISTRY
        return WORKER_REGISTRY.get(name)
    except:
        return None
"@
        $content + $newFunc | Set-Content -Path $orchFile -Encoding UTF8
        Write-Host "Added get_worker to orchestrator.py" -ForegroundColor Green
    } else {
        Write-Host "get_worker already exists" -ForegroundColor Green
    }
}
