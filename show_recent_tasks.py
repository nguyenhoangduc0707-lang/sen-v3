import sqlite3
from datetime import datetime

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

cursor.execute('''
    SELECT id, title, task_type, status, worker_name, 
           datetime(created_at, 'localtime') as created
    FROM tasks 
    ORDER BY id DESC 
    LIMIT 10
''')

print('\n📋 RECENT TASKS')
print('=' * 80)
for row in cursor.fetchall():
    print(f'#{row[0]} | {row[3]} | {row[4]}')
    print(f'   {row[1][:50]} ({row[2]})')
    print(f'   Created: {row[5]}')
    print('-' * 80)

conn.close()
