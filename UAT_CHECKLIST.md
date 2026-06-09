# UAT_CHECKLIST.md - DYT-01 User Acceptance Testing

## Pre-test Setup
- [ ] Copy .env.example → .env và điền thông tin
- [ ] Chạy `python start.py init-db` tạo database
- [ ] Chạy `alembic upgrade head` (nếu cần)
- [ ] Thêm Facebook page vào bảng facebook_accounts (qua API hoặc script)
- [ ] Thêm AccessTrade API key vào .env (nếu test affiliate thật)

## Test 1: API Health
- [ ] `curl http://localhost:8000/health` → returns 200 + "status": "healthy"
- [ ] `curl http://localhost:8000/metrics` → returns metrics

## Test 2: Authentication
- [ ] Login với admin: `POST /api/v1/auth/login` (username: admin_system, password: ChangeMeImmediately123!) → nhận token
- [ ] Access protected endpoint với token (ví dụ GET /schedules) → thành công 200
- [ ] Note: The actual endpoint is under /api/v1/auth (not /auth)

## Test 3: Facebook Worker
- [ ] Start worker: `python start.py worker --type facebook`
- [ ] Tạo post task: `POST /posts/facebook`
- [ ] Kiểm tra task được xử lý: `GET /posts/facebook/status/{id}` (hoặc kiểm tra log worker)

## Test 4: Affiliate Worker
- [ ] Start worker: `python start.py worker --type affiliate`
- [ ] Fetch campaigns: `GET /affiliate/campaigns`
- [ ] Tạo affiliate link: `POST /affiliate/links`

## Test 5: Scheduler Worker
- [ ] Start scheduler: `python start.py scheduler`
- [ ] Tạo schedule: `POST /schedules` (scheduled_at = now + 2 minutes)
- [ ] Chờ 2 phút → kiểm tra task được enqueue (xem log scheduler)
- [ ] Kiểm tra `scheduled_tasks.is_processed = True` (qua GET /schedules)

## Test 6: Docker Compose
- [ ] `docker-compose up -d`
- [ ] `docker-compose ps` → tất cả services đều healthy
- [ ] Truy cập API: `curl localhost:8000/health`

## Post-test
- [ ] Export kết quả test
- [ ] Log bugs phát hiện (nếu có)
- [ ] Quyết định: APPROVE / REJECT
