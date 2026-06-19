param(
  [string]$AuditDir = "C:\Temp\copilot-audit-check",
  [switch]$AutoApprove  # set to run non-interactive where sensible
)

function Is-Admin {
  return ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Prompt-Choose([string[]]$items, [string]$prompt) {
  for ($i=0; $i -lt $items.Count; $i++) { Write-Output "[$i] $($items[$i])" }
  if ($AutoApprove) { return 0 }
  $choice = Read-Host $prompt
  if ($choice -match '^\d+$' -and [int]$choice -ge 0 -and [int]$choice -lt $items.Count) { return [int]$choice }
  return $null
}

function Backup-File($path) {
  $bak = "$path.bak.$([DateTime]::UtcNow.ToString('yyyyMMddHHmmss'))"
  Copy-Item -Path $path -Destination $bak -Force
  Write-Output "BACKUP: $bak"
}

function Update-ListenAddresses($filePath) {
  $content = Get-Content -Raw -LiteralPath $filePath
  $pattern = '(^\s*listen_addresses\s*=\s*)(["'']?).*?\2\s*$'
  $lines = $content -split "`r?`n"
  $found = $false
  for ($i=0; $i -lt $lines.Count; $i++) {
    $line = $lines[$i]
    if ($line -match '^\s*#') { continue }
    if ($line -match '^\s*listen_addresses\s*=') {
      $lines[$i] = "listen_addresses = 'localhost'"
      $found = $true
      break
    }
  }
  if (-not $found) {
    # append at end
    $lines += "listen_addresses = 'localhost'"
    Write-Output "No active listen_addresses found; appended new line."
  } else {
    Write-Output "Replaced listen_addresses in file."
  }
  $new = $lines -join "`r`n"
  Set-Content -LiteralPath $filePath -Value $new -Force
}

function Find-Postgres-Confs {
  $roots = @("C:\\Program Files\\PostgreSQL","C:\\Program Files (x86)\\PostgreSQL","C:\\ProgramData","C:\\")
  $found = @()
  foreach ($r in $roots) {
    if (Test-Path $r) {
      try {
        $matches = Get-ChildItem -Path $r -Filter postgresql.conf -Recurse -ErrorAction SilentlyContinue -Force -Depth 4
        foreach ($m in $matches) { $found += $m.FullName }
      } catch { }
    }
  }
  # dedupe
  return $found | Select-Object -Unique
}

function Find-Postgres-Service {
  $svc = Get-Service -Name "postgresql*" -ErrorAction SilentlyContinue
  if ($svc) { return $svc }
  return $null
}

function Check-Port5432 {
  try {
    $listeners = Get-NetTCPConnection -LocalPort 5432 -State Listen -ErrorAction SilentlyContinue
    if ($listeners) {
      $addrs = $listeners | Select-Object -ExpandProperty LocalAddress -Unique
      Write-Output "Port 5432 listeners: $($addrs -join ', ')"
    } else {
      # fallback to netstat
      $ns = & netstat -ano | Select-String ":5432\s" -SimpleMatch
      if ($ns) { $ns | Select-Object -First 20 | ForEach-Object { $_.ToString() } } else { Write-Output "No listener found on port 5432" }
    }
  } catch {
    Write-Output ("Unable to query listeners: {0}" -f ($_))
  }
}

function RedactPreview($s) {
  if ($s -match '^(AKIA[0-9A-Z]{4})([0-9A-Z-]+)([0-9A-Z]{4})$') {
    return "$($matches[1])...[REDACTED]...$($matches[3])"
  } elseif ($s.Length -gt 8) {
    return $s.Substring(0,4) + '...[REDACTED]...' + $s.Substring($s.Length-4)
  } else { return '[REDACTED]' }
}

function Secret-Scan($dir) {
  if (-not (Test-Path $dir)) { Write-Output "AuditDir not found: $dir"; return @() }
  $patterns = @{
    'AWS_AK' = 'AKIA[0-9A-Z]{8,}'
    'AWS_SECRET' = '(?i)AWS_SECRET_ACCESS_KEY'
    'GITHUB_PAT' = 'ghp_[A-Za-z0-9_]{10,}'
    'GITHUB_TOKEN' = 'GITHUB_TOKEN'
    'BEGIN_PRIV' = '-----BEGIN'
  }
  $hits = @()
  foreach ($p in $patterns.GetEnumerator()) {
    $res = Select-String -Path (Join-Path $dir '*') -Pattern $p.Value -SimpleMatch -AllMatches -ErrorAction SilentlyContinue
    foreach ($r in $res) {
      $value = $null
      foreach ($m in $r.Matches) { $value = $m.Value; break }
      $preview = RedactPreview($value)
      $hits += [PSCustomObject]@{ File = $r.Path; Pattern = $p.Key; Match = $preview; LineNumber = $r.LineNumber }
    }
  }
  return $hits
}

function Write-Redacted-Files($dir) {
  $files = Get-ChildItem -Path (Join-Path $dir '*') -File -Recurse -ErrorAction SilentlyContinue
  foreach ($f in $files) {
    $txt = Get-Content -Raw -LiteralPath $f.FullName -ErrorAction SilentlyContinue
    if (-not $txt) { continue }
    $txt2 = $txt -replace '(?s)-----BEGIN.*?-----END.*?-----','[REDACTED]'
    $txt2 = $txt2 -replace 'AKIA[0-9A-Z]{8,}','AKIA[REDACTED]'
    $txt2 = $txt2 -replace 'ghp_[A-Za-z0-9_]{10,}','ghp_[REDACTED]'
    $txt2 = $txt2 -replace 'GITHUB_TOKEN','[REDACTED]'
    $out = "$($f.FullName).redacted.txt"
    Set-Content -LiteralPath $out -Value $txt2 -Force
    Write-Output "WROTE $out"
  }
}

function List-And-Stop-Processes {
  $patterns = "chrome","msedge","electron","discord","Code","ChatGPT","copilot"
  $procs = Get-Process | Where-Object { $_.ProcessName -match 'chrome|msedge|electron|discord|Code|ChatGPT|copilot' } -ErrorAction SilentlyContinue
  if (-not $procs) { Write-Output "No matching browser/Electron processes found." ; return }
  $procs | Select-Object Id,ProcessName,CPU,WS | Format-Table -AutoSize
  if ($AutoApprove) {
    $yn = 'Y'
  } else {
    $yn = Read-Host "Stop these processes? (Y/N)"
  }
  if ($yn -match '^[Yy]') {
    $procs | ForEach-Object { try { Stop-Process -Id $_.Id -Force -ErrorAction Stop; Write-Output "Stopped $($_.ProcessName) ($($_.Id))" } catch { Write-Warning ("Failed to stop {0}: {1}" -f $($_.ProcessName), $_) } }
  } else {
    Write-Output "Skipped stopping processes."
  }
}

# MAIN
Write-Output "Starting remediation script: $(Get-Date -Format s)"
if (-not (Is-Admin)) { Write-Warning "Not running as Administrator. Some actions (service restart, port checks) may fail. Re-run as admin if possible." }

# 1) PostgreSQL config find & update
$confs = Find-Postgres-Confs
$SkipPostgres = $false
if ($AutoApprove) {
  Write-Output "AutoApprove set — skipping modification of postgresql.conf to avoid unsafe auto-selection."
  $SkipPostgres = $true
}
if (-not $SkipPostgres) {
  if ($confs.Count -eq 0) {
    Write-Output "No postgresql.conf found in common locations. You will be asked to provide path manually."
    $manual = Read-Host "Enter full path to postgresql.conf (or press Enter to skip)"
    if ($manual) { $confs = @($manual) } else { Write-Output "Skipping PostgreSQL config step."; $SkipPostgres = $true }
  }
  if (-not $SkipPostgres) {
    $choiceIndex = Prompt-Choose -items $confs -prompt "Choose postgresql.conf to modify (index). Press Enter to skip"
    if ($choiceIndex -ne $null) {
      $chosen = $confs[$choiceIndex]
      Write-Output "Chosen: $chosen"
      Backup-File $chosen
      Update-ListenAddresses $chosen
      # Restart service
      $svcs = Find-Postgres-Service
      if ($svcs) {
        $svcList = $svcs | ForEach-Object { "$($_.Name) - $($_.DisplayName)" }
        $svcChoice = Prompt-Choose -items $svcList -prompt "Choose service to restart (index)"
        if ($svcChoice -ne $null) {
          $svcToRestart = $svcs[$svcChoice].Name
          try {
            Restart-Service -Name $svcToRestart -Force -ErrorAction Stop
            Write-Output "Restarted service $svcToRestart"
          } catch { Write-Warning ("Failed to restart {0}: {1}" -f $svcToRestart, $_) }
        } else {
          Write-Output "No service chosen; skipping restart."
        }
      } else {
        Write-Warning "No postgres service matched 'postgresql*'. You may need to restart DB manually."
      }
      Check-Port5432
    } else {
      Write-Output "Skipped PostgreSQL config changes."
    }
  } else {
    Write-Output "Skipped PostgreSQL config changes (Auto flow)."
  }
} else {
  Write-Output "Skipped PostgreSQL config changes (AutoApprove)."
}
# 2) Secret scan in audit dir
Write-Output "`n=== Secret scan in $AuditDir ==="
$hits = Secret-Scan -dir $AuditDir
if ($hits.Count -eq 0) { Write-Output "No matches found for common secret patterns." } else {
  Write-Output "Found $($hits.Count) potential matches (preview shown)."
  $hits | Format-Table -AutoSize
  if ($AutoApprove -or (Read-Host "Create redacted copies of files under $AuditDir? (Y/N)" ) -match '^[Yy]') {
    Write-Output "Creating redacted copies..."
    Write-Redacted-Files -dir $AuditDir
  } else { Write-Output "Skipped creating redacted files." }
  Write-Output "If AKIA keys found: revoke via AWS Console or AWS CLI: aws iam delete-access-key --access-key-id <AKIA...> --user-name <user>"
}

# 3) List and optionally stop Electron/Chrome processes
Write-Output "`n=== Process cleanup ==="
List-And-Stop-Processes

Write-Output "`nRemediation script completed at $(Get-Date -Format s). Summary:"
Check-Port5432
Write-Output "If you found any AKIA keys, rotate/revoke them immediately. If you changed postgresql.conf, verify application connectivity."
