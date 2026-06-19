from fastapi import APIRouter, Request, HTTPException
import json
import logging

from src.orchestrator import get_worker
from src.db.cloud_sql import SessionLocal
from src.db.models import Task

router = APIRouter(prefix="/worker", tags=["worker"])
logger = logging.getLogger(__name__)

@router.post("/run")
async def run_worker_task(request: Request):
    data = await request.json()
    task_id = data.get("task_id")
    worker_name = data.get("worker_name")
    payload = data.get("payload", {})

    if not worker_name:
        raise HTTPException(status_code=400, detail="Missing worker_name")

    worker_class = get_worker(worker_name)
    if not worker_class:
        raise HTTPException(status_code=404, detail=f"Worker {worker_name} not found")

    worker = worker_class()
    try:
        result = worker.run(payload)
        # Cập nhật trạng thái task trong DB
        db = SessionLocal()
        try:
            if task_id is not None:
                task = db.query(Task).filter(Task.id == task_id).first()
                if task:
                    task.status = "COMPLETED"
                    task.result = json.dumps(result)
                    db.add(task)
                    db.commit()
        finally:
            db.close()
        return {"status": "success", "result": result}
    except Exception as e:
        logger.exception("Worker execution failed")
        db = SessionLocal()
        try:
            if task_id is not None:
                task = db.query(Task).filter(Task.id == task_id).first()
                if task:
                    task.status = "FAILED"
                    task.last_error = str(e)
                    db.add(task)
                    db.commit()
        finally:
            db.close()
        raise HTTPException(status_code=500, detail=str(e))
