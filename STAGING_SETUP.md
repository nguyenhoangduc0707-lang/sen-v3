# STAGING_SETUP.md

## Mục đích
Staging environment để test trước khi deploy production.

## Yêu cầu
- Docker và Docker Compose
- Git
- 2GB RAM, 10GB disk

## Các bước setup

### 1. Clone và checkout staging branch
```bash
git clone <repo-url> dyt-staging
cd dyt-staging
git checkout staging
```

### 2. Tạo .env file
```bash
cp .env.example .env
# Edit .env với thông tin staging
# - DATABASE_URL=postgresql://...
# - DEBUG=true
# - LOG_LEVEL=DEBUG
```

### 3. Start với Docker Compose
```bash
docker-compose up -d
```

### 4. Initialize database
```bash
docker-compose exec api python start.py init-db
```

### 5. Add test Facebook page (via API)
```bash
# Hoặc dùng script
python scripts/add_test_facebook_page.py
```

### 6. Chạy UAT test
```bash
python scripts/uat_test.py --env staging
```

### 7. Xem logs nếu có lỗi
```bash
docker-compose logs -f api
docker-compose logs -f worker-facebook
docker-compose logs -f scheduler
```

### Rollback staging
```bash
docker-compose down -v  # Xóa database
git checkout main
# Setup lại từ đầu
```
