"""
Automation API Router
Provides endpoints for templates and no-code rules.
Matches the "Start with an automation template" and "Create your own automation rules" flow.
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.automation import AutomationEngine
from src.auth.jwt import get_current_user_optional
from src.db.models import User

router = APIRouter(prefix="/api/v1/automation", tags=["Automation"])

engine = AutomationEngine()

# Pydantic models for API
class AutomationTemplateResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    category: Optional[str]
    trigger: str
    conditions: List[Dict[str, Any]]
    actions: List[Dict[str, Any]]

class CreateRuleRequest(BaseModel):
    name: str
    trigger: str
    conditions: List[Dict[str, Any]] = []
    actions: List[Dict[str, Any]]
    description: Optional[str] = None
    template_id: Optional[int] = None  # If provided, copy from template

class AutomationRuleResponse(BaseModel):
    id: int
    name: str
    trigger: str
    conditions: List[Dict[str, Any]]
    actions: List[Dict[str, Any]]
    enabled: bool
    trigger_count: int = 0

@router.on_event("startup")
async def seed_on_startup():
    """Auto-seed templates on first run."""
    engine.seed_templates()

@router.get("/templates", response_model=List[AutomationTemplateResponse])
async def list_templates(category: Optional[str] = None, current_user: Optional[User] = Depends(get_current_user_optional)):
    """List automation templates. 'Start with an automation template'."""
    templates = engine.get_templates(category)
    return templates

@router.post("/rules", response_model=AutomationRuleResponse)
async def create_rule(
    req: CreateRuleRequest,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """Create automation rule, optionally from template. No coding needed."""
    if req.template_id:
        rule_id = engine.create_rule_from_template(
            req.template_id, 
            name=req.name, 
            created_by_id=current_user.id if current_user else None
        )
    else:
        rule_id = engine.create_rule(
            name=req.name,
            trigger=req.trigger,
            conditions=req.conditions,
            actions=req.actions,
            description=req.description,
            created_by_id=current_user.id if current_user else None
        )
    # Fetch and return
    rules = engine.get_rules(enabled_only=False)
    for r in rules:
        if r["id"] == rule_id:
            return r
    raise HTTPException(404, "Rule created but not found")

@router.get("/rules", response_model=List[AutomationRuleResponse])
async def list_rules(enabled_only: bool = True, current_user: Optional[User] = Depends(get_current_user_optional)):
    """List active automation rules."""
    return engine.get_rules(enabled_only=enabled_only)

@router.post("/rules/{rule_id}/toggle")
async def toggle_rule(rule_id: int, current_user: Optional[User] = Depends(get_current_user_optional)):
    """Enable/disable a rule."""
    s = engine.Session()
    rule = s.get(AutomationRule, rule_id)  # type: ignore
    if not rule:
        s.close()
        raise HTTPException(404, "Rule not found")
    rule.enabled = not rule.enabled
    s.commit()
    s.close()
    return {"id": rule_id, "enabled": rule.enabled}

@router.post("/seed-templates")
async def seed_templates(current_user: Optional[User] = Depends(get_current_user_optional)):
    """Admin: re-seed default templates."""
    engine.seed_templates()
    return {"status": "seeded"}

# Example: how to hook in task creation (call from task_queue_db.py after commit)
# from src.automation import apply_automations_on_task_create
# apply_automations_on_task_create(new_task)
