import sqlite3
from datetime import datetime

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

print('\n' + '='*60)
print(f' DYT-01 DETAILED REPORT - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
print('='*60)

# 1. Thống kê theo giờ
cursor.execute('''
    SELECT time(scheduled_at, 'localtime'), COUNT(*) 
    FROM tasks 
    WHERE status='SCHEDULED' 
    GROUP BY time(scheduled_at, 'localtime')
    ORDER BY scheduled_at
''')
print('\n📅 SCHEDULE DISTRIBUTION:')
for hour, count in cursor.fetchall():
    bar = '█' * (count // 5) if count > 0 else '░'
    print(f'   {hour[:5]} | {bar:10} {count} posts')

# 2. Tổng số
cursor.execute('SELECT COUNT(*) FROM tasks WHERE status="SCHEDULED"')
total = cursor.fetchone()[0]
print(f'\n📊 TOTAL SCHEDULED POSTS: {total}')

# 3. Bài đăng hôm nay
cursor.execute('''
    SELECT COUNT(*) 
    FROM tasks 
    WHERE status='SCHEDULED' 
    AND date(scheduled_at) = date('now', 'localtime')
''')
today = cursor.fetchone()[0]
print(f'📅 Today: {today} posts')

# 4. Bài đăng ngày mai
cursor.execute('''
    SELECT COUNT(*) 
    FROM tasks 
    WHERE status='SCHEDULED' 
    AND date(scheduled_at) = date('now', 'localtime', '+1 day')
''')
tomorrow = cursor.fetchone()[0]
print(f'📅 Tomorrow: {tomorrow} posts')

conn.close()
print('='*60)
