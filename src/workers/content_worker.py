from src.base_worker import BaseWorker
from typing import Any, Dict
from content_creation_agent import create_article

class ContentWorker(BaseWorker):
    description = "Generate affiliate/content using campaign info"
    category = "content"
    version = "2.0"

    def healthcheck(self) -> bool:
        # TODO: check if content_creation_agent / LLM is available
        return True

    def run(self, **kwargs) -> Dict[str, Any]:
        """
        Expects:
        - campaign_info or data in payload
        - theme: "affiliate" (default), "motivational", "banking"
        - fanpage_key or page_url for posting target
        """
        payload = kwargs.get("payload", {}) or kwargs
        campaign_info = payload.get("campaign_info") or kwargs.get("campaign_info")
        theme = payload.get("theme", "affiliate")
        fanpage_key = payload.get("fanpage_key") or payload.get("page") or "affiliate_fashion_cosmetics"

        if not campaign_info and "campaign_id" in payload:
            campaign_info = {
                "name": f"Campaign {payload['campaign_id']}",
                "commission_display": "N/A",
                "description": ""
            }

        if not campaign_info:
            # For non-affiliate themes, still allow generating general content
            campaign_info = {
                "name": payload.get("name", "Cuộc Sống"),
                "commission_display": "",
                "description": payload.get("description", "")
            }

        try:
            content = create_article(campaign_info, theme=theme)
            return {
                "status": "ok",
                "summary": content,
                "data": {
                    "provider": "content_agent",
                    "theme": theme,
                    "fanpage_key": fanpage_key
                }
            }
        except Exception as e:
            return {"status": "error", "summary": f"Content generation failed: {str(e)}"}


# ========== SEN V3 ContentWorker Wrapper for Task Queue ==========
import logging
from typing import Dict, Any
import sqlite3
import os

logger = logging.getLogger(__name__)

def get_content_agent():
    """Robust factory that works with current content_creation_agent.py"""
    try:
        # Try the advanced one first (if it has the class)
        from content_creation_agent import ContentCreationAgent
        return ContentCreationAgent()
    except (ImportError, AttributeError):
        pass

    # Fallback to existing module functions
    try:
        from content_creation_agent import create_article
        class _LegacyAgent:
            async def generate_affiliate_post(self, **kwargs):
                # Adapt to existing create_article
                campaign = {
                    "name": kwargs.get("product_name"),
                    "commission_display": "N/A",
                    "description": ", ".join(kwargs.get("features", []))
                }
                content = create_article(campaign, theme="affiliate")
                return {"status": "ok", "content": content, "model": "legacy"}
            async def generate_content(self, prompt: str, **kwargs):
                return {"status": "ok", "content": prompt[:500] + "... (legacy fallback)", "model": "legacy"}
        return _LegacyAgent()
    except Exception as e:
        logger.warning(f"Could not load any content agent: {e}")
        class _Dummy:
            async def generate_affiliate_post(self, **kwargs):
                return {"status": "error", "summary": "No content agent available (missing LLM keys or import)"}
            async def generate_content(self, **kwargs):
                return {"status": "error", "summary": "No content agent available"}
        return _Dummy()


class ContentWorker:
    """
    Worker wrapper để nhận task từ queue và gọi ContentCreationAgent
    Dùng cho AsyncTaskQueueDB hoặc Redis queue
    SEN V3 Multi-Agent style
    """

    def __init__(self):
        self.agent = get_content_agent()
        self.name = "content_worker"

    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Xử lý task từ queue

        Task format:
        {
            'id': task_id,
            'task_type': 'content',
            'data': {
                'action': 'generate_affiliate_post',
                'product_name': '...',
                'features': [...],
                'affiliate_link': '...',
                ...
            }
        }
        """
        task_id = task.get('id')
        data = task.get('data', {})
        action = data.get('action', 'generate_content')

        logger.info(f"📝 ContentWorker processing task {task_id}: {action}")

        await self._log_to_db(task_id, "started", None)

        try:
            if action == 'generate_affiliate_post':
                # Build campaign dict with all required fields for good prompt
                campaign = {
                    "name": data.get('product_name'),
                    "commission_display": data.get('commission_display', 'hấp dẫn'),
                    "description": ", ".join(data.get('features', [])),
                    "affiliate_link": data.get('affiliate_link')
                }
                # Call the async version directly for best results
                try:
                    from content_creation_agent import create_article_async
                    agent_result = await create_article_async(campaign, theme="affiliate")
                    result = {
                        "status": "ok",
                        "content": agent_result.get("content", ""),
                        "provider": agent_result.get("provider", "groq"),
                        "model": "groq"
                    }
                except Exception as e:
                    # Fallback to legacy
                    result = await self.agent.generate_affiliate_post(
                        product_name=data.get('product_name'),
                        features=data.get('features', []),
                        affiliate_link=data.get('affiliate_link'),
                        target_audience=data.get('target_audience', 'general'),
                        tone=data.get('tone', 'friendly'),
                        task_id=task_id
                    )
            elif action == 'generate_seo_article':
                result = await self.agent.generate_seo_article(
                    keyword=data.get('keyword'),
                    target_length=data.get('target_length', 1000),
                    include_faq=data.get('include_faq', True),
                    task_id=task_id
                )
            elif action == 'generate_facebook_caption':
                result = await self.agent.generate_facebook_caption(
                    product_name=data.get('product_name'),
                    key_benefits=data.get('key_benefits', []),
                    promotion=data.get('promotion'),
                    task_id=task_id
                )
            else:
                # Generic content generation
                result = await self.agent.generate_content(
                    prompt=data.get('prompt'),
                    max_tokens=data.get('max_tokens', 1000),
                    temperature=data.get('temperature', 0.7),
                    task_id=task_id
                )

            if result.get('status') == 'ok':
                await self._log_to_db(task_id, "completed", result)
                logger.info(f"✅ ContentWorker completed task {task_id}")
            else:
                await self._log_to_db(task_id, "failed", result)
                logger.error(f"❌ ContentWorker failed task {task_id}: {result.get('summary')}")

            return result

        except Exception as e:
            logger.error(f"ContentWorker exception for task {task_id}: {e}")
            await self._log_to_db(task_id, "error", {"error": str(e)})
            return {"status": "error", "summary": str(e)}

    async def _log_to_db(self, task_id: int, status: str, result: Dict = None):
        """Ghi log vào execution_logs"""
        try:
            conn = sqlite3.connect('sen_v3.db')  # or app.db
            cursor = conn.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS execution_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    agent_name TEXT,
                    task_id INTEGER,
                    action TEXT,
                    input_summary TEXT,
                    output_summary TEXT,
                    duration_ms INTEGER,
                    success BOOLEAN,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            cursor.execute('''
                INSERT INTO execution_logs (agent_name, task_id, action, output_summary, success)
                VALUES (?, ?, ?, ?, ?)
            ''', ('ContentWorker', task_id, status, str(result)[:500] if result else None, status == 'completed'))

            conn.commit()
            conn.close()
        except Exception as e:
            logger.debug(f"Failed to log to DB: {e}")


# Factory function
_content_worker = None

def get_content_worker() -> ContentWorker:
    global _content_worker
    if _content_worker is None:
        _content_worker = ContentWorker()
    return _content_worker
