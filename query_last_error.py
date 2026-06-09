#!/usr/bin/env python
"""
Query last_error cho facebook_autoposter tasks.
Chạy từ E:\DYT_01 :
    python query_last_error.py
"""
import json
import os
import sqlite3
from datetime import datetime

print("=" * 75)
print("QUERY LAST_ERROR - FACEBOOK AUTOPOSTER")
print("=" * 75)

candidates = ["ai_os.db", "sen_v3.db"]
db_file = None
for c in candidates:
    if os.path.exists(c):
        db_file = c
        break

if not db_file:
    print("❌ Không tìm thấy DB (ai_os.db hoặc sen_v3.db)")
    exit(1)

print(f"\n📁 DB: {db_file}")
print(f"⏰ Local now: {datetime.now()}\n")

conn = sqlite3.connect(db_file)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

cur.execute('SELECT id, status, last_error, payload FROM tasks WHERE worker_name="facebook_autoposter" ORDER BY id DESC LIMIT 20')

print("ID   | STATUS    | FANPAGE                      | SCHEDULED_AT          | LAST_ERROR")
print("-" * 115)

for r in cur.fetchall():
    p = r["payload"]
    fp = sched = "?"
    if p:
        try:
            pj = json.loads(p) if isinstance(p, str) else p
            fp = pj.get("fanpage_key", "?")
            sched = pj.get("scheduled_at", "?")
        except:
            pass
    le = (r["last_error"] or "").strip()[:65]
    print(f"{r['id']:4} | {r['status']:9} | {fp:28} | {sched:20} | {le}")

print("\n--- THỐNG KÊ ---")
cur.execute('SELECT status, COUNT(*) as c FROM tasks WHERE worker_name="facebook_autoposter" GROUP BY status')
for row in cur.fetchall():
    print(f"  {row['status']}: {row['c']}")

cur.close()
conn.close()
print("\nGợi ý: python run_scheduled_posts.py --once")
print("=" * 75)