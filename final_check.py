import sqlite3
from datetime import datetime

conn = sqlite3.connect('app.db')
c = conn.cursor()

print('\n' + '='*60)
print(f' FINAL SYSTEM STATUS - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
print('='*60)

# Thống kê
c.execute('SELECT status, COUNT(*) FROM tasks GROUP BY status')
stats = c.fetchall()

print('\n📊 TASK STATUS:')
status_icons = {
    'COMPLETED': '✅',
    'RUNNING': '🔄',
    'SCHEDULED': '⏰',
    'PENDING': '⏳',
    'FAILED': '❌'
}
for status, count in stats:
    icon = status_icons.get(status, '📋')
    print(f'   {icon} {status}: {count}')

# Kiểm tra worker
import subprocess
result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq python.exe'], capture_output=True, text=True)
python_count = result.stdout.count('python.exe')
print(f'\n🤖 Python processes: {python_count}')

if python_count >= 2:
    print('   ✅ Workers are running')
else:
    print('   ⚠️ Check: run_facebook_worker.py may not be running')

conn.close()
print('='*60)
