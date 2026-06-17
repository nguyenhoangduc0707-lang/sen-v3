import sqlite3
c = sqlite3.connect('sen_v3.db')
cur = c.cursor()
try:
    cur.execute("SELECT id, status, scheduled_at FROM facebook_posts ORDER BY id DESC LIMIT 10")
    rows = cur.fetchall()
    for r in rows:
        print(r)
    if not rows:
        print("NO ROWS IN facebook_posts table")
except Exception as e:
    print("ERROR:", e)

# also list all tables
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
print("TABLES:", cur.fetchall())
c.close()
