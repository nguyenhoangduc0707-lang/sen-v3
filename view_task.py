import sqlite3
import json

conn = sqlite3.connect('sen_v3.db')
cursor = conn.cursor()

task_id = input("Nhập task ID cần xem: ")
cursor.execute('SELECT id, status, worker_name, payload, last_error FROM tasks WHERE id=?', (task_id,))
task = cursor.fetchone()

if task:
    print(f'\n📋 TASK ID: {task[0]}')
    print(f'   Status: {task[1]}')
    print(f'   Worker: {task[2]}')
    if task[3]:
        payload = json.loads(task[3]) if isinstance(task[3], str) else task[3]
        print(f'   Payload: {json.dumps(payload, indent=2, ensure_ascii=False)}')
    if task[4]:
        print(f'   Error: {task[4]}')
else:
    print('Không tìm thấy task')
conn.close()
