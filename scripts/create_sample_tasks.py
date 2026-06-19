"""
Create sample tasks for testing workers locally.
Usage: python scripts\create_sample_tasks.py
This script ensures DB tables exist and inserts one sample task per worker name.
"""
import time
from src.task_queue_db import TaskQueueDB

# Ensure DB tables are present via the existing DB init in run_worker or elsewhere.
try:
    from src.db.database import Base, engine
    Base.metadata.create_all(bind=engine)
except Exception:
    # If DB initialization isn't available, continue and let TaskQueueDB handle engine creation
    pass

queue = TaskQueueDB()

workers = [
    "echo_worker",
    "shopee_affiliate",
    "tiktok_affiliate",
    "content_creator",
    "facebook_autoposter",
]

for w in workers:
    # Per-worker sample payloads: provide realistic payload for facebook_autoposter
    base = {"sample": True, "created_at": time.time(), "worker": w}
    if w == "facebook_autoposter":
        payload = {
            "content": "[SAMPLE] This is a test post created by create_sample_tasks.py",
            "media_path": None,
            "media_type": None,
            "is_personal": False,
            "dry_run": True,  # instruct worker to not perform real posting if supported
            **base,
        }
    else:
        payload = base

    try:
        tid = queue.add_task(category="sample", worker_name=w, payload=payload, priority="normal")
        print(f"Created task id={tid} for worker={w}")
    except Exception as e:
        print(f"Failed to create task for {w}: {e}")
