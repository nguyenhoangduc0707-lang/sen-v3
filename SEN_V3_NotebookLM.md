# SEN V3 — Tài liệu cập nhật cho NotebookLM
**Ngày cập nhật:** 29/05/2026  
**Trạng thái:** Production-ready (AI thật đang hoạt động)

---

## 1. TỔNG QUAN DỰ ÁN

SEN V3 là hệ thống tự động hóa affiliate marketing chạy trên Windows local.  
Luồng chính: **Accesstrade campaign → AI sinh nội dung → Worker xử lý task → Lưu PostgreSQL**

### Stack kỹ thuật
| Thành phần | Công nghệ |
|---|---|
| API Server | FastAPI + Uvicorn, cổng 8000 |
| Worker Engine | Python asyncio + ThreadPool, 5 loops |
| Database | PostgreSQL 16 |
| Task Queue | Database-based (bảng `tasks`) |
| AI Provider | **Groq API** (llama-3.3-70b-versatile) |
| Fallback AI | Template cố định (không cần API) |

---

## 2. THAY ĐỔI TRONG PHIÊN BÀN NÀY (29/05/2026)

### 2.1 Chuyển AI Provider từ Gemini → Groq

**Trước:**
- Dùng `google-genai` + Gemini 2.0 Flash
- Bị lỗi API key invalid (400 INVALID_ARGUMENT)
- Fallback template 100% task

**Sau:**
- Dùng `groq` SDK + model `llama-3.3-70b-versatile`
- Free tier: **14,400 request/ngày** (dư cho 200 task/ngày)
- Groq thật: **3/3 task ✅**
- Latency: ~800ms–1.5s/request

**File thay đổi:**
```
C:\DYT_01\content_creation_agent.py   ← viết lại hoàn toàn
C:\DYT_01\src\workers\content_worker.py ← nâng cấp async + fix event loop
```

### 2.2 Kiến trúc AI Provider Layer (mới)

```
Worker gọi create_article_async()
    ↓
Kiểm tra Cache (TTL 1 giờ)
    ↓ cache miss
Gọi Groq API (llama-3.3-70b-versatile)
    ↓ lỗi key/quota → _NoRetryError (không retry)
    ↓ lỗi network/timeout → retry 3 lần (exponential backoff)
Fallback Template
    ↓
Cache kết quả (cả fallback)
    ↓
Trả về {"content", "provider", "cached"}
```

### 2.3 Các cải tiến kỹ thuật

| Tính năng | Chi tiết |
|---|---|
| Rate Limit Guard | 25 req/min, sliding window, async lock |
| Retry Decorator | 3 lần, exponential backoff 2s/4s/8s |
| Smart No-Retry | Không retry khi key sai hoặc quota hết |
| Cache Layer | In-memory, TTL 1 giờ, cache cả fallback |
| Async/Sync | `run_async()` cho orchestrator async, `run()` sync cho tương thích cũ |
| Event Loop Fix | `nest_asyncio` + ThreadPoolExecutor để tránh conflict |

### 2.4 Cấu hình môi trường (.env)

```env
GROQ_API_KEY=gsk_...        # ← Key mới, đã hoạt động
DATABASE_URL=postgresql://sen_user:sen_pass@localhost:5432/sen_v3
MAX_CONCURRENT_WORKERS=5    # ← Đã fix lỗi dính liền với GROQ key
```

---

## 3. TRẠNG THÁI TỪNG WORKER

| Worker | Trạng thái | Ghi chú |
|---|---|---|
| `echo_worker` | ✅ Mock hoạt động | Dùng để test pipeline |
| `content_creator` | ✅ **AI thật (Groq)** | Groq 3/3 task |
| `shopee_affiliate` | ⏳ Mock | Chờ tích hợp Shopee API |
| `tiktok_affiliate` | ⏳ Mock | Chờ tích hợp TikTok API |

---

## 4. VẤN ĐỀ CÒN TỒN ĐỌNG

| Vấn đề | Mức độ | Giải pháp đề xuất |
|---|---|---|
| Accesstrade API lỗi 503 | Trung bình | Chờ service phục hồi, thêm circuit breaker |
| Shopee/TikTok worker là mock | Trung bình | Xem hướng đi tiếp theo bên dưới |
| Log rotate lỗi PermissionError | Thấp | Sửa `logging_config.py` |
| Cache in-memory (mất khi restart) | Thấp | Nâng cấp Redis nếu cần scale |
| Frontend React chưa kết nối | Thấp | Phase sau |

