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
