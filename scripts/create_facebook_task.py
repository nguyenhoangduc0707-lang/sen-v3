"""
Create one Facebook post task (real post when dry_run=False).
Usage: python scripts/create_facebook_task.py
"""
from src.task_queue_db import TaskQueueDB
from datetime import datetime

q = TaskQueueDB()

payload = {
    "content": "[DYT_01 TEST] Auto post at " + datetime.utcnow().isoformat(),
    "fanpage_key": "default",
    "dry_run": False,
}

tid = q.add_task(category="facebook", worker_name="facebook_autoposter", payload=payload, priority="normal")
print("Created facebook task id=", tid)