---

## 5. HƯỚNG ĐI TIẾP THEO (ĐỀ XUẤT)

### Phase 2A — Tích hợp Accesstrade thật (Tuần 1-2)
**Mục tiêu:** Lấy campaign thật thay vì mock data

```python
# Luồng mục tiêu:
Accesstrade API → lấy danh sách campaign → 
tạo task tự động → content_creator sinh nội dung → 
lưu kết quả vào DB
```

Việc cần làm:
1. Kiểm tra `ACCESS_TRADE_ACCESS_KEY` trong `.env` — key có sẵn
2. Viết `accesstrade_client.py` — gọi API lấy campaign list
3. Viết `campaign_scheduler.py` — tự động tạo task mỗi giờ
4. Test end-to-end với 1 campaign thật

### Phase 2B — Shopee Affiliate Worker (Tuần 2-3)
**Mục tiêu:** Tạo deep link Shopee + nội dung tự động

Việc cần làm:
1. Đăng ký Shopee Affiliate Program → lấy App ID + Secret
2. Viết `shopee_client.py` — generate deep link
3. Kết hợp với `content_creator` — sinh caption cho sản phẩm Shopee
4. Worker `shopee_affiliate` xử lý end-to-end

### Phase 2C — TikTok Content Worker (Tuần 3-4)
**Mục tiêu:** Sinh caption TikTok ngắn (150 từ) cho sản phẩm affiliate

Việc cần làm:
1. Tạo prompt riêng cho TikTok style (ngắn, trendy, hashtag)
2. Worker `tiktok_affiliate` gọi Groq với prompt TikTok
3. Output: caption + hashtag + link affiliate

### Phase 3 — Dashboard & Monitor (Tuần 4-5)
**Mục tiêu:** Quan sát hệ thống không cần xem log thủ công

Việc cần làm:
1. Thêm endpoint `/api/v1/stats` — task count, provider breakdown, error rate
2. Dashboard đơn giản (FastAPI + Jinja2 hoặc kết nối React frontend có sẵn)
3. Alert khi error rate > 20%

### Phase 4 — Tối ưu chi phí (Khi scale)
Khi vượt 200 task/ngày:
- Groq free: 14,400 req/ngày → đủ dùng đến ~500 task/ngày
- Nếu cần hơn: xem xét Gemini Flash ($0.075/1M token) hoặc OpenRouter
- Bật Redis cache để giảm API call khi nhiều campaign trùng lặp

---

## 6. CÁCH KHỞI ĐỘNG HỆ THỐNG

```powershell
# Cửa sổ 1 — API Server
cd C:\DYT_01
venv\Scripts\activate
python run_api.py

# Cửa sổ 2 — Worker Engine
cd C:\DYT_01
venv\Scripts\activate
python run_worker.py

# Cửa sổ 3 — Tạo task test
$body = @{
    category    = "content"
    worker_name = "content_creator"
    payload     = @{
        name        = "Shopee 12.12"
        commission  = 15.0
        description = "Sale cuối năm lớn nhất"
    }
    priority = "normal"
} | ConvertTo-Json -Depth 3
Invoke-RestMethod -Uri http://localhost:8000/api/v1/tasks -Method Post -Body $body -ContentType "application/json"

# Kiểm tra kết quả trong DB
python -c "
import psycopg2
conn = psycopg2.connect('postgresql://sen_user:sen_pass@localhost:5432/sen_v3')
cur = conn.cursor()
cur.execute('SELECT id, status, result FROM tasks ORDER BY id DESC LIMIT 5')
for row in cur.fetchall(): print(row)
"
```

---

## 7. DEPENDENCIES HIỆN TẠI

```
fastapi
uvicorn
sqlalchemy
psycopg2-binary
python-dotenv
groq                  ← MỚI thêm
nest_asyncio          ← MỚI thêm
alembic
python-jose
passlib
```

---

*Tài liệu này dùng để import vào NotebookLM.*  
*Cập nhật tiếp khi hoàn thành Phase 2A (Accesstrade thật).*
