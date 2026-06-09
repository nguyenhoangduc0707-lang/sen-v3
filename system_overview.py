import sqlite3
from datetime import datetime

conn = sqlite3.connect('app.db')
c = conn.cursor()

print('\n' + '='*60)
print(f' DYT-01 SYSTEM OVERVIEW - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
print('='*60)

# Thống kê theo task type
c.execute('SELECT task_type, status, COUNT(*) FROM tasks GROUP BY task_type, status')
print('\n📊 TASK TYPES:')
current_type = None
for task_type, status, count in c.fetchall():
    if task_type != current_type:
        print(f'\n   {task_type}:')
        current_type = task_type
    print(f'      {status}: {count}')

# Tổng số
c.execute('SELECT COUNT(*) FROM tasks')
total = c.fetchone()[0]
print(f'\n📋 TOTAL TASKS: {total}')

conn.close()
