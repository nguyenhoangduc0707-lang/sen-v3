"""
Automation Engine for cutting down on repetitive tasks.

Supports:
- Automation Templates (pre-built for common workflows)
- No-code Automation Rules (user defined conditions + actions)
- Triggers on task events (created, status change, failed, etc.)
- Actions: route to worker, update status, notify (log/email stub), etc.

No coding required for users - rules defined via JSON or future UI form.
"""

import json
from datetime import datetime
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import sessionmaker

from src.db.session import get_engine
from src.db.models import AutomationRule, AutomationTemplate, AutomationLog, Task
from src.task_queue_db import TaskQueueDB


class AutomationEngine:
    def __init__(self, engine=None):
        self.engine = engine or get_engine()
        self.Session = sessionmaker(bind=self.engine)
        self.task_queue = TaskQueueDB()  # uses get_engine internally

    def get_templates(self, category: Optional[str] = None) -> List[Dict]:
        """Return available automation templates (for 'Start with an automation template')."""
        s = self.Session()
        q = s.query(AutomationTemplate).filter(AutomationTemplate.is_active == True)
        if category:
            q = q.filter(AutomationTemplate.category == category)
        templates = q.all()
        s.close()
        return [
            {
                "id": t.id,
                "name": t.name,
                "description": t.description,
                "category": t.category,
                "trigger": t.trigger,
                "conditions": json.loads(t.conditions) if t.conditions else [],
                "actions": json.loads(t.actions) if t.actions else [],
            }
            for t in templates
        ]

    def create_rule_from_template(self, template_id: int, name: str = None, created_by_id: int = None) -> int:
        """Create a rule by copying a template (no coding needed)."""
        s = self.Session()
        template = s.get(AutomationTemplate, template_id)
        if not template:
            s.close()
            raise ValueError("Template not found")

        rule = AutomationRule(
            name=name or template.name,
            description=template.description,
            trigger=template.trigger,
            conditions=template.conditions,
            actions=template.actions,
            enabled=True,
            created_by_id=created_by_id,
        )
        s.add(rule)
        s.commit()
        rule_id = rule.id
        s.close()
        return rule_id

    def create_rule(self, name: str, trigger: str, conditions: List[Dict], actions: List[Dict], 
                    description: str = None, created_by_id: int = None) -> int:
        """Create custom automation rule (no coding - via API/UI form)."""
        s = self.Session()
        rule = AutomationRule(
            name=name,
            description=description,
            trigger=trigger,
            conditions=json.dumps(conditions),
            actions=json.dumps(actions),
            enabled=True,
            created_by_id=created_by_id,
        )
        s.add(rule)
        s.commit()
        rule_id = rule.id
        s.close()
        return rule_id

    def evaluate_conditions(self, conditions: List[Dict], task: Task) -> bool:
        """Simple condition evaluator. Supports equals, contains, etc."""
        if not conditions:
            return True
        task_dict = {
            "category": task.category,
            "status": task.status,
            "worker_name": task.worker_name,
            "priority": task.priority,
            "payload": json.loads(task.payload) if task.payload else {},
        }
        for cond in conditions:
            field = cond.get("field")
            op = cond.get("op", "equals")
            value = cond.get("value")
            if not field:
                continue
            # Support nested payload.field
            actual = task_dict
            for part in field.split("."):
                if isinstance(actual, dict):
                    actual = actual.get(part)
                else:
                    actual = None
                    break
            if actual is None:
                return False
            if op == "equals" and actual != value:
                return False
            if op == "contains" and value not in str(actual):
                return False
            if op == "not_equals" and actual == value:
                return False
        return True

    def execute_actions(self, actions: List[Dict], task: Task) -> List[str]:
        """Execute actions on the task."""
        results = []
        s = self.Session()
        task = s.merge(task)  # attach to session
        for action in actions:
            action_type = action.get("type")
            if action_type == "set_worker":
                task.worker_name = action.get("value")
                results.append(f"Set worker to {task.worker_name}")
            elif action_type == "set_status":
                task.status = action.get("value")
                results.append(f"Set status to {task.status}")
            elif action_type == "set_priority":
                task.priority = action.get("value", 1)
                results.append(f"Set priority to {task.priority}")
            elif action_type == "notify":
                # Stub for notification - in real would send email/Slack/etc.
                to = action.get("to", "admin")
                msg = f"Notification: Task #{task.id} ({task.category}) - {action.get('message', '')}"
                print(f"[AUTOMATION NOTIFY to {to}]: {msg}")
                results.append(f"Sent notification to {to}")
            elif action_type == "add_tag":
                # Could extend payload
                payload = json.loads(task.payload or "{}")
                tags = payload.get("tags", [])
                tags.append(action.get("value"))
                payload["tags"] = tags
                task.payload = json.dumps(payload)
                results.append(f"Added tag {action.get('value')}")
            # Add more actions as needed: schedule, call API, etc.
        s.commit()
        s.close()
        return results

    def run_for_task(self, task: Task, trigger: str = "task.created") -> List[Dict]:
        """Run matching rules for a task event. Call this after task create/update."""
        s = self.Session()
        rules = s.query(AutomationRule).filter(
            AutomationRule.enabled == True,
            AutomationRule.trigger == trigger
        ).order_by(AutomationRule.priority.asc()).all()

        executed = []
        for rule in rules:
            conditions = json.loads(rule.conditions or "[]")
            if self.evaluate_conditions(conditions, task):
                actions = json.loads(rule.actions or "[]")
                action_results = self.execute_actions(actions, task)
                # Log
                log = AutomationLog(
                    rule_id=rule.id,
                    task_id=task.id,
                    trigger=trigger,
                    status="success",
                    details=json.dumps({"actions": action_results})
                )
                s.add(log)
                # Update rule stats
                rule.last_triggered_at = datetime.utcnow()
                rule.trigger_count = (rule.trigger_count or 0) + 1
                executed.append({
                    "rule_id": rule.id,
                    "rule_name": rule.name,
                    "actions": action_results
                })
        s.commit()
        s.close()
        return executed

    def seed_templates(self):
        """Seed default templates (run once on init or via admin)."""
        s = self.Session()
        if s.query(AutomationTemplate).count() > 0:
            # Still ensure rules exist
            pass
        else:
            templates = [
                {
                    "name": "Auto-route content creation tasks",
                    "description": "Automatically assign new content tasks to the content_creator worker.",
                    "category": "task_routing",
                    "trigger": "task.created",
                    "conditions": [{"field": "category", "op": "equals", "value": "content"}],
                    "actions": [{"type": "set_worker", "value": "content_creator"}]
                },
                {
                    "name": "Notify on failed Facebook post",
                    "description": "Send notification when a facebook_autoposter task fails.",
                    "category": "notification",
                    "trigger": "task.failed",
                    "conditions": [{"field": "worker_name", "op": "equals", "value": "facebook_autoposter"}],
                    "actions": [{"type": "notify", "to": "admin", "message": "FB post failed - check logs"}]
                },
                {
                    "name": "Auto set high priority for affiliate campaigns",
                    "description": "Prioritize tasks related to affiliate campaigns.",
                    "category": "task_routing",
                    "trigger": "task.created",
                    "conditions": [{"field": "category", "op": "contains", "value": "affiliate"}],
                    "actions": [{"type": "set_priority", "value": 3}]
                },
                {
                    "name": "Mark completed tasks as done and notify customer",
                    "description": "Update status and send notification when task finishes successfully.",
                    "category": "notification",
                    "trigger": "task.completed",
                    "conditions": [],
                    "actions": [
                        {"type": "set_status", "value": "COMPLETED"},
                        {"type": "notify", "to": "customer", "message": "Your request has been completed."}
                    ]
                }
            ]

            for t in templates:
                template = AutomationTemplate(
                    name=t["name"],
                    description=t["description"],
                    category=t["category"],
                    trigger=t["trigger"],
                    conditions=json.dumps(t["conditions"]),
                    actions=json.dumps(t["actions"]),
                )
                s.add(template)
            s.commit()
            print("✅ Seeded default automation templates.")

        # Auto-create rules from templates for demo (users can toggle/disable in UI)
        created = 0
        for t in s.query(AutomationTemplate).filter(AutomationTemplate.is_active == True).all():
            existing = s.query(AutomationRule).filter(AutomationRule.name == t.name).first()
            if not existing:
                rule = AutomationRule(
                    name=t.name,
                    description=t.description,
                    trigger=t.trigger,
                    conditions=t.conditions,
                    actions=t.actions,
                    enabled=True,
                )
                s.add(rule)
                created += 1
        if created:
            s.commit()
            print(f"✅ Auto-created {created} demo rules from templates (toggle off in production).")
        s.close()

    def get_rules(self, enabled_only: bool = True) -> List[Dict]:
        """List current automation rules."""
        s = self.Session()
        q = s.query(AutomationRule)
        if enabled_only:
            q = q.filter(AutomationRule.enabled == True)
        rules = q.all()
        s.close()
        return [
            {
                "id": r.id,
                "name": r.name,
                "trigger": r.trigger,
                "conditions": json.loads(r.conditions or "[]"),
                "actions": json.loads(r.actions or "[]"),
                "enabled": r.enabled,
                "trigger_count": r.trigger_count or 0,
            }
            for r in rules
        ]


# Convenience: hook into existing task creation
def apply_automations_on_task_create(task: Task):
    """Call this after creating a task to run automations."""
    engine = AutomationEngine()
    return engine.run_for_task(task, "task.created")


# Example usage in task_queue_db or enqueue:
# after session.commit() in add_task:
#   apply_automations_on_task_create(t)
