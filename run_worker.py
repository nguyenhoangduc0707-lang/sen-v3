import asyncio
import os
from src.orchestrator_async import run_engine
from src.orchestrator import register_worker

from src.workers.echo_worker import EchoWorker
from src.workers.shopee_worker import ShopeeWorker
from src.workers.tiktok_worker import TikTokWorker
from src.workers.content_worker import ContentWorker
from src.workers.facebook_autoposter import FacebookAutoPoster

# Ensure DB tables exist (safe for SQLite)
try:
    from src.db.session import get_engine
    from src.db.models import Base
    Base.metadata.create_all(bind=get_engine())
except Exception as e:
    print(f'[WARN] Could not ensure DB tables: {e}')

register_worker("echo_worker", EchoWorker)
register_worker("shopee_affiliate", ShopeeWorker)
register_worker("tiktok_affiliate", TikTokWorker)
register_worker("content_creator", ContentWorker)
register_worker("facebook_autoposter", FacebookAutoPoster)

print('[Core] Registered workers:', list(__import__('src.orchestrator', fromlist=['registry']).registry.keys()))

def drain_pending_once(max_workers: int = 3, timeout: float = 10.0):
    """Reliable one-shot processor for --run-once or testing."""
    import asyncio
    from concurrent.futures import ThreadPoolExecutor
    from src.orchestrator_async import worker_loop, TaskQueueDB
    from src.orchestrator import load_workers

    load_workers()
    queue = TaskQueueDB()
    executor = ThreadPoolExecutor(max_workers=max_workers)
    stop_event = asyncio.Event()

    async def _drain():
        tasks = [asyncio.create_task(worker_loop(i, queue, executor, 0.2, stop_event)) for i in range(max_workers)]
        # Wait for no pending or timeout
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
    import sys
    if "--run-once" in sys.argv:
        print("[Core] Running one-shot drain of pending tasks...")
        drain_pending_once()
    else:
        asyncio.run(run_engine())
