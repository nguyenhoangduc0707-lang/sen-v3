# ============================================
# REBUILD-SENV3.PS1
# SEN V3 Project Rebuild and Cleanup Script
# Run as Administrator
# ============================================

param(
    [switch]$DryRun,
    [switch]$Force
)

$ColorInfo = "Cyan"
$ColorSuccess = "Green"
$ColorWarning = "Yellow"
$ColorError = "Red"

# Header
Write-Host "`n============================================" -ForegroundColor $ColorInfo
Write-Host "   SEN V3 PROJECT REBUILD & CLEANUP" -ForegroundColor $ColorInfo
Write-Host "============================================`n" -ForegroundColor $ColorInfo

if ($DryRun) {
    Write-Host "[DRY RUN MODE] - No actual changes will be made`n" -ForegroundColor $ColorWarning
}

# ============================================
# PART 1: CHECK CURRENT STATUS
# ============================================
Write-Host "[PART 1] CHECKING PROJECT STATUS" -ForegroundColor $ColorInfo
Write-Host "----------------------------------------" -ForegroundColor $ColorInfo

$ProjectRoot = Get-Location
Write-Host "Project Directory: $ProjectRoot" -ForegroundColor $ColorSuccess

# Count files by type
$pyFiles = Get-ChildItem -Recurse -Filter "*.py" -ErrorAction SilentlyContinue | Measure-Object | Select-Object -ExpandProperty Count
$jsFiles = Get-ChildItem -Recurse -Filter "*.js" -ErrorAction SilentlyContinue | Measure-Object | Select-Object -ExpandProperty Count
$jsonFiles = Get-ChildItem -Recurse -Filter "*.json" -ErrorAction SilentlyContinue | Measure-Object | Select-Object -ExpandProperty Count
$txtFiles = Get-ChildItem -Recurse -Filter "*.txt" -ErrorAction SilentlyContinue | Measure-Object | Select-Object -ExpandProperty Count

Write-Host "`nFile Statistics:" -ForegroundColor $ColorInfo
Write-Host "   Python files: $pyFiles"
Write-Host "   JavaScript files: $jsFiles"
Write-Host "   JSON files: $jsonFiles"
Write-Host "   TXT files: $txtFiles"

