import sqlite3
conn = sqlite3.connect("sen_v3.db")
cur = conn.cursor()

# Reset RUNNING back to PENDING (from interrupted runs)
cur.execute('UPDATE tasks SET status="PENDING", started_at=NULL WHERE worker_name="facebook_autoposter" AND status="RUNNING"')
print("Reset RUNNING to PENDING:", cur.rowcount)

# Reset recent errored PENDING that had browser closed (so they can retry)
cur.execute('UPDATE tasks SET status="PENDING", started_at=NULL, last_error=NULL WHERE worker_name="facebook_autoposter" AND status="PENDING" AND last_error LIKE "%closed%"')
print("Reset closed-error PENDING:", cur.rowcount)

conn.commit()
cur.close()
conn.close()
print("Stuck tasks cleaned. Ready for python run_scheduled_posts.py --once")