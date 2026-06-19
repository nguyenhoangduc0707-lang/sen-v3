"""Insert a sample task into the local SQLite task queue.

This script is intentionally side-effect free on import so pytest can safely
scan the repository. Run it directly when you want to seed a local task:

    python scripts/inject_test.py
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from pathlib import Path


DB_PATH = Path(__file__).resolve().parents[1] / "sen_v3.db"


def get_columns(cursor: sqlite3.Cursor, table_name: str) -> set[str]:
    cursor.execute(f"PRAGMA table_info({table_name})")
    return {row[1] for row in cursor.fetchall()}


def insert_sample_task(db_path: Path = DB_PATH) -> int:
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        columns = get_columns(cursor, "tasks")

        if {"title", "task_type", "worker_name", "status", "payload"}.issubset(columns):
            payload = {
                "url": "https://tiktok.com/test",
                "source": "scripts/inject_test.py",
            }
            cursor.execute(
                """
                INSERT INTO tasks (
                    title, task_type, worker_name, status, priority, payload, created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    "Sample TikTok task",
                    "tiktok_worker",
                    "tiktok_worker",
                    "PENDING",
                    1,
                    json.dumps(payload, ensure_ascii=False),
                    datetime.utcnow().isoformat(),
                ),
            )
        elif {"user_id", "worker", "url", "status"}.issubset(columns):
            cursor.execute(
                """
                INSERT INTO tasks (user_id, worker, url, status)
                VALUES (?, ?, ?, ?)
                """,
                (1, "tiktok_worker", "https://tiktok.com/test", "pending"),
            )
        else:
            raise RuntimeError(
                "Unsupported tasks schema. Found columns: "
                + ", ".join(sorted(columns))
            )

        conn.commit()
        return int(cursor.lastrowid)


def main() -> None:
    task_id = insert_sample_task()
    print(f"Inserted sample task #{task_id} into {DB_PATH}")


if __name__ == "__main__":
    main()