$totalSize = (Get-ChildItem -Recurse -File -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1MB
Write-Host "`nTotal Size: $([math]::Round($totalSize, 2)) MB" -ForegroundColor $ColorSuccess

# ============================================
# PART 2: DELETE JUNK FILES
# ============================================
Write-Host "`n[PART 2] DELETING JUNK FILES" -ForegroundColor $ColorInfo
Write-Host "----------------------------------------" -ForegroundColor $ColorInfo

$junkPatterns = @(
    "*.pyc", "*.pyo", "__pycache__",
    "*.bak", "*.bak2", "*.old", "*.backup",
    "*.log", "*.tmp", "*.temp",
    ".DS_Store", "Thumbs.db"
)

$deletedCount = 0
foreach ($pattern in $junkPatterns) {
    $files = Get-ChildItem -Recurse -Filter $pattern -ErrorAction SilentlyContinue
    foreach ($file in $files) {
        if (-not $DryRun) {
            Remove-Item -Path $file.FullName -Force -ErrorAction SilentlyContinue
        }
        Write-Host "   Deleted: $($file.FullName)" -ForegroundColor $ColorWarning
        $deletedCount++
    }
}

Write-Host "`nDeleted $deletedCount junk files" -ForegroundColor $ColorSuccess

# ============================================
# PART 3: DELETE OLD PROJECT FOLDERS
# ============================================
Write-Host "`n[PART 3] DELETING OLD PROJECTS" -ForegroundColor $ColorInfo
Write-Host "----------------------------------------" -ForegroundColor $ColorInfo

$oldFolders = @(
    "00_CORE", "01_CONTENT", "02_CAMPAIGN", "03_POST", "04_AFFILIATE", "05_MONITOR",
    "ACFC_CAMPAIGN", "ACFC_CAMPAIGN_FULL", "ACFC_DEMO", "ACFC_IMAGES", "ACFC_POSTS",
    "VinWonders_Project", "Vin_hinh_anh", "Vin_video",
    "Hinh_sales_off", "affiliate", "fullwork", "workers",
    "data", "tasks", "media"
)

foreach ($folder in $oldFolders) {
    if (Test-Path $folder) {
        if (-not $DryRun) {
            Remove-Item -Path $folder -Recurse -Force -ErrorAction SilentlyContinue
        }
        Write-Host "   Deleted: $folder/" -ForegroundColor $ColorWarning
    }
}

# ============================================
# PART 4: DELETE OLD SCRIPTS
# ============================================
Write-Host "`n[PART 4] DELETING OLD SCRIPTS" -ForegroundColor $ColorInfo
Write-Host "----------------------------------------" -ForegroundColor $ColorInfo

$scriptPatterns = @(
    "test_*.py", "demo_*.py", "check_*.py", "run_*.ps1", "start_*.ps1",
    "accesstrade_*.py", "auto_*.py", "tiktok_*.py", "byteplus_*.py",
    "generate_*.py", "find_*.py", "get_*.py", "sync_*.py",
    "export_*.py", "upload_*.py", "create_*.py", "add_*.py"
)

foreach ($pattern in $scriptPatterns) {
    $files = Get-ChildItem -Filter $pattern -ErrorAction SilentlyContinue
    foreach ($file in $files) {
        if (-not $DryRun) {
            Remove-Item -Path $file.FullName -Force -ErrorAction SilentlyContinue
        }
        Write-Host "   Deleted: $($file.Name)" -ForegroundColor $ColorWarning
    }
}

# ============================================
# PART 5: CREATE CLEAN STRUCTURE
# ============================================
Write-Host "`n[PART 5] CREATING CLEAN STRUCTURE" -ForegroundColor $ColorInfo
Write-Host "----------------------------------------" -ForegroundColor $ColorInfo

$coreFolders = @("src", "web", "config", "docs", "scripts", "tests", ".github")
foreach ($folder in $coreFolders) {
    if (-not (Test-Path $folder)) {
        if (-not $DryRun) {
            New-Item -ItemType Directory -Path $folder -Force -ErrorAction SilentlyContinue | Out-Null
        }
        Write-Host "   Created: $folder/" -ForegroundColor $ColorSuccess
    }
}

# Create subfolders
$subFolders = @{
    "src" = @("agents", "workers", "db", "utils", "models")
    "web" = @("routers", "services", "schemas")
    ".github" = @("workflows")
}

foreach ($parent in $subFolders.Keys) {
    foreach ($sub in $subFolders[$parent]) {
        $subPath = Join-Path $parent $sub
        if (-not (Test-Path $subPath)) {
            if (-not $DryRun) {
                New-Item -ItemType Directory -Path $subPath -Force -ErrorAction SilentlyContinue | Out-Null
            }
            Write-Host "   Created: $subPath/" -ForegroundColor $ColorSuccess
        }
    }
}

# ============================================
# PART 6: CREATE STARTUP SCRIPTS
# ============================================
Write-Host "`n[PART 6] CREATING STARTUP SCRIPTS" -ForegroundColor $ColorInfo
Write-Host "----------------------------------------" -ForegroundColor $ColorInfo

if (-not $DryRun) {
    # Create start-api.ps1
    @'
# start-api.ps1
Write-Host "Starting SEN V3 API Server..." -ForegroundColor Cyan
$env:FERNET_KEY = "WphX9F3TeO5B4N4EcBhxd1ehvI9NhgHPz1mH2cPi9QI="
$env:JWT_SECRET_KEY = "xK9mP2nQ5rS8tU1wX4zA7cD0fG3jJ6lM9oR2sU5vY8"
uvicorn web.main:app --reload --host 0.0.0.0 --port 8001
'@ | Out-File -FilePath "start-api.ps1" -Encoding ascii

    # Create start-worker.ps1
    @'
# start-worker.ps1
Write-Host "Starting SEN V3 Worker..." -ForegroundColor Cyan
python run_worker.py
'@ | Out-File -FilePath "start-worker.ps1" -Encoding ascii

    # Create start-all.ps1
    @'
# start-all.ps1
Write-Host "Starting SEN V3 Full System..." -ForegroundColor Cyan
Write-Host "Starting API Server..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit -Command cd '$PSScriptRoot'; .\start-api.ps1"
Start-Sleep -Seconds 2
Write-Host "Starting Worker..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit -Command cd '$PSScriptRoot'; .\start-worker.ps1"
Write-Host "System started! API: http://localhost:8001/docs" -ForegroundColor Green
'@ | Out-File -FilePath "start-all.ps1" -Encoding ascii

    Write-Host "   Created: start-api.ps1" -ForegroundColor $ColorSuccess
    Write-Host "   Created: start-worker.ps1" -ForegroundColor $ColorSuccess
    Write-Host "   Created: start-all.ps1" -ForegroundColor $ColorSuccess
}

# ============================================
# PART 7: SUMMARY
# ============================================
Write-Host "`n[PART 7] SUMMARY" -ForegroundColor $ColorInfo
Write-Host "----------------------------------------" -ForegroundColor $ColorInfo

if ($DryRun) {
    Write-Host "DRY RUN COMPLETED - No actual changes made" -ForegroundColor $ColorWarning
    Write-Host "Run again with -Force to apply changes" -ForegroundColor $ColorInfo
} else {
    $newFileCount = Get-ChildItem -Recurse -File -ErrorAction SilentlyContinue | Measure-Object | Select-Object -ExpandProperty Count
    $newSize = (Get-ChildItem -Recurse -File -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1MB
    
    Write-Host "REBUILD COMPLETED!" -ForegroundColor $ColorSuccess
    Write-Host "   Files remaining: $newFileCount" -ForegroundColor $ColorSuccess
    Write-Host "   Total size: $([math]::Round($newSize, 2)) MB" -ForegroundColor $ColorSuccess
    Write-Host "   Junk deleted: $deletedCount files" -ForegroundColor $ColorSuccess
}

Write-Host "`nHOW TO USE:" -ForegroundColor $ColorInfo
Write-Host "   1. Start API:        .\start-api.ps1" -ForegroundColor $ColorSuccess
Write-Host "   2. Start Worker:     .\start-worker.ps1" -ForegroundColor $ColorSuccess
Write-Host "   3. Start all:        .\start-all.ps1" -ForegroundColor $ColorSuccess
Write-Host "   4. API Docs:         http://localhost:8001/docs" -ForegroundColor $ColorSuccess
Write-Host "   5. GitHub:           https://github.com/nguyenhoangduc0707-lang/sen-v3" -ForegroundColor $ColorSuccess

Write-Host "`n============================================" -ForegroundColor $ColorInfo