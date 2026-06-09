# Migration Guide: From Old Scripts to New Worker System (DYT-01 Phase 4+)

This guide helps you migrate from the old messy script-based system (pre-Phase 1) to the clean, modern worker + scheduler architecture.

## 1. Overview of Changes

**Old Way (before rebuild):**
- Many standalone scripts: `auto_facebook_post.py`, `affiliate_worker_fixed.py`, `schedule_optimized_posts.py`, `run_scheduled_posts.py`, `accesstrade_auto_link.py`, etc.
- Direct file I/O (CSV, TXT, JSON for links/posts)
- Hardcoded `facebook_auth.json`, cookies
- Manual running or PowerShell cron-like

**New Way (after Phase 4):**
- Centralized `start.py` (api / worker / scheduler / all)
- `AsyncTaskQueueDB` + `SchedulerWorker`
- `FacebookWorker`, `AffiliateWorker`
- Encrypted credentials in DB (`facebook_accounts`)
- API-driven scheduling (`/schedules`)
- Clean models: `Task`, `ScheduledTask`, `CommissionLog`, `AffiliateLink`

## 2. Step-by-Step Migration

### Step 1: Backup Everything
```powershell
# Backup old data
Copy-Item *.csv, *.txt, *.json, sen_v3.db -Destination .\backup_pre_migration\ -Recurse
```

### Step 2: Run Database Migration (if needed)
```powershell
python start.py init-db
alembic upgrade head
```

This ensures you have the latest tables (`scheduled_tasks`, `facebook_accounts`, `affiliate_links`, etc.).

### Step 3: Migrate AccessTrade / Affiliate Data

We have a helper script:

```powershell
python scripts/migrate_accesstrade.py
```

This script:
- Reads old `accesstrade_campaigns_*.csv` (if present)
- Fetches fresh data from AccessTrade API
- Creates recurring `ScheduledTask` entries (daily fetch)

After running, old CSVs can be archived.

### Step 4: Migrate Facebook Pages / Auth

**Old:** `facebook_auth.json` or cookies in JSON.

**New:** Use the API (admin only):

```bash
curl -X POST http://localhost:8000/facebook/accounts \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "page_id": "YOUR_PAGE_ID",
    "page_name": "My Fanpage",
    "access_token": "EAAB...",
    "app_id": "YOUR_APP_ID",
    "app_secret": "YOUR_APP_SECRET",
    "expires_in_days": 60
  }'
```

The token is encrypted and stored in `facebook_accounts`.

If you had many pages, write a small one-time script to import from old files.

### Step 5: Migrate Existing Schedules / Posts

**Old scheduled posts** (from `schedule_optimized_posts.py` or text files):

- Parse your old post files / DB (if any).
- Use the new API to create `ScheduledTask`:

```bash
curl -X POST http://localhost:8000/schedules \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "task_type": "post_to_page",
    "scheduled_at": "2026-06-10T09:00:00",
    "data": {
      "page_id": "123456",
      "message": "Your migrated post content here...",
      "link": "https://..."
    },
    "priority": 0
  }'
```

For recurring (daily/weekly), create multiple or enhance later.

### Step 6: Stop Using Old Scripts

- Delete or move to `.archive/` the old scripts we cleaned in Phase 4.
- Use only `python start.py ...`

### Step 7: Update Any External Triggers

If you had cron jobs, Task Scheduler, or other tools calling old scripts:

- Replace with calls to the new API (`/schedules`) or direct `start.py scheduler`.
- Or keep a thin wrapper script that calls the API.

### Step 8: Verify

1. Start the system:
   ```powershell
   python start.py api
   python start.py worker --type facebook
   python start.py worker --type affiliate
   python start.py scheduler
   ```

2. Create a test schedule with `scheduled_at` = now + 2 minutes.

3. Watch the Scheduler log: "Enqueued scheduled task ..."

4. Watch the corresponding worker pick it up and execute.

## 3. Common Migration Scenarios

### From old affiliate link files (affiliate_links.txt)

Use the new `POST /affiliate/links` or let the `AffiliateWorker` handle `create_affiliate_link` tasks.

### From manual Facebook posting scripts

All posting should now go through `POST /posts/facebook` or schedules.

### From direct CSV campaign processing

Use `POST /affiliate/campaigns/fetch` + let `AffiliateWorker` process.

## 4. Rollback Plan (if needed)

- Keep the backup folder.
- The old scripts are still in `.archive/` (if you moved them during Phase 0/4).
- Database changes are additive (new tables), so old data is safe.

## 5. After Migration

- Delete old CSV/TXT export files (they are now in DB).
- Update any documentation or team processes.
- Monitor the new Scheduler + Workers for a few days.

## 6. Need Help?

- Check logs from `SchedulerWorker` and individual workers.
- Use `/api/v1/queue/tasks` to see what's in the queue.
- Use `/schedules` to manage future jobs.

**Migration completed?** You are now fully on the new architecture. Welcome to the clean DYT-01 system! 🚀

---

*Last updated: Phase 4 completion*
