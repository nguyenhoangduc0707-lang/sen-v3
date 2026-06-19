# Sửa facebook_autoposter.py để tìm đúng đường dẫn auth file
$fbWorkerFile = "src\workers\facebook_autoposter.py"
$content = Get-Content $fbWorkerFile -Raw

# Thêm import Path
if ($content -notmatch "from pathlib import Path") {
    $content = "from pathlib import Path`n" + $content
}

# Thay đổi logic tìm auth file
$content = $content -replace 'if not self.auth_file.exists\(\):', @'
        # Tìm auth file ở nhiều vị trí
        possible_paths = [
            Path("credentials/facebook_auth.json"),
            Path(__file__).parent.parent.parent / "credentials" / "facebook_auth.json",
            Path.home() / ".dyt" / "facebook_auth.json"
        ]
        auth_file = None
        for p in possible_paths:
            if p.exists():
                auth_file = p
                break
        
        if not auth_file:
            return {"status": "error", "message": "Missing facebook_auth.json. Run save_facebook_auth.py first."}
        
        with open(auth_file) as f:
            auth_data = json.load(f)
'@

$content | Set-Content -Path $fbWorkerFile -Encoding UTF8
Write-Host "✅ Đã sửa facebook_autoposter.py để tìm auth file ở nhiều vị trí" -ForegroundColor Green