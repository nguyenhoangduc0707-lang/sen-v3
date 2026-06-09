"""
Process all pending tasks once. Useful for testing the core.
Usage: python process_pending.py
"""
import asyncio
from concurrent.futures import ThreadPoolExecutor
import sys

# Import run_worker to trigger all registrations (important!)
import run_worker

from src.orchestrator_async import worker_loop, TaskQueueDB
from src.orchestrator import load_workers

async def main():
    print("Loading workers...")
    load_workers()
    queue = TaskQueueDB()
    executor = ThreadPoolExecutor(max_workers=3)
    stop_event = asyncio.Event()

    # Run a few workers for a short time to drain pending
    print("Processing pending tasks...")
    tasks = [
        asyncio.create_task(worker_loop(i, queue, executor, 0.1, stop_event))
        for i in range(2)
    ]

    # Wait up to 10 seconds or until no more pending
    for _ in range(100):
        try:
            with queue.engine.connect() as conn:
                from sqlalchemy import text
                res = conn.execute(text('SELECT COUNT(*) FROM tasks WHERE status = \"PENDING\"'))
                pending = res.scalar() or 0
            if pending == 0:
                print("No more pending tasks.")
                break
        except:
            pass
        await asyncio.sleep(0.1)

    stop_event.set()
    await asyncio.wait(tasks, timeout=2)
    executor.shutdown(wait=True)
    print("Done processing.")

if __name__ == "__main__":
    asyncio.run(main())
