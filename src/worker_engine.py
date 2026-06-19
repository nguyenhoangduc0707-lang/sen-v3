from src.workers import WORKER_REGISTRY
import logging

logger = logging.getLogger(__name__)

def run_worker_sync(worker_name: str, payload: dict):
    """Chạy worker đồng bộ với payload"""
    if worker_name not in WORKER_REGISTRY:
        return {"status": "error", "error": f"Worker '{worker_name}' not found"}
    
    try:
        worker_func = WORKER_REGISTRY[worker_name]
        # Nếu payload là dict, truyền vào như kwargs
        if isinstance(payload, dict):
            result = worker_func(**payload)
        else:
            result = worker_func(payload)
        return {"status": "success", "result": result}
    except Exception as e:
        logger.exception(f"Worker {worker_name} failed")
        return {"status": "error", "error": str(e)}
