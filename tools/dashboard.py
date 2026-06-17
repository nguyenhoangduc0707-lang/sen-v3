import sqlite3
import time
import os
from datetime import datetime

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_dashboard():
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    
    clear_screen()
    print('=' * 70)
    print(f' DYT-01 AUTOMATION DASHBOARD - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print('=' * 70)
    
    # Thống kê tổng quan
    cursor.execute('SELECT status, COUNT(*) FROM tasks GROUP BY status')
    stats = dict(cursor.fetchall())
    
    print(f'\n📊 TASK OVERVIEW')
    print(f'   ✅ COMPLETED: {stats.get("COMPLETED", 0)}')
    print(f'   🔄 RUNNING:   {stats.get("RUNNING", 0)}')
    print(f'   ⏰ SCHEDULED: {stats.get("SCHEDULED", 0)}')
    print(f'   ⏳ PENDING:   {stats.get("PENDING", 0)}')
    print(f'   ❌ FAILED:    {stats.get("FAILED", 0)}')
    
    # Tasks hôm nay
    cursor.execute('''
        SELECT id, title, scheduled_at, priority
        FROM tasks 
        WHERE status = 'SCHEDULED' 
        AND date(scheduled_at) = date('now')
        ORDER BY scheduled_at
    ''')
    today_tasks = cursor.fetchall()
    
    print(f'\n📅 TODAY\'S SCHEDULE ({len(today_tasks)} posts)')
    if today_tasks:
        for task in today_tasks:
            time_str = task[2][11:16] if task[2] else 'Pending'
            print(f'   {time_str} | #{task[0]} | {task[1][:35]}')
    else:
        print('   No posts scheduled for today')
    
    # Workers status
    cursor.execute('''
        SELECT worker_name, COUNT(*) 
        FROM tasks 
        WHERE status = 'RUNNING'
        GROUP BY worker_name
    ''')
    workers = cursor.fetchall()
    
    print(f'\n🤖 ACTIVE WORKERS')
    if workers:
        for worker, count in workers:
            print(f'   {worker}: {count} task(s)')
    else:
        print('   No active workers')
    
    conn.close()

try:
    while True:
        show_dashboard()
        time.sleep(5)
except KeyboardInterrupt:
    print('\n👋 Dashboard closed')
