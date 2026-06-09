import sqlite3
from datetime import datetime

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

print('\n' + '='*60)
print(' DYT-01 SYSTEM DASHBOARD')
print(f' {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
print('='*60)

# Thống kê
cursor.execute('SELECT status, COUNT(*) FROM tasks GROUP BY status')
stats = dict(cursor.fetchall())

print(f'\n📊 TASK STATISTICS')
print(f'   ✅ COMPLETED: {stats.get("COMPLETED", 0)}')
print(f'   🔄 RUNNING:   {stats.get("RUNNING", 0)}')
print(f'   ⏰ SCHEDULED: {stats.get("SCHEDULED", 0)}')
print(f'   ⏳ PENDING:   {stats.get("PENDING", 0)}')
print(f'   📋 TOTAL:     {sum(stats.values())}')

# Bài đăng hôm nay
cursor.execute('''
    SELECT COUNT(*) 
    FROM tasks 
    WHERE status = "SCHEDULED" 
    AND date(scheduled_at) = date("now", "localtime")
''')
today_count = cursor.fetchone()[0]
print(f'\n📅 TODAY\'S SCHEDULED: {today_count} posts')

# Bài đăng tiếp theo
cursor.execute('''
    SELECT id, datetime(scheduled_at, "localtime"), title 
    FROM tasks 
    WHERE status = "SCHEDULED" 
    AND datetime(scheduled_at) > datetime("now", "localtime")
    ORDER BY scheduled_at 
    LIMIT 1
''')
next_post = cursor.fetchone()
if next_post:
    print(f'\n⏰ NEXT POST: #{next_post[0]} at {next_post[1]}')
    print(f'   {next_post[2]}')

# Tasks đang chạy
cursor.execute('''
    SELECT id, title, worker_name 
    FROM tasks 
    WHERE status IN ("RUNNING", "PENDING")
    ORDER BY priority DESC
    LIMIT 5
''')
active = cursor.fetchall()
if active:
    print(f'\n🔄 ACTIVE TASKS:')
    for task in active:
        print(f'   #{task[0]} | {task[2]} | {task[1][:40]}')

conn.close()
print('\n' + '='*60)
