import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest.mock import patch

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.db.models import Base, DeadLetter, ExecutionLog, Task, Worker
from src.task_queue_db import TaskQueueDB


@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    engine.dispose()


@pytest.fixture
def queue(db_session):
    with patch("src.task_queue_db.get_engine", return_value=db_session.bind):
        with patch("src.task_queue_db.get_session", return_value=db_session):
            yield TaskQueueDB()


def test_add_task(queue, db_session):
    tid = queue.add_task("category1", "worker_a", {"key": "value"}, "high")
    task = db_session.get(Task, tid)
    assert task.category == "category1"
    assert task.worker_name == "worker_a"
    assert task.payload == {"key": "value"}
    assert task.status == "PENDING"


def test_claim_next_task_returns_task(queue, db_session):
    queue.add_task(None, "worker", {}, "normal")
    task = queue.claim_next_task()
    assert task is not None
    assert task.status == "RUNNING"
    assert task.started_at is not None


def test_claim_next_task_no_pending(queue):
    task = queue.claim_next_task()
    assert task is None


def test_mark_completed(queue, db_session):
    tid = queue.add_task(None, "w", {})
    queue.mark_completed(tid)
    task = db_session.get(Task, tid)
    assert task.status == "COMPLETED"
    assert task.finished_at is not None


def test_mark_failed_below_max_retries(queue, db_session):
    tid = queue.add_task(None, "w", {})
    queue.mark_failed(tid, "loi tam thoi", max_retries=3)
    task = db_session.get(Task, tid)
    assert task.retries == 1
    assert task.status == "PENDING"
    assert task.started_at is None


def test_mark_failed_exceed_retries(queue, db_session):
    tid = queue.add_task(None, "w", {})
    task = db_session.get(Task, tid)
    task.retries = 2
    db_session.commit()
    queue.mark_failed(tid, "loi cuoi", max_retries=2)
    # Sau khi gọi mark_failed, task bị expired, cần lấy lại từ session
    db_session.expire_all()
    task = db_session.get(Task, tid)
    assert task.status == "FAILED"
    assert task.finished_at is not None
    dead = db_session.query(DeadLetter).filter(DeadLetter.original_task_id == tid).first()
    assert dead is not None


def test_update_worker_heartbeat_new(queue, db_session):
    queue.update_worker_heartbeat("worker_new", "1.0")
    w = db_session.query(Worker).filter(Worker.name == "worker_new").first()
    assert w.version == "1.0"
    assert w.status == "ACTIVE"
    assert w.last_heartbeat is not None


def test_update_worker_heartbeat_existing(queue, db_session):
    w = Worker(name="worker_old", version="0.9", last_heartbeat=None, status="INACTIVE")
    db_session.add(w)
    db_session.commit()
    queue.update_worker_heartbeat("worker_old", "2.0")
    db_session.expire_all()  # Làm mới session
    w = db_session.query(Worker).filter(Worker.name == "worker_old").first()
    assert w.version == "2.0"
    assert w.status == "ACTIVE"
    assert w.last_heartbeat is not None


def test_log_execution(queue, db_session):
    tid = queue.add_task(None, "w", {})
    queue.log_execution(tid, "w", "INFO", "test message")
    log = db_session.query(ExecutionLog).filter(ExecutionLog.task_id == tid).first()
    assert log.log_level == "INFO"
    assert log.message == "test message"
