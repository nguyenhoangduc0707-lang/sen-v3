import sqlite3
from datetime import datetime

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

# Xem 10 bài sắp đăng nhất
cursor.execute('''
    SELECT id, title, datetime(scheduled_at, "localtime") as scheduled_time, priority
    FROM tasks 
    WHERE status = 'SCHEDULED'
    ORDER BY scheduled_at
    LIMIT 10
''')

print('\n📅 UPCOMING SCHEDULED POSTS')
print('=' * 70)
for task in cursor.fetchall():
    print(f'#{task[0]} | {task[2]} | Priority: {task[3]}')
    print(f'   {task[1][:50]}')
    print('-' * 70)

# Xem 5 bài đã hoàn thành gần đây
cursor.execute('''
    SELECT id, title, datetime(completed_at, "localtime") as completed_time
    FROM tasks 
    WHERE status = 'COMPLETED'
    ORDER BY completed_at DESC
    LIMIT 5
''')

print('\n✅ RECENTLY COMPLETED POSTS')
print('=' * 70)
for task in cursor.fetchall():
    print(f'#{task[0]} | {task[2]}')
    print(f'   {task[1][:50]}')
    print('-' * 70)

conn.close()
