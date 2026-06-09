import sqlite3
conn = sqlite3.connect('sen_v3.db')
cur = conn.cursor()
cur.execute('UPDATE tasks SET status="PENDING", last_error=NULL, started_at=NULL WHERE worker_name="facebook_autoposter" AND last_error LIKE "%not found%"')
print('Reset not-found tasks:', cur.rowcount)
conn.commit()
cur.close()
conn.close()