from src.orchestrator import register_worker


class TikTokWorker:
    description = "TikTok smoke-test worker"
    category = "tiktok"
    version = "1.0"

    def healthcheck(self):
        return True

    def run(self, url="", **kwargs):
        return {
            "status": "success",
            "summary": "TikTok test OK",
            "raw_stats": {"likes": 100, "url": url},
        }
