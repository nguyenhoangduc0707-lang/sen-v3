from src.base_worker import BaseWorker
from src.orchestrator import register_worker


@register_worker("video.youtube_dl")
class Youtube_dlWorker(BaseWorker):
    """Example youtube downloader worker (minimal implementation)."""

    description = "YouTube downloader example"
    category = "video"
    version = "0.1"

    def healthcheck(self) -> bool:
        # simple healthcheck; extend to check network, dependencies, credentials
        return True

    def run(self, **kwargs):
        # TODO: Implement real download logic
        return {"status": "success", "message": "Worker youtube_dl works!"}
