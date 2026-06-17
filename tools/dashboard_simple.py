import sqlite3
import time
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_dashboard():
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    
    clear_screen()
    print('=' * 60)
    print(' DYT-01 DASHBOARD - GOOGLE SHEETS INTEGRATION')
    print('=' * 60)
    
    # Thống kê
    cursor.execute('SELECT status, COUNT(*) FROM tasks GROUP BY status')
    stats = dict(cursor.fetchall())
    
    print(f'\n📊 TASKS OVERVIEW')
    print(f'   ✅ COMPLETED: {stats.get("COMPLETED", 0)}')
    print(f'   🔄 RUNNING:   {stats.get("RUNNING", 0)}')
    print(f'   ⏰ SCHEDULED: {stats.get("SCHEDULED", 0)}')
    print(f'   ⏳ PENDING:   {stats.get("PENDING", 0)}')
    
    # Lấy 5 tasks gần nhất
    cursor.execute('''
        SELECT id, title, status, datetime(scheduled_at, "localtime") as scheduled
        FROM tasks 
        WHERE status = "SCHEDULED"
        ORDER BY scheduled_at
        LIMIT 5
    ''')
    
    tasks = cursor.fetchall()
    if tasks:
        print(f'\n📅 NEXT 5 SCHEDULED POSTS')
        for task in tasks:
            print(f'   #{task[0]} | {task[3] or "No schedule"} | {task[1][:35]}')
    
    conn.close()

try:
    while True:
        show_dashboard()
        time.sleep(5)
except KeyboardInterrupt:
    print('\n👋 Dashboard closed')
