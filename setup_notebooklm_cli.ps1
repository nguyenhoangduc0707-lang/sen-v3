$ErrorActionPreference = "Stop"

$NotebookUrl = "https://notebooklm.google.com/notebook/5e64f86d-3f1b-44bd-a5c0-067fd839e3a5"
$NotebookId = "5e64f86d-3f1b-44bd-a5c0-067fd839e3a5"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  DYT_01 - NOTEBOOKLM CLI SETUP" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Notebook target:" -ForegroundColor Yellow
Write-Host "  $NotebookUrl"
Write-Host ""

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Host "ERROR: Python is not available in PATH." -ForegroundColor Red
    exit 1
}

Write-Host "Python:" -ForegroundColor Yellow
python -c "import sys; print(sys.executable); print(sys.version)"
Write-Host ""

Write-Host "Installing/upgrading NotebookLM CLI package..." -ForegroundColor Yellow
python -m pip install --upgrade notebooklm-cli
Write-Host ""

$nlmCommand = Get-Command nlm -ErrorAction SilentlyContinue
$nlmPath = $null
if ($nlmCommand) {
    $nlmPath = $nlmCommand.Source
} else {
    $userScripts = Join-Path $env:APPDATA "Python\Python311\Scripts\nlm.exe"
    if (Test-Path $userScripts) {
        $nlmPath = $userScripts
        Write-Host "nlm is installed but not in PATH. Using:" -ForegroundColor Yellow
        Write-Host "  $nlmPath"
    }
}

if (-not $nlmPath) {
    Write-Host "ERROR: nlm was installed but cannot be found." -ForegroundColor Red
    Write-Host "Try closing and reopening PowerShell, then run: nlm --help"
    exit 1
}

Write-Host "NotebookLM CLI:" -ForegroundColor Yellow
& $nlmPath --help
Write-Host ""

$env:NOTEBOOKLM_NOTEBOOK = $NotebookUrl
$env:NOTEBOOKLM_CLI = $nlmPath
$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"
$env:NO_COLOR = "1"
[System.Environment]::SetEnvironmentVariable("NOTEBOOKLM_NOTEBOOK", $NotebookUrl, "User")
[System.Environment]::SetEnvironmentVariable("NOTEBOOKLM_CLI", $nlmPath, "User")

Write-Host ""
Write-Host "Refreshing local NotebookLM context files..." -ForegroundColor Yellow
python update_notebooklm.py

Write-Host ""
Write-Host "Checking auth and uploading DYT_01 context to NotebookLM..." -ForegroundColor Yellow
python notebooklm_client.py

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  NOTEBOOKLM CLI SETUP COMPLETE" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host "Notebook ID: $NotebookId"
Write-Host "Notebook URL: $NotebookUrl"
