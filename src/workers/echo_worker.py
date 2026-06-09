from src.base_worker import BaseWorker
from typing import Any, Dict

class EchoWorker(BaseWorker):
    description = "Simple echo worker for testing the queue"
    category = "test"
    version = "1.0"

    def healthcheck(self) -> bool:
        return True

    def run(self, **kwargs) -> Dict[str, Any]:
        return {"status": "ok", "summary": f"Echo: {kwargs}"}
