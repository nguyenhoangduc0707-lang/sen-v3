import sqlite3
conn = sqlite3.connect('sen_v3.db')
cur = conn.cursor()
cur.execute('UPDATE tasks SET status="PENDING", last_error=NULL, started_at=NULL WHERE worker_name="facebook_autoposter" AND (status IN ("FAILED","RUNNING") OR last_error LIKE "%not found%" OR last_error LIKE "%closed%")')
print('Reset problematic FB tasks:', cur.rowcount)
conn.commit()
cur.close()
conn.close()
print('Done. Now run_scheduled_posts.py --once should work better.')