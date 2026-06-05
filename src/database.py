import sqlite3, json, logging
from pathlib import Path
DB = Path("sen_v3.db")
logger = logging.getLogger("Database")

def save_task_result(user_id, worker, url, result):
    try:
        conn = sqlite3.connect(DB)
        conn.execute(
            "INSERT INTO tasks (user_id,worker,url,status,result_summary,raw_stats,revenue,finished_at) VALUES (?,?,?,?,?,?,?,datetime('now'))",
            (user_id, worker, url,
             result.get("status","unknown"),
             json.dumps(result.get("summary","")),
             json.dumps(result.get("raw_stats",{})),
             result.get("raw_stats",{}).get("revenue",0))
        )
        conn.commit()
        conn.close()
        logger.info(f"[DB] Saved: {worker} user={user_id}")
    except Exception as e:
        logger.error(f"[DB] Error: {e}")