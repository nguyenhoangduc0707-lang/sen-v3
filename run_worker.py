import asyncio
import sys
import logging
from concurrent.futures import ThreadPoolExecutor

from src.orchestrator_async import run_engine, worker_loop
from src.task_queue_db import TaskQueueDB
from src.orchestrator import registry, load_workers

# Try to import all workers (skip if not found)
workers_to_register = [
    ("echo_worker", "src.workers.echo_worker.EchoWorker"),
    ("shopee_affiliate", "src.workers.shopee_worker.ShopeeWorker"),
    ("tiktok_affiliate", "src.workers.tiktok_worker.TikTokWorker"),
    ("content_creator", "src.workers.content_worker.ContentWorker"),
    ("facebook_autoposter", "src.workers.facebook_autoposter.FacebookAutoPoster"),
]

# Đăng ký worker nếu import thành công
for name, path in workers_to_register:
    try:
        module_path, class_name = path.rsplit(".", 1)
        module = __import__(module_path, fromlist=[class_name])
        worker_class = getattr(module, class_name)
        registry[name] = worker_class
        print(f"Registered worker: {name}")
    except ImportError as e:
        print(f"Worker '{name}' skipped (import error: {e})")
    except Exception as e:
        print(f"Worker '{name}' failed to register: {e}")

# Ensure DB tables exist
try:
    from src.db.database import Base, engine
    Base.metadata.create_all(bind=engine)
    print("Database tables ensured")
except Exception as e:
    print(f"⚠️ Could not create DB tables: {e}")

print(f"Registered workers: {list(registry.keys())}")

def drain_pending_once(max_workers: int = 3, timeout: float = 10.0):
    """Reliable one-shot processor for --run-once or testing."""
    load_workers()
    queue = TaskQueueDB()
    executor = ThreadPoolExecutor(max_workers=max_workers)
    stop_event = asyncio.Event()

    async def _drain():
        tasks = [asyncio.create_task(worker_loop(i, queue, executor, 0.2, stop_event)) for i in range(max_workers)]
        waited = 0.0
        while waited < timeout:
            try:
                with queue.engine.connect() as conn:
                    from sqlalchemy import text
                    res = conn.execute(text('SELECT COUNT(*) FROM tasks WHERE status = "PENDING"'))
                    if (res.scalar() or 0) == 0:
                        break
            except Exception:
                pass
            await asyncio.sleep(0.2)
            waited += 0.2
        stop_event.set()
        await asyncio.wait(tasks, timeout=2)
        executor.shutdown(wait=True)

    asyncio.run(_drain())

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    if "--run-once" in sys.argv:
        print("[Core] Running one-shot drain of pending tasks...")
        drain_pending_once()
    else:
        print("Starting Worker Engine (continuous mode)...")
        try:
            asyncio.run(run_engine())
        except KeyboardInterrupt:
            print("Worker stopped by user")