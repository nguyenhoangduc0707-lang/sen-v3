[33mcommit 2a0155a03cc439c5faa66026d83da90699329d32[m[33m ([m[1;36mHEAD[m[33m -> [m[1;32mnew-branch[m[33m, [m[1;32mfeature/new-feature[m[33m)[m
Author: Admin <admin@example.com>
Date:   Thu Jun 18 06:18:06 2026 +0700

    Final cleanup: remove deleted files and update .gitignore

[1mdiff --git a/.gitignore b/.gitignore[m
[1mindex 0318e45b..14656f8e 100644[m
[1m--- a/.gitignore[m
[1m+++ b/.gitignore[m
[36m@@ -26,3 +26,6 @@[m [mpackage-lock.json[m
 gemini-cli/[m
 package-lock.json[m
 node_modules/[m
[32m+[m
[32m+[m[32mgemini-cli/[m
[32m+[m[32mpackage-lock.json[m

[33mcommit 24b0403f88c5a6492db1dd715d7dfef0592eeb45[m
Author: Admin <admin@example.com>
Date:   Thu Jun 18 06:17:34 2026 +0700

    Final cleanup: remove deleted files, update .gitignore

[1mdiff --git a/.gitignore b/.gitignore[m
[1mindex 505195b6..0318e45b 100644[m
[1m--- a/.gitignore[m
[1m+++ b/.gitignore[m
[36m@@ -21,3 +21,8 @@[m [mforeplay_data.json[m
 worker_simple[m
 gemini-cli/[m
 package-lock.json[m
[32m+[m
[32m+[m[32m# Gemini CLI[m
[32m+[m[32mgemini-cli/[m
[32m+[m[32mpackage-lock.json[m
[32m+[m[32mnode_modules/[m

[33mcommit 1641111c22ad71eab6f608e734c785bf632a7162[m
Author: Admin <admin@example.com>
Date:   Thu Jun 18 06:17:05 2026 +0700

    Clean up: remove deleted files, update .gitignore

[1mdiff --git a/.gitignore b/.gitignore[m
[1mindex f9cd3faa..505195b6 100644[m
[1m--- a/.gitignore[m
[1m+++ b/.gitignore[m
[36m@@ -19,3 +19,5 @@[m [msen_v3.db[m
 app.db[m
 foreplay_data.json[m
 worker_simple[m
[32m+[m[32mgemini-cli/[m
[32m+[m[32mpackage-lock.json[m
[1mdiff --git a/asyncio.run b/asyncio.run[m
[1mdeleted file mode 100644[m
[1mindex 91cf03be..00000000[m
[1m--- a/asyncio.run[m
[1m+++ /dev/null[m
[36m@@ -1,24 +0,0 @@[m
[31m-# install playwright: pip install playwright[m
[31m-# python -m playwright install[m
[31m-[m
[31m-import asyncio[m
[31m-from playwright.async_api import async_playwright[m
[31m-[m
[31m-async def save_fb_cookies():[m
[31m-    async with async_playwright() as p:[m
[31m-        # Mở trình duyệt (chạy ở chế độ có giao diện để bạn đăng nhập)[m
[31m-        browser = await p.chromium.launch(headless=False)[m
[31m-        context = await browser.new_context()[m
[31m-        page = await context.new_page()[m
[31m-        [m
[31m-        # Đi tới trang Facebook[m
[31m-        await page.goto('https://www.facebook.com/')[m
[31m-        print("🔐 Vui lòng đăng nhập Facebook bằng tay trong cửa sổ trình duyệt vừa mở...")[m
[31m-        input("📌 Sau khi đăng nhập thành công, nhấn ENTER để lưu cookies...")[m
[31m-        [m
[31m-        # Lưu trạng thái (cookies + localStorage) vào file[m
[31m-        await context.storage_state(path="facebook_auth.json")[m
[31m-        await browser.close()[m
[31m-        print("✅ Cookies đã được lưu vào file 'facebook_auth.json'")[m
[31m-[m
[31m-asyncio.run(save_fb_cookies())[m
\ No newline at end of file[m
[1mdiff --git a/run_test.bat b/run_test.bat[m
[1mdeleted file mode 100644[m
[1mindex 46dac544..00000000[m
[1m--- a/run_test.bat[m
[1m+++ /dev/null[m
[36m@@ -1,20 +0,0 @@[m
[31m-@echo off[m
[31m-chcp 65001 > nul[m
[31m-echo ========================================[m
[31m-echo   GEMINI 3.5 FLASH - GOOGLE GENAI TEST[m
[31m-echo ========================================[m
[31m-echo.[m
[31m-[m
[31m-REM Set your API key here (thay YOUR_API_KEY b?ng key th?t)[m
[31m-set GOOGLE_API_KEY=gemini-3.5-flash[m
[31m-set GOOGLE_GENAI_USE_ENTERPRISE=False[m
[31m-[m
[31m-echo Running test with Gemini 3.5 Flash...[m
[31m-echo.[m
[31m-python test_simple.py[m
[31m-[m
[31m-echo.[m
[31m-echo ========================================[m
[31m-echo Test completed![m
[31m-echo ========================================[m
[31m-pause[m
[1mdiff --git a/setup_genai.ps1 b/setup_genai.ps1[m
[1mdeleted file mode 100644[m
[1mindex 1a9922bc..00000000[m
[1m--- a/setup_genai.ps1[m
[1m+++ /dev/null[m
[36m@@ -1,101 +0,0 @@[m
[31m-﻿# Script tự động setup môi trường cho Google GenAI với Gemini 3.5 Flash[m
[31m-Write-Host "========================================" -ForegroundColor Cyan[m
[31m-Write-Host "  GOOGLE GENAI - GEMINI 3.5 FLASH SETUP" -ForegroundColor Cyan[m
[31m-Write-Host "========================================" -ForegroundColor Cyan[m
[31m-Write-Host ""[m
[31m-Write-Host "🤖 Model mới nhất: gemini-3.5-flash" -ForegroundColor Green[m
[31m-Write-Host "📅 Knowledge cutoff: Tháng 1/2025" -ForegroundColor Green[m
[31m-Write-Host "⚡ Đặc điểm: Tốc độ cao, chi phí thấp" -ForegroundColor Green[m
[31m-Write-Host ""[m
[31m-[m
[31m-# Kiểm tra pip và cài đặt thư viện[m
[31m-Write-Host "📦 Đang kiểm tra và cài đặt thư viện..." -ForegroundColor Yellow[m
[31m-$checkPackage = pip show google-genai 2>$null[m
[31m-if (-not $checkPackage) {[m
[31m-    Write-Host "Đang cài đặt google-genai..." -ForegroundColor Yellow[m
[31m-    pip install --upgrade google-genai[m
[31m-} else {[m
[31m-    Write-Host "✅ google-genai đã được cài đặt" -ForegroundColor Green[m
[31m-    pip install --upgrade google-genai[m
[31m-}[m
[31m-[m
[31m-Write-Host ""[m
[31m-Write-Host "========================================" -ForegroundColor Cyan[m
[31m-Write-Host "  CẤU HÌNH AUTHENTICATION" -ForegroundColor Cyan[m
[31m-Write-Host "========================================" -ForegroundColor Cyan[m
[31m-Write-Host ""[m
[31m-Write-Host "Chọn phương thức xác thực:" -ForegroundColor Yellow[m
[31m-Write-Host "1. API Key (đơn giản, dùng cho cá nhân) - Khuyến nghị" -ForegroundColor White[m
[31m-Write-Host "2. Vertex AI / OAuth2 (doanh nghiệp)" -ForegroundColor White[m
[31m-Write-Host ""[m
[31m-[m
[31m-$choice = Read-Host "Nhập lựa chọn (1 hoặc 2)"[m
[31m-[m
[31m-if ($choice -eq "1") {[m
[31m-    Write-Host ""[m
[31m-    Write-Host "🔑 CẤU HÌNH API KEY" -ForegroundColor Cyan[m
[31m-    Write-Host "📍 Lấy API Key miễn phí tại: https://aistudio.google.com/app/apikey" -ForegroundColor Yellow[m
[31m-    $apiKey = Read-Host "Nhập Google API Key của bạn"[m
[31m-    [m
[31m-    # Set environment variable cho phiên hiện tại[m
[31m-    $env:GOOGLE_API_KEY = $apiKey[m
[31m-    Remove-Item Env:GOOGLE_GENAI_USE_ENTERPRISE -ErrorAction SilentlyContinue[m
[31m-    [m
[31m-    # Lưu vào User environment (tùy chọn)[m
[31m-    $savePermanent = Read-Host "Lưu permanent? (y/n)"[m
[31m-    if ($savePermanent -eq "y") {[m
[31m-        [System.Environment]::SetEnvironmentVariable('GOOGLE_API_KEY', $apiKey, 'User')[m
[31m-        Write-Host "✅ Đã lưu API key permanent" -ForegroundColor Green[m
[31m-    }[m
[31m-    [m
[31m-    Write-Host ""[m
[31m-    Write-Host "✅ Đã cấu hình API Key mode cho Gemini 3.5 Flash" -ForegroundColor Green[m
[31m-    [m
[31m-} elseif ($choice -eq "2") {[m
[31m-    Write-Host ""[m
[31m-    Write-Host "🔐 CẤU HÌNH VERTEX AI" -ForegroundColor Cyan[m
[31m-    [m
[31m-    $project = Read-Host "Nhập Google Cloud Project ID"[m
[31m-    $location = Read-Host "Nhập Location (mặc định: us-central1)"[m
[31m-    if ([string]::IsNullOrWhiteSpace($location)) { $location = "us-central1" }[m
[31m-    [m
[31m-    # Set environment variables[m
[31m-    $env:GOOGLE_CLOUD_PROJECT = $project[m
[31m-    $env:GOOGLE_CLOUD_LOCATION = $location[m
[31m-    $env:GOOGLE_GENAI_USE_ENTERPRISE = "True"[m
[31m-    Remove-Item Env:GOOGLE_API_KEY -ErrorAction SilentlyContinue[m
[31m-    [m
[31m-    # Lưu permanent[m
[31m-    $savePermanent = Read-Host "Lưu permanent? (y/n)"[m
[31m-    if ($savePermanent -eq "y") {[m
[31m-        [System.Environment]::SetEnvironmentVariable('GOOGLE_CLOUD_PROJECT', $project, 'User')[m
[31m-        [System.Environment]::SetEnvironmentVariable('GOOGLE_CLOUD_LOCATION', $location, 'User')[m
[31m-        [System.Environment]::SetEnvironmentVariable('GOOGLE_GENAI_USE_ENTERPRISE', 'True', 'User')[m
[31m-        Write-Host "✅ Đã lưu cấu hình permanent" -ForegroundColor Green[m
[31m-    }[m
[31m-    [m
[31m-    # OAuth2 login[m
[31m-    Write-Host ""[m
[31m-    Write-Host "🔄 Đang đăng nhập Google Cloud..." -ForegroundColor Yellow[m
[31m-    gcloud auth application-default login[m
[31m-    [m
[31m-    Write-Host "✅ Đã cấu hình Vertex AI mode cho Gemini 3.5 Flash" -ForegroundColor Green[m
[31m-} else {[m
[31m-    Write-Host "❌ Lựa chọn không hợp lệ" -ForegroundColor Red[m
[31m-    exit 1[m
[31m-}[m
[31m-[m
[31m-Write-Host ""[m
[31m-Write-Host "========================================" -ForegroundColor Cyan[m
[31m-Write-Host "  KIỂM TRA CẤU HÌNH VỚI GEMINI 3.5 FLASH" -ForegroundColor Cyan[m
[31m-Write-Host "========================================" -ForegroundColor Cyan[m
[31m-python test_genai_full.py[m
[31m-[m
[31m-Write-Host ""[m
[31m-Write-Host "========================================" -ForegroundColor Green[m
[31m-Write-Host "  SETUP HOÀN TẤT!" -ForegroundColor Green[m
[31m-Write-Host "========================================" -ForegroundColor Green[m
[31m-Write-Host ""[m
[31m-Write-Host "🚀 Các lệnh hữu ích:" -ForegroundColor Yellow[m
[31m-Write-Host "  • Chạy test nhanh: python test_simple.py"[m
[31m-Write-Host "  • Chạy test đầy đủ: python test_genai_full.py"[m

[33mcommit 847f048669e731cd555512838b49796c8f9d63fe[m
Author: Admin <admin@example.com>
Date:   Thu Jun 18 06:14:28 2026 +0700

    Cap nhat .gitignore va don dep repository

[1mdiff --git a/.gitignore b/.gitignore[m
[1mindex eeef63a4..f9cd3faa 100644[m
[1m--- a/.gitignore[m
[1m+++ b/.gitignore[m
[36m@@ -1,62 +1,21 @@[m
 ﻿# Python[m
 __pycache__/[m
 *.py[cod][m
[31m-*$py.class[m
[31m-*.so[m
[31m-.Python[m
 venv/[m
 env/[m
[31m-ENV/[m
[31m-.venv[m
[31m-[m
[31m-# Environment variables[m
[31m-.env[m
[31m-.env.local[m
[31m-.env.*.local[m
[31m-[m
[31m-# IDE[m
[31m-.vscode/[m
[31m-.idea/[m
[31m-*.swp[m
[31m-*.swo[m
[31m-[m
[31m-# Logs[m
[32m+[m[32m*.db[m
[32m+[m[32m*.db-shm[m
[32m+[m[32m*.db-wal[m
[32m+[m[32m*.xlsx[m
 *.log[m
 logs/[m
[31m-*.pid[m
[31m-[m
[31m-# Database[m
[31m-*.db[m
[31m-*.sqlite[m
[31m-*.sqlite3[m
[31m-[m
[31m-# Test & coverage (Phase 4 cleanup)[m
[31m-.pytest_cache/[m
[31m-.coverage[m
[31m-htmlcov/[m
[31m-.coverage.*[m
[31m-*.cover[m
[31m-*.py,cover[m
[31m-[m
[31m-# Backup[m
[31m-*.bak[m
[31m-backup_*/[m
[31m-*.backup[m
[31m-[m
[31m-# Test files[m
[31m-test_*.py[m
[31m-debug_*.py[m
[31m-check_*.py[m
[31m-temp_*.py[m
[31m-*_temp.py[m
[31m-[m
[31m-# OS[m
[31m-.DS_Store[m
[31m-Thumbs.db[m
[31m-[m
[31m-# Secrets[m
[31m-*.pem[m
[31m-*.key[m
[31m-*.crt[m
[31m-secrets/[m
[31m-credentials.json[m
[32m+[m[32mtemp/[m
[32m+[m[32mdata/[m
[32m+[m[32mbackups/[m
[32m+[m[32mcredentials/[m
[32m+[m[32m.env[m
[32m+[m[32m*.secret[m
[32m+[m[32msen_v3.db[m
[32m+[m[32mapp.db[m
[32m+[m[32mforeplay_data.json[m
[32m+[m[32mworker_simple[m
[1mdiff --git a/CORE_START_GUIDE.md b/CORE_START_GUIDE.md[m
[1mdeleted file mode 100644[m
[1mindex 599d33ba..00000000[m
[1m--- a/CORE_START_GUIDE.md[m
[1m+++ /dev/null[m
[36m@@ -1,129 +0,0 @@[m
[31m-# DYT-01 Core - Hướng dẫn Khởi động Production-like (3 Terminal)[m
[31m-[m
[31m-## Mục tiêu[m
[31m-Chạy ổn định 3 thành phần chính:[m
[31m-1. **API** (FastAPI) - nhận task qua HTTP[m
[31m-2. **Worker** (General) - xử lý task ngay (content, echo, shopee, tiktok)[m
[31m-3. **Scheduled Poster** - đăng Facebook đúng giờ theo lịch (chỉ 2 page thật)[m
[31m-[m
[31m-## Cách chạy nhanh nhất (khuyến nghị)[m
[31m-[m
[31m-```powershell[m
[31m-cd E:\DYT_01[m
[31m-[m
[31m-# Mở 3 cửa sổ PowerShell cùng lúc (production-like)[m
[31m-powershell -ExecutionPolicy Bypass -File .\start_core.ps1[m
[31m-[m
[31m-# Hoặc chạy worker ở chế độ drain 1 lần (rất hữu ích khi test/debug)[m
[31m-powershell -ExecutionPolicy Bypass -File .\start_core.ps1 -WorkerOnce[m
[31m-```[m
[31m-[m
[31m-Script sẽ tự động mở:[m
[31m-- Terminal 1: API (http://localhost:8000/docs)[m
[31m-- Terminal 2: Worker (xử lý immediate)[m
[31m-- Terminal 3: Scheduled (FB đúng giờ)[m
[31m-[m
[31m-## Cách chạy thủ công (3 terminal riêng)[m
[31m-[m
[31m-**Terminal 1 (API):**[m
[31m-```powershell[m
[31m-cd E:\DYT_01[m
[31m-powershell -ExecutionPolicy Bypass -File .\start_api.ps1[m
[31m-```[m
[31m-[m
[31m-**Terminal 2 (Worker):**[m
[31m-```powershell[m
[31m-cd E:\DYT_01[m
[31m-powershell -ExecutionPolicy Bypass -File .\start_worker.ps1[m
[31m-# hoặc drain nhanh: python run_worker.py --run-once[m
[31m-```[m
[31m-[m
[31m-**Terminal 3 (Scheduled FB):**[m
[31m-```powershell[m
[31m-cd E:\DYT_01[m
[31m-powershell -ExecutionPolicy Bypass -File .\start_scheduled.ps1[m
[31m-```[m
[31m-[m
[31m-## Các lệnh hay dùng sau khi Core chạy[m
[31m-[m
[31m-```powershell[m
[31m-# Xem lịch 3 ngày (không enqueue)[m
[31m-python schedule_optimized_posts.py --fanpage_key affiliate_fashion_cosmetics --days 3 --dry_run[m
[31m-python schedule_optimized_posts.py --fanpage_key motivational_postcard --days 3 --dry_run[m
[31m-[m
[31m-# Schedule thật 3 ngày (chỉ 2 page thật)[m
[31m-python schedule_optimized_posts.py --fanpage_key affiliate_fashion_cosmetics --days 3[m
[31m-python schedule_optimized_posts.py --fanpage_key motivational_postcard --days 3[m
[31m-[m
[31m-# Test enqueue nhanh[m
[31m-python test_core_e2e_direct.py          # test echo + content[m
[31m-python enqueue_task.py ...              # (nếu có)[m
[31m-[m
[31m-# Xem task + last_error[m
[31m-python query_last_error.py[m
[31m-python check_facebook_status.py[m
[31m-[m
[31m-# Drain một lần (khi không muốn mở terminal worker)[m
[31m-python run_worker.py --run-once[m
[31m-```[m
[31m-[m
[31m-## Yêu cầu trước khi chạy[m
[31m-[m
[31m-1. **Python** phải có trong PATH (khuyến nghị Python 3.11 x64).[m
[31m-2. **facebook_auth.json** ở thư mục gốc (rất quan trọng cho Terminal 3).[m
[31m-   - Chưa có? Chạy: `python save_facebook_auth.py` hoặc `python test_facebook_auth.py`[m
[31m-3. DB (sen_v3.db hoặc ai_os.db) đã được khởi tạo (script tự create table khi cần).[m
[31m-4. Nên chạy trong thư mục `E:\DYT_01` (không phải worktree).[m
[31m-[m
[31m-## Dừng hệ thống[m
[31m-[m
[31m-- Đơn giản nhất: đóng 3 cửa sổ PowerShell.[m
[31m-- Hoặc Ctrl+C trong từng terminal.[m
[31m-[m
[31m-## Lưu ý quan trọng[m
[31m-[m
[31m-- Facebook tasks nên để **Terminal 3 (run_scheduled_posts.py)** xử lý (vì có scheduled_at + nặng).[m
[31m-- Content / echo / shopee nên để **Terminal 2** xử lý (nhanh).[m
[31m-- Muốn test nhanh: dùng `-WorkerOnce` hoặc `python run_worker.py --run-once`.[m
[31m-- Optimizer sẽ tự dùng data COMPLETED nội bộ khi đủ mẫu (>=5 giờ có data).[m
[31m-[m
[31m-## Tích hợp với Confluence (mới)[m
[31m-[m
[31m-Bạn có thể dùng Confluence làm "nơi quản lý nội dung chính" với các macro (Children Display, Table of Contents, Page Properties Report, Include Page...).[m
[31m-[m
[31m-Hệ thống DYT có thể:[m
[31m-[m
[31m-- Đọc nội dung đã "approved" từ Confluence pages (dùng label + Page Properties).[m
[31m-- Tự động đưa vào queue để đăng Facebook theo lịch.[m
[31m-- Hoặc generate nội dung bằng AI rồi push lên Confluence trước khi review.[m
[31m-[m
[31m-**Cách bật nhanh:**[m
[31m-[m
[31m-1. Tạo file `.env` (copy từ .env.example) và điền thông tin Confluence Cloud:[m
[31m-   ```[m
[31m-   CONFLUENCE_BASE_URL=https://xxx.atlassian.net/wiki[m
[31m-   CONFLUENCE_EMAIL=...[m
[31m-   CONFLUENCE_API_TOKEN=...[m
[31m-   CONFLUENCE_SPACE_KEY=...[m
[31m-   ```[m
[31m-[m
[31m-2. Trong Confluence:[m
[31m-   - Tạo trang content.[m
[31m-   - Dùng **Page Properties** macro để set: fanpage-key, scheduled-date, theme.[m
[31m-   - Gắn label `fb-approved` (và sau khi đăng sẽ tự thêm `posted`).[m
[31m-[m
[31m-3. Chạy:[m
[31m-   ```powershell[m
[31m-   python sync_confluence_to_fb_queue.py[m
[31m-   ```[m
[31m-   Script sẽ quét các trang approved và tạo task facebook_autoposter.[m
[31m-[m
[31m-4. Sau đó chạy scheduled poster như bình thường.[m
[31m-[m
[31m-Chi tiết xem code trong `src/confluence_client.py` và `sync_confluence_to_fb_queue.py`.[m
[31m-[m
[31m-Điều này giúp bạn tận dụng tốt các macro Confluence để có dashboard, reuse nội dung, cấu trúc phân cấp, trong khi vẫn dùng được automation đăng FB + tối ưu giờ của DYT.[m
[31m-[m
[31m-Script này được thiết kế để bạn có thể chạy lại bất cứ lúc nào khi muốn mở lại môi trường dev/test/production-like sạch.[m
[31m-[m
[31m-Chúc bạn chạy Core ổn định! 🚀[m
[1mdiff --git a/MIGRATION_GUIDE.md b/MIGRATION_GUIDE.md[m
[1mdeleted file mode 100644[m
[1mindex ab8777e4..00000000[m
[1m--- a/MIGRATION_GUIDE.md[m
[1m+++ /dev/null[m
[36m@@ -1,164 +0,0 @@[m
[31m-# Migration Guide: From Old Scripts to New Worker System (DYT-01 Phase 4+)[m
[31m-[m
[31m-This gu