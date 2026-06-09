import sqlite3
from datetime import datetime

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

cursor.execute('''
    SELECT id, title, scheduled_at, priority 
    FROM tasks 
    WHERE status = 'SCHEDULED'
    ORDER BY scheduled_at
''')

tasks = cursor.fetchall()

if tasks:
    print('\n📅 SCHEDULED POSTS')
    print('=' * 60)
    for task in tasks:
        scheduled = datetime.fromisoformat(task[2])
        print(f'ID: {task[0]} | Priority: {task[3]}')
        print(f'Time: {scheduled.strftime("%Y-%m-%d %H:%M:%S")}')
        print(f'Title: {task[1]}')
        print('-' * 60)
else:
    print('\n📭 No scheduled posts')

# Thống kê
cursor.execute('''
    SELECT status, COUNT(*) 
    FROM tasks 
    GROUP BY status
''')
stats = cursor.fetchall()

print('\n📊 TASK STATISTICS')
print('=' * 60)
for status, count in stats:
    print(f'{status}: {count}')

conn.close()
