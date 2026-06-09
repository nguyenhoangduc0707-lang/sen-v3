"""DB-backed Task Queue with atomic claim using RETURNING (works on modern SQLite and Postgres).

Provides methods to add, claim, complete, fail tasks and record execution logs and dead-letter moves.
"""

from datetime import datetime
from typing import Any, Dict, Optional
import json

from sqlalchemy import text

from src.db.models import DeadLetter, ExecutionLog, Task, Worker
from src.db.session import get_engine, get_session

MAX_RETRIES_DEFAULT = 3


class TaskQueueDB:
    def __init__(self, engine=None):
        self.engine = engine or get_engine()

    def add_task(
        self,
        category: Optional[str],
        worker_name: str,
        payload: Dict[str, Any],
        priority: str = "normal",
    ) -> int:
        session = get_session()
        try:
            # Serialize payload to JSON string for Text column
            payload_str = json.dumps(payload) if payload else None
            t = Task(
                title=category or f"task-{worker_name}",
                task_type="generic",  # legacy NOT NULL
                category=category,
                worker_name=worker_name,
                payload=payload_str,
                status="PENDING",
                retries=0,
            )
            session.add(t)
            session.commit()
            session.refresh(t)

            # Apply automations (route, notify, update status etc) - no coding for users
            try:
                from src.automation import apply_automations_on_task_create
                apply_automations_on_task_create(t)
            except Exception as auto_err:
                print(f"[Automation] Skipped on task create: {auto_err}")

            return t.id
        finally:
            session.close()

    def claim_next_task(self, priority_preference: Optional[str] = None) -> Optional[Task]:
        """Atomically claim next pending task and return it (or None).

        Uses a RETURNING-based raw SQL to atomically set status=RUNNING and started_at.
        """
        engine = self.engine
        now = datetime.utcnow().isoformat()

        # Dynamic query depending on database engine type (SQLite vs PostgreSQL)
        is_sqlite = engine.dialect.name == "sqlite"
        if is_sqlite:
            sql = text(
                """
                UPDATE tasks
                SET status = 'RUNNING', started_at = :now
                WHERE id = (
                    SELECT id FROM tasks
                    WHERE status = 'PENDING'
                    ORDER BY CASE
                      WHEN json_extract(payload, '$.priority') = 'high' THEN 0
                      ELSE 1
                    END, created_at
                    LIMIT 1
                )
                RETURNING id, worker_name, payload, retries
                """
            )
        else:
            sql = text(
                """
                UPDATE tasks
                SET status = 'RUNNING', started_at = :now
                WHERE id = (
                    SELECT id FROM tasks
                    WHERE status = 'PENDING'
                    ORDER BY CASE
                      WHEN payload->>'priority' = 'high' THEN 0
                      ELSE 1
                    END, created_at
                    LIMIT 1
                )
                RETURNING id, worker_name, payload, retries
                """
            )
        claimed_id = None
        with engine.begin() as conn:
            try:
                res = conn.execute(sql, {"now": now})
                row = res.fetchone()
                if not row:
                    return None
                claimed_id = row[0]
            except Exception:
                # fallback: non-RETURNING DB (older SQLite). Do safe select-then-update in transaction.
                session = get_session()
                try:
                    t = session.query(Task).filter(Task.status == "PENDING").order_by(Task.created_at.asc()).first()
                    if not t:
                        return None
                    t.status = "RUNNING"
                    t.started_at = datetime.utcnow()
                    session.commit()
                    session.refresh(t)
                    return t
                finally:
                    session.close()

        if claimed_id is None:
            return None
        session = get_session()
        try:
            t = session.get(Task, claimed_id)
            if t and isinstance(t.payload, str):
                try:
                    t.payload = json.loads(t.payload)
                except Exception:
                    pass  # keep as string if not valid json
            return t
        finally:
            session.close()

    def mark_completed(self, task_id: int) -> None:
        session = get_session()
        try:
            t = session.get(Task, task_id)
            if not t:
                return
            t.status = "COMPLETED"
            t.finished_at = datetime.utcnow()
            session.commit()
        finally:
            session.close()

    def mark_failed(
        self,
        task_id: int,
        error_message: Optional[str] = None,
        max_retries: int = MAX_RETRIES_DEFAULT,
    ) -> None:
        session = get_session()
        try:
            t = session.get(Task, task_id)
            if not t:
                return
            t.last_error = error_message
            if (t.retries or 0) < max_retries:
                t.retries = (t.retries or 0) + 1
                t.status = "PENDING"
                t.started_at = None
            else:
                # move to dead_letter
                dead = DeadLetter(
                    original_task_id=t.id,
                    category=t.category,
                    worker_name=t.worker_name,
                    payload=t.payload,
                    failure_reason=error_message,
                )
                session.add(dead)
                t.status = "FAILED"
                t.finished_at = datetime.utcnow()
            session.commit()
        finally:
            session.close()

    def update_worker_heartbeat(self, name: str, version: Optional[str] = None) -> None:
        session = get_session()
        try:
            w = session.query(Worker).filter(Worker.name == name).first()
            if not w:
                w = Worker(
                    name=name,
                    version=version or "unknown",
                    last_heartbeat=datetime.utcnow(),
                    status="ACTIVE",
                )
                session.add(w)
            else:
                w.last_heartbeat = datetime.utcnow()
                w.status = "ACTIVE"
                if version:
                    w.version = version
            session.commit()
        finally:
            session.close()

    def log_execution(
        self,
        task_id: Optional[int],
        worker_name: Optional[str],
        level: str,
        message: str,
    ) -> None:
        session = get_session()
        try:
            e = ExecutionLog(
                task_id=task_id,
                worker_name=worker_name,
                log_level=level,
                message=message,
            )
            session.add(e)
            session.commit()
        finally:
            session.close()

    async def claim_task(self, worker_name: str):
        """Alias for compatibility with BaseWorker"""
        return await self.claim_next_task(worker_name)
