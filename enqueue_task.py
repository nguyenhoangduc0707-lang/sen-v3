"""
Helper script to enqueue a task for the core worker engine.
Supports multi-fanpage themes.

Usage examples:
  # Affiliate fashion page
  python enqueue_task.py content_creator '{"campaign_info": {"name": "BST Denim", "commission_display": "15%"}, "theme": "affiliate", "fanpage_key": "affiliate_fashion_cosmetics"}'

  # Motivational page
  python enqueue_task.py content_creator '{"name": "Bài viết động lực", "description": "Về tình yêu bản thân", "theme": "motivational", "fanpage_key": "motivational_postcard"}'

  # Facebook specific
  python enqueue_task.py facebook_autoposter '{"content": "Nội dung bài đăng", "fanpage_key": "affiliate_fashion_cosmetics"}'
"""
import sys
import json
from src.task_queue_db import TaskQueueDB

def main():
    if len(sys.argv) < 2:
        print("Usage: python enqueue_task.py <worker_name> [json_payload]")
        print("See file header for multi-theme / multi-fanpage examples.")
        sys.exit(1)

    worker_name = sys.argv[1]
    payload = {}
    if len(sys.argv) > 2:
        try:
            payload = json.loads(sys.argv[2])
        except Exception as e:
            print("Invalid JSON payload:", e)
            sys.exit(1)

    # Default theme and fanpage for convenience
    if "theme" not in payload and worker_name in ["content_creator", "shopee_affiliate"]:
        payload["theme"] = "affiliate"
    if "fanpage_key" not in payload:
        if payload.get("theme") == "motivational":
            payload["fanpage_key"] = "motivational_postcard"
        elif payload.get("theme") == "banking":
            payload["fanpage_key"] = "banking_finance"
        else:
            payload["fanpage_key"] = "affiliate_fashion_cosmetics"

    q = TaskQueueDB()
    task_id = q.add_task(category="manual", worker_name=worker_name, payload=payload)
    print(f"Enqueued task #{task_id} for worker '{worker_name}'")
    print(f"Payload: {payload}")
    print("Run worker: python run_worker.py  or  python process_pending.py")

if __name__ == "__main__":
    main()
