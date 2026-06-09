import sqlite3
from datetime import datetime, timedelta
import time

print('⏰ Watching for tasks due in next 5 minutes...')
print('Press Ctrl+C to stop\n')

last_count = 0
try:
    while True:
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()
        now = datetime.now()
        soon = now + timedelta(minutes=5)
        
        cursor.execute('''
            SELECT id, title, scheduled_at 
            FROM tasks 
            WHERE status = 'SCHEDULED' 
            AND datetime(scheduled_at) BETWEEN datetime(?) AND datetime(?)
        ''', (now.isoformat(), soon.isoformat()))
        
        tasks = cursor.fetchall()
        
        if tasks and len(tasks) != last_count:
            print(f'\n[{now.strftime("%H:%M:%S")}] ⏰ {len(tasks)} task(s) due soon:')
            for task in tasks:
                scheduled = datetime.fromisoformat(task[2])
                print(f'   #{task[0]} at {scheduled.strftime("%H:%M")}: {task[1][:30]}')
            last_count = len(tasks)
        
        conn.close()
        time.sleep(2)
except KeyboardInterrupt:
    print('\n👋 Stopped watching')
