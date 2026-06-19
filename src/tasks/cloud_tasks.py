import os
import json

# Lazy import GCP client to avoid hard dependency for local dev
try:
    from google.cloud import tasks_v2
    _HAS_TASKS = True
except Exception:
    _HAS_TASKS = False

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
LOCATION = os.getenv("GCP_LOCATION", "asia-southeast1")
QUEUE_NAME = os.getenv("CLOUD_TASKS_QUEUE", "dyt-tasks-queue")
WORKER_URL = os.getenv("WORKER_URL")  # URL của worker service trên Cloud Run

_client = None
_parent = None

def _ensure_client():
    global _client, _parent
    if not _HAS_TASKS:
        raise RuntimeError("google-cloud-tasks not installed in environment")
    if _client is None:
        _client = tasks_v2.CloudTasksClient()
        _parent = _client.queue_path(PROJECT_ID, LOCATION, QUEUE_NAME)


def enqueue_task(payload: dict):
    """Tạo task và gửi vào Cloud Tasks. Trả về task name string."""
    if PROJECT_ID is None or WORKER_URL is None:
        raise RuntimeError("GCP_PROJECT_ID and WORKER_URL must be set to enqueue Cloud Tasks")
    _ensure_client()
    task = {
        "http_request": {
            "http_method": tasks_v2.HttpMethod.POST,
            "url": WORKER_URL,
            "body": json.dumps(payload).encode(),
            "headers": {"Content-Type": "application/json"},
        }
    }
    response = _client.create_task(parent=_parent, task=task)
    return response.name
