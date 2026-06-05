import os
import sys
from pathlib import Path

os.environ["DATABASE_URL"] = "sqlite:///:memory:"
sys.path.insert(0, str(Path(".").resolve()))

from src.db.models import Base, Task
from src.db.session import get_engine, get_session
from src.task_queue_db import TaskQueueDB


def setup_module():
    Base.metadata.create_all(get_engine())


def test_db_queue_claim_and_complete():
    queue = TaskQueueDB()
    task_id = queue.add_task("video", "video.youtube_dl", {"url": "http://example.com"})

    task = queue.claim_next_task()
    assert task is not None
    assert task.id == task_id
    assert task.status == "RUNNING"

    queue.mark_completed(task.id)

    session = get_session()
    try:
        saved = session.get(Task, task_id)
        assert saved.status == "COMPLETED"
        assert saved.finished_at is not None
    finally:
        session.close()
