import sys
from pathlib import Path

sys.path.insert(0, str(Path(".").resolve()))

from src.orchestrator import load_workers, registry
from src.orchestrator_async import run_worker_sync


def test_run_worker_sync_expands_payload_kwargs():
    load_workers()
    assert "shopee_worker" in registry

    result = run_worker_sync("shopee_worker", {"url": "https://shopee.vn/item"})

    assert result["status"] == "success"
    assert result["raw_stats"]["url"] == "https://shopee.vn/item"
