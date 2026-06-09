from src.base_worker import BaseWorker
from typing import Any, Dict

class TikTokWorker(BaseWorker):
    description = "TikTok smoke-test worker"
    category = "tiktok"
    version = "1.0"

    def healthcheck(self) -> bool:
        return True

    def run(self, **kwargs) -> Dict[str, Any]:
        payload = kwargs.get("payload", {}) or kwargs
        url = payload.get("url") or kwargs.get("url", "")
        return {
            "status": "ok",
            "summary": "TikTok test OK",
            "data": {
                "likes": 100,
                "url": url,
                "fanpage_key": payload.get("fanpage_key"),
            },
        }
