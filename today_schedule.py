import sqlite3
from datetime import datetime

conn = sqlite3.connect('app.db')
c = conn.cursor()

print(f'\n📅 TODAY\'S SCHEDULE - {datetime.now().strftime("%Y-%m-%d")}')
print('='*50)

c.execute('''
    SELECT id, time(scheduled_at, 'localtime'), title 
    FROM tasks 
    WHERE status = 'SCHEDULED' 
    AND date(scheduled_at) = date('now', 'localtime')
    ORDER BY scheduled_at
''')

tasks = c.fetchall()

if tasks:
    for task in tasks:
        print(f'   {task[1]} - #{task[0]}: {task[2][:40]}')
    print(f'\n📊 Total posts today: {len(tasks)}')
else:
    print('   No posts scheduled for today')

# Thống kê ngày mai
c.execute('''
    SELECT COUNT(*) 
    FROM tasks 
    WHERE status = 'SCHEDULED' 
    AND date(scheduled_at) = date('now', 'localtime', '+1 day')
''')
tomorrow = c.fetchone()[0]
print(f'📅 Tomorrow: {tomorrow} posts scheduled')

conn.close()
