import sqlite3, json
conn = sqlite3.connect('sen_v3.db')
conn.row_factory = sqlite3.Row
cur = conn.cursor()
cur.execute('SELECT id, status, last_error, payload FROM tasks WHERE worker_name="facebook_autoposter" ORDER BY id DESC LIMIT 8')
print('Recent FB tasks after clean:')
for r in cur.fetchall():
    p = r['payload']
    sched = '?'
    fp = '?'
    if p:
        try:
            pj = json.loads(p) if isinstance(p, str) else p
            sched = pj.get('scheduled_at', '?')
            fp = pj.get('fanpage_key', '?')
        except: pass
    err = (r['last_error'] or '')[:60]
    print(f"#{r['id']} | {r['status']:9} | {fp:28} | sched={sched} | err={err}")
cur.close()
conn.close()