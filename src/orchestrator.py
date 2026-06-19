import logging
from typing import Dict, Any, List

logger = logging.getLogger("Orchestrator")
registry: Dict[str, Any] = {}

def register_worker(name: str, worker_class):
    registry[name] = worker_class
    logger.info(f"[Worker] Registered: {name}")

def load_workers() -> List:
    """Load all registered workers"""
    return list(registry.values())

# ==================== WORKER REGISTRY HELPERS ====================
def get_worker(name: str):
    """Trả về worker class từ registry."""
    try:
        from src.workers import WORKER_REGISTRY
        return WORKER_REGISTRY.get(name)
    except ImportError:
        # Fallback: thử import từ registry cũ
        try:
            from src.orchestrator import registry
            return registry.get(name)
        except:
            return None

def register_worker(name: str, worker_class):
    """Đăng ký worker vào registry."""
    try:
        from src.workers import WORKER_REGISTRY
        WORKER_REGISTRY[name] = worker_class
        return True
    except:
        return False
