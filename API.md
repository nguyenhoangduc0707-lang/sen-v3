# DYT-01 API Reference

Base URL: `http://localhost:8000` (or your production domain)

All protected endpoints require:
```
Authorization: Bearer <your_jwt_token>
```

---

## Authentication

### POST /api/v1/auth/login
```json
{
  "username": "admin_system",
  "password": "ChangeMeImmediately123!"
}
```

Response:
```json
{
  "access_token": "...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### POST /api/v1/auth/register
...

### GET /api/v1/auth/me
Returns current user info (including token quota).

---

## Facebook

### POST /facebook/accounts (Admin only)
Add a Facebook page with encrypted token.

### GET /facebook/accounts
List your (or all) Facebook pages.

### POST /posts/facebook
```json
{
  "page_id": "123456789",
  "message": "Hello from DYT-01!",
  "link": "https://example.com",
  "image_url": "https://...",
  "scheduled_at": "2026-06-07T10:00:00"   // optional
}
```

Returns:
```json
{ "task_id": 42, "status": "queued" }   // or "scheduled"
```

---

## Affiliate

### POST /affiliate/campaigns/fetch
Trigger campaign fetch from AccessTrade.

### POST /affiliate/links
Create affiliate tracking link.

### GET /affiliate/commission
Get commission report (with optional date filters).

---

## Scheduler (Phase 3)

### POST /schedules
Create a scheduled task.

Example:
```json
{
  "task_type": "post_to_page",
  "scheduled_at": "2026-06-07T10:00:00",
  "data": {
    "page_id": "123456",
    "message": "Scheduled via API"
  },
  "priority": 1
}
```

### GET /schedules
List schedules (user sees own, admin sees all).

### GET /schedules/{id}
Get one schedule.

### PUT /schedules/{id}
Update a schedule (only if not yet processed).

### DELETE /schedules/{id}
Soft cancel (set `is_active=false`).

### POST /schedules/{id}/pause
Temporarily disable.

### POST /schedules/{id}/resume
Re-enable.

---

## Health & System

- `GET /` → Basic info
- `GET /health` → Health check
- `GET /api/v1/queue/tasks` → Current queue status (protected)

---

**Note**: Full interactive docs available at `/docs` when the API is running.
