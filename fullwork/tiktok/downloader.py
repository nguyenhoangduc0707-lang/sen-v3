from typing import Any, Dict

from src.base_worker import BaseWorker
from src.orchestrator import register_worker


@register_worker("tiktok.downloader")
class TikTokDownloader(BaseWorker):
    description = "Example TikTok downloader worker"
    category = "tiktok"
    version = "0.1"

    def healthcheck(self) -> bool:
        # Lightweight health check; extend as needed (network, credentials...)
        return True

    def run(self, **kw) -> Dict[str, Any]:
        payload = kw.get("payload") or {}
        url = payload.get("url")
        if not url:
            return {"status": "error", "summary": "missing 'url' in payload"}
        # Placeholder implementation: in real worker, download/process the url
        return {"status": "ok", "summary": f"fetched {url}", "meta": {"size": 12345}}
