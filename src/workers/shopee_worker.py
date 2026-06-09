from src.base_worker import BaseWorker
from typing import Any, Dict
from content_creation_agent import create_article

class ShopeeWorker(BaseWorker):
    description = "Generate Shopee affiliate content"
    category = "shopee"
    version = "2.0"

    def healthcheck(self) -> bool:
        return True

    def run(self, **kwargs) -> Dict[str, Any]:
        """
        New core style: prefer campaign_info or url passed in payload.
        campaign_id support kept for compatibility but no longer does direct old DB.
        """
        campaign_info = kwargs.get("campaign_info") or (kwargs.get("payload") or {}).get("campaign_info")
        url = kwargs.get("url") or (kwargs.get("payload") or {}).get("url")

        if not campaign_info:
            if url:
                campaign_info = {
                    "name": "Sản phẩm Shopee",
                    "commission_display": "10%",
                    "description": "",
                    "url": url
                }
            else:
                # Minimal fallback
                campaign_info = {
                    "name": kwargs.get("name", "Shopee Product"),
                    "commission_display": "10%",
                    "description": "",
                    "url": url or ""
                }

        try:
            content = create_article(campaign_info)
            return {
                "status": "ok",
                "summary": content,
                "data": {
                    "url": campaign_info.get("url"),
                    "provider": "groq"
                }
            }
        except Exception as e:
            return {"status": "error", "summary": f"Content generation failed: {str(e)}"}
