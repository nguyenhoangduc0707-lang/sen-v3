<#
Create and optionally merge a PR for a branch using GitHub CLI (gh).
Usage (from repo root):
  pwsh .\scripts\create_and_merge_pr.ps1 -Branch ci/ci-full -Base master -Title "chore(ci): add CI workflow" -Body "Add CI workflow" -AutoMerge
Notes: gh must be installed and the user must be authenticated (gh auth login --web).
This script does NOT accept tokens; it relies on gh auth.
#>

param(
    [string]$Branch = 'ci/ci-full',
    [string]$Base = 'master',
    [string]$Title = 'chore(ci): add CI workflow',
    [string]$Body = 'Add CI workflow (backend tests, lint, security; frontend build).',
    [switch]$AutoMerge
)

function Fail($msg){ Write-Error $msg; exit 1 }

# Ensure gh is installed
$gh = Get-Command gh -ErrorAction SilentlyContinue
if (-not $gh) {
    Fail 'GitHub CLI (gh) not found. Install with: winget install --id GitHub.cli or see https://cli.github.com/'
}

# Ensure we're in a git repo
if (-not (Test-Path ".git" -PathType Container)) {
    Fail 'Current directory is not a git repository. Run this script from the repo root.'
}

# Check authentication
$auth = gh auth status 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host 'Not authenticated with gh. Opening web login...'
    gh auth login --web || Fail 'gh auth login failed'
}

# Create PR if not exists
$existing = gh pr list --head $Branch --base $Base --limit 1 --json number,url,state --jq '.[] | select(.state=="OPEN") | .url' 2>$null
if ($existing) {
    Write-Host "Found existing open PR: $existing"
    $prUrl = $existing
} else {
    Write-Host "Creating PR: $Branch -> $Base"
    $create = gh pr create --base $Base --head $Branch --title $Title --body $Body --repo $(git config --get remote.origin.url) 2>&1
    if ($LASTEXITCODE -ne 0) { Fail "gh pr create failed:\n$create" }
    # Extract URL from output
    $prUrl = ($create -split "\r?\n" | Select-String -Pattern 'https://github.com/').Matches.Value | Select-Object -First 1
    if (-not $prUrl) { Write-Host "PR created; unable to parse URL from gh output. Use 'gh pr list' to find it." }
    else { Write-Host "PR created: $prUrl" }
}

if ($AutoMerge) {
    Write-Host 'Attempting to merge PR...'
    # Find PR number
    $prNum = gh pr view --json number --jq '.number' 2>$null
    if (-not $prNum) {
        Write-Host 'Could not determine PR number, trying to parse from URL...'
        if ($prUrl -match '/pull/(\d+)') { $prNum = $Matches[1] }
    }
    if (-not $prNum) { Fail 'PR number not found; cannot merge automatically.' }

    gh pr merge $prNum --merge --delete-branch --admin || Fail 'gh pr merge failed'
    Write-Host "PR #$prNum merged and branch deleted."
} else {
    Write-Host 'AutoMerge not requested. Open the PR URL to review and merge manually.'
    if ($prUrl) { Write-Host $prUrl }
}
