# -*- coding: utf-8 -*-
import sqlite3
import json

conn = sqlite3.connect('sen_v3.db')
cur = conn.cursor()

# Check if payload column exists
cur.execute("PRAGMA table_info(tasks)")
cols = [row[1] for row in cur.fetchall()]
has_payload = 'payload' in cols

if has_payload:
    cur.execute("""
        SELECT id, payload FROM tasks 
        WHERE worker_name = 'facebook_autoposter' AND status = 'PENDING'
    """)
else:
    cur.execute("""
        SELECT id FROM tasks 
        WHERE (worker_name = 'facebook_autoposter' OR worker_name IS NULL) 
        AND status = 'PENDING'
    """)

to_clean = []
for row in cur.fetchall():
    tid = row[0]
    if has_payload:
        pl = row[1]
        try:
            p = json.loads(pl) if pl else {}
            if not p.get('fanpage_key'):
                to_clean.append(tid)
        except:
            to_clean.append(tid)
    else:
        to_clean.append(tid)

print(f'Found {len(to_clean)} legacy tasks to clean')
for tid in to_clean:
    cur.execute("UPDATE tasks SET status='FAILED', last_error='legacy cleaned after auth success' WHERE id=?", (tid,))

conn.commit()
print('Legacy FB tasks cleaned.')
conn.close()
