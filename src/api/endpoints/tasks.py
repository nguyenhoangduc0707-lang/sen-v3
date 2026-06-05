from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from src.db.session import get_db
from src.models.task import Task

router = APIRouter()

@router.get("/tasks")
async def get_tasks(db: Session = Depends(get_db)):
    """Get all tasks"""
    try:
        tasks = db.query(Task).all()
        return {"tasks": [{"id": t.id, "title": t.title, "status": t.status} for t in tasks]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/tasks")
async def create_task(task_data: Dict[str, Any], db: Session = Depends(get_db)):
    """Create a new task"""
    try:
        new_task = Task(**task_data)
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        return {"id": new_task.id, "message": "Task created successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
