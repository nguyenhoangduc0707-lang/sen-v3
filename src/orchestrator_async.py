from src.orchestrator import load_workers
"""Async orchestrator: polls DB for tasks and runs workers concurrently.

Uses asyncio.to_thread to run synchronous worker code in thread pool.
"""

import asyncio
import signal
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict

from src.logging_config import configure_logging
from src.orchestrator import registry
# load_workers khÃ´ng cÃ³, cÃ³ thá»ƒ Ä‘á»‹nh nghÄ©a hoáº·c bá» qua
from src.task_queue_db import TaskQueueDB

logger = configure_logging(log_name="worker")

MAX_RETRIES = 3


def run_worker_sync(worker_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """Run a registered worker synchronously. Returns result dict."""
    cls = registry.get(worker_name)
    if not cls:
        return {"status": "error", "summary": f"Worker '{worker_name}' not found"}
    inst = cls()
    try:
        if not getattr(inst, "healthcheck", lambda: True)():
            return {"status": "error", "summary": "healthcheck failed"}
        if isinstance(payload, dict):
            try:
                return inst.run(**payload)
            except TypeError:
                return inst.run(payload=payload)
        return inst.run(payload=payload)
    except Exception as e:
        return {"status": "error", "summary": str(e)}


async def worker_loop(
    worker_id: int,
    queue: TaskQueueDB,
    executor: ThreadPoolExecutor,
    poll_interval: float,
    stop_event: asyncio.Event,
):

    logger.info("worker.loop.start", worker_id=worker_id)
    while not stop_event.is_set():
        # claim next task
        task = await asyncio.to_thread(queue.claim_next_task)
        if not task:
            await asyncio.sleep(poll_interval)
            continue

        task_id = int(task.id)
        worker_name = task.worker_name
        payload = task.payload or {}

        logger.info("task.claimed", worker_name=worker_name, task_id=task_id)
        await asyncio.to_thread(queue.update_worker_heartbeat, worker_name)

        # run worker in thread pool
        try:
            result = await asyncio.to_thread(run_worker_sync, worker_name, payload)
        except Exception as e:
            # unexpected exception
            await asyncio.to_thread(queue.mark_failed, task_id, str(e), MAX_RETRIES)
            await asyncio.to_thread(
                queue.log_execution,
                task_id,
                worker_name,
                "ERROR",
                f"Worker exception: {e}",
            )
            logger.error("task.exception", worker_name=worker_name, task_id=task_id, error=str(e))
            continue

        # write execution log
        await asyncio.to_thread(queue.log_execution, task_id, worker_name, "INFO", f"Result: {result}")

        status = (result or {}).get("status", "").lower()
        if status in ("ok", "success"):
            await asyncio.to_thread(queue.mark_completed, task_id)
            logger.info(
                "task.completed",
                worker_name=worker_name,
                task_id=task_id,
                result=result,
            )
        else:
            err = (result or {}).get("summary") or (result or {}).get("error") or "unknown error"
            await asyncio.to_thread(queue.mark_failed, task_id, str(err), MAX_RETRIES)
            logger.warning("task.failed", worker_name=worker_name, task_id=task_id, error=err)

    logger.info("worker.loop.stopped", worker_id=worker_id)


async def run_engine(max_workers: int = 5, poll_interval: float = 1.0, run_once: bool = False):
    load_workers()
    queue = TaskQueueDB()
    n_workers = max_workers
    executor = ThreadPoolExecutor(max_workers=max_workers)
    stop_event = asyncio.Event()
    loop = asyncio.get_running_loop()

    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, stop_event.set)
        except (NotImplementedError, RuntimeError, ValueError):
            pass

    tasks = [asyncio.create_task(worker_loop(i, queue, executor, poll_interval, stop_event)) for i in range(n_workers)]

    if run_once:
        # run a short period then stop
        await asyncio.sleep(poll_interval * 2)
        stop_event.set()

    await asyncio.wait(tasks)
    executor.shutdown(wait=True)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--max-workers", type=int, default=5)
    parser.add_argument("--poll-interval", type=float, default=1.0)
    parser.add_argument("--run-once", action="store_true")
    args = parser.parse_args()
    asyncio.run(run_engine(args.max_workers, args.poll_interval, args.run_once))
