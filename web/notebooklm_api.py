from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.notebooklm_service import NotebookLMService

router = APIRouter(prefix="/api/notebooklm", tags=["notebooklm"])
service = NotebookLMService()

class NotebookCreate(BaseModel):
    name: str
    description: str = ""

class Question(BaseModel):
    notebook_id: str
    question: str

class SourceAdd(BaseModel):
    notebook_id: str
    content: str
    name: str = None

@router.post("/notebooks")
async def create_notebook(data: NotebookCreate):
    return await service.create_notebook(data.name, data.description)

@router.get("/notebooks")
async def list_notebooks():
    return await service.list_notebooks()

@router.post("/ask")
async def ask_question(data: Question):
    result = await service.ask_notebook(data.notebook_id, data.question)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result.get("error"))
    return result

@router.post("/sources")
async def add_source(data: SourceAdd):
    return await service.add_source(data.notebook_id, data.content, data.name)