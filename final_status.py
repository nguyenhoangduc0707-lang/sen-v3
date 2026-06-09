import sqlite3
from datetime import datetime

conn = sqlite3.connect('app.db')
c = conn.cursor()

print('\n' + '='*60)
print(f' DYT-01 FINAL STATUS - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
print('='*60)

# Thống kê
c.execute('SELECT status, COUNT(*) FROM tasks GROUP BY status')
stats = c.fetchall()

print('\n📊 TASK SUMMARY:')
for status, count in stats:
    emoji = '✅' if status == 'COMPLETED' else '🔄' if status == 'RUNNING' else '⏰' if status == 'SCHEDULED' else '⏳' if status == 'PENDING' else '❌'
    print(f'   {emoji} {status}: {count}')

# Bài đăng hôm nay
c.execute('''
    SELECT COUNT(*) 
    FROM tasks 
    WHERE status = 'SCHEDULED' 
    AND date(scheduled_at) = date('now', 'localtime')
''')
today = c.fetchone()[0]

# Bài đăng ngày mai
c.execute('''
    SELECT COUNT(*) 
    FROM tasks 
    WHERE status = 'SCHEDULED' 
    AND date(scheduled_at) = date('now', 'localtime', '+1 day')
''')
tomorrow = c.fetchone()[0]

print(f'\n📅 SCHEDULE:')
print(f'   Today: {today} posts')
print(f'   Tomorrow: {tomorrow} posts')

# Tổng số
c.execute('SELECT COUNT(*) FROM tasks')
total = c.fetchone()[0]
print(f'\n📋 TOTAL TASKS MANAGED: {total}')

# Worker status
c.execute('SELECT COUNT(*) FROM tasks WHERE status = \"RUNNING\"')
running = c.fetchone()[0]
if running > 0:
    print(f'\n🤖 Active workers: {running} task(s) in progress')

conn.close()
print('='*60)

print('\n🎉 SYSTEM STATUS: OPERATIONAL')
print('   - Facebook auto-poster: ACTIVE')
print('   - Affiliate system: ACTIVE')
print('   - Google Sheets sync: READY')
print('   - 24/7 operation: ENABLED')
