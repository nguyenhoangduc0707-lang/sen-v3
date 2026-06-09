# DYT-01 Core - Hướng dẫn Khởi động Production-like (3 Terminal)

## Mục tiêu
Chạy ổn định 3 thành phần chính:
1. **API** (FastAPI) - nhận task qua HTTP
2. **Worker** (General) - xử lý task ngay (content, echo, shopee, tiktok)
3. **Scheduled Poster** - đăng Facebook đúng giờ theo lịch (chỉ 2 page thật)

## Cách chạy nhanh nhất (khuyến nghị)

```powershell
cd E:\DYT_01

# Mở 3 cửa sổ PowerShell cùng lúc (production-like)
powershell -ExecutionPolicy Bypass -File .\start_core.ps1

# Hoặc chạy worker ở chế độ drain 1 lần (rất hữu ích khi test/debug)
powershell -ExecutionPolicy Bypass -File .\start_core.ps1 -WorkerOnce
```

Script sẽ tự động mở:
- Terminal 1: API (http://localhost:8000/docs)
- Terminal 2: Worker (xử lý immediate)
- Terminal 3: Scheduled (FB đúng giờ)

## Cách chạy thủ công (3 terminal riêng)

**Terminal 1 (API):**
```powershell
cd E:\DYT_01
powershell -ExecutionPolicy Bypass -File .\start_api.ps1
```

**Terminal 2 (Worker):**
```powershell
cd E:\DYT_01
powershell -ExecutionPolicy Bypass -File .\start_worker.ps1
# hoặc drain nhanh: python run_worker.py --run-once
```

**Terminal 3 (Scheduled FB):**
```powershell
cd E:\DYT_01
powershell -ExecutionPolicy Bypass -File .\start_scheduled.ps1
```

## Các lệnh hay dùng sau khi Core chạy

```powershell
# Xem lịch 3 ngày (không enqueue)
python schedule_optimized_posts.py --fanpage_key affiliate_fashion_cosmetics --days 3 --dry_run
python schedule_optimized_posts.py --fanpage_key motivational_postcard --days 3 --dry_run

# Schedule thật 3 ngày (chỉ 2 page thật)
python schedule_optimized_posts.py --fanpage_key affiliate_fashion_cosmetics --days 3
python schedule_optimized_posts.py --fanpage_key motivational_postcard --days 3

# Test enqueue nhanh
python test_core_e2e_direct.py          # test echo + content
python enqueue_task.py ...              # (nếu có)

# Xem task + last_error
python query_last_error.py
python check_facebook_status.py

# Drain một lần (khi không muốn mở terminal worker)
python run_worker.py --run-once
```

## Yêu cầu trước khi chạy

1. **Python** phải có trong PATH (khuyến nghị Python 3.11 x64).
2. **facebook_auth.json** ở thư mục gốc (rất quan trọng cho Terminal 3).
   - Chưa có? Chạy: `python save_facebook_auth.py` hoặc `python test_facebook_auth.py`
3. DB (sen_v3.db hoặc ai_os.db) đã được khởi tạo (script tự create table khi cần).
4. Nên chạy trong thư mục `E:\DYT_01` (không phải worktree).

## Dừng hệ thống

- Đơn giản nhất: đóng 3 cửa sổ PowerShell.
- Hoặc Ctrl+C trong từng terminal.

## Lưu ý quan trọng

- Facebook tasks nên để **Terminal 3 (run_scheduled_posts.py)** xử lý (vì có scheduled_at + nặng).
- Content / echo / shopee nên để **Terminal 2** xử lý (nhanh).
- Muốn test nhanh: dùng `-WorkerOnce` hoặc `python run_worker.py --run-once`.
- Optimizer sẽ tự dùng data COMPLETED nội bộ khi đủ mẫu (>=5 giờ có data).

## Tích hợp với Confluence (mới)

Bạn có thể dùng Confluence làm "nơi quản lý nội dung chính" với các macro (Children Display, Table of Contents, Page Properties Report, Include Page...).

Hệ thống DYT có thể:

- Đọc nội dung đã "approved" từ Confluence pages (dùng label + Page Properties).
- Tự động đưa vào queue để đăng Facebook theo lịch.
- Hoặc generate nội dung bằng AI rồi push lên Confluence trước khi review.

**Cách bật nhanh:**

1. Tạo file `.env` (copy từ .env.example) và điền thông tin Confluence Cloud:
   ```
   CONFLUENCE_BASE_URL=https://xxx.atlassian.net/wiki
   CONFLUENCE_EMAIL=...
   CONFLUENCE_API_TOKEN=...
   CONFLUENCE_SPACE_KEY=...
   ```

2. Trong Confluence:
   - Tạo trang content.
   - Dùng **Page Properties** macro để set: fanpage-key, scheduled-date, theme.
   - Gắn label `fb-approved` (và sau khi đăng sẽ tự thêm `posted`).

3. Chạy:
   ```powershell
   python sync_confluence_to_fb_queue.py
   ```
   Script sẽ quét các trang approved và tạo task facebook_autoposter.

4. Sau đó chạy scheduled poster như bình thường.

Chi tiết xem code trong `src/confluence_client.py` và `sync_confluence_to_fb_queue.py`.

Điều này giúp bạn tận dụng tốt các macro Confluence để có dashboard, reuse nội dung, cấu trúc phân cấp, trong khi vẫn dùng được automation đăng FB + tối ưu giờ của DYT.

Script này được thiết kế để bạn có thể chạy lại bất cứ lúc nào khi muốn mở lại môi trường dev/test/production-like sạch.

Chúc bạn chạy Core ổn định! 🚀
