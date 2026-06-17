import sqlite3
import time
import sys
import os
sys.path.insert(0, os.getcwd())

from src.workers.content_worker import ContentWorker
import asyncio

def get_pending_task():
    conn = sqlite3.connect('sen_v3.db')
    cursor = conn.cursor()
    
    # Lấy task PENDING
    cursor.execute("""
        SELECT id, title, description, task_type, payload
        FROM tasks 
        WHERE status = 'PENDING'
        ORDER BY id
        LIMIT 1
    """)
    task = cursor.fetchone()
    conn.close()
    return task

def process_task(task):
    if not task:
        return None
    
    task_id, title, description, task_type, payload = task
    print(f"📋 Đang xử lý task {task_id}: {title}")
    
    # Cập nhật status
    conn = sqlite3.connect('sen_v3.db')
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tasks 
        SET status = 'PROCESSING', 
            worker_name = 'content_creator',
            started_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (task_id,))
    conn.commit()
    conn.close()
    
    # Gọi worker
    w = ContentWorker()
    result = asyncio.run(w.process_task({
        'id': task_id,
        'data': {
            'action': 'generate_content',
            'prompt': title
        }
    }))
    
    # Cập nhật kết quả
    conn = sqlite3.connect('sen_v3.db')
    cursor = conn.cursor()
    if result.get('status') == 'ok':
        cursor.execute("""
            UPDATE tasks 
            SET status = 'COMPLETED',
                completed_at = CURRENT_TIMESTAMP,
                last_error = NULL
            WHERE id = ?
        """, (task_id,))
    else:
        cursor.execute("""
            UPDATE tasks 
            SET status = 'FAILED',
                last_error = ?
            WHERE id = ?
        """, (result.get('summary', 'Unknown error'), task_id))
    conn.commit()
    conn.close()
    
    print(f"✅ Task {task_id} done: {result.get('status')}")
    return result

if __name__ == "__main__":
    print("🔄 WORKER SIMPLE LOOP")
    print("Lấy task từ database và xử lý")
    while True:
        task = get_pending_task()
        if task:
            process_task(task)
        else:
            print(".", end="", flush=True)
            time.sleep(5)
