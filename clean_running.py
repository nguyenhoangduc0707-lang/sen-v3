import sqlite3
conn = sqlite3.connect('sen_v3.db')
cur = conn.cursor()
cur.execute('UPDATE tasks SET status="PENDING", started_at=NULL, last_error=NULL WHERE worker_name="facebook_autoposter" AND status="RUNNING"')
print('Cleaned RUNNING FB tasks:', cur.rowcount)
conn.commit()
cur.close()
conn.close()