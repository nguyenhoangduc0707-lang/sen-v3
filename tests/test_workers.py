import sys
from pathlib import Path

# Ensure project root is importable when tests run from repo root
sys.path.insert(0, str(Path('.').resolve()))

from src.workers import echo_worker, shopee_worker, tiktok_worker, content_worker, facebook_autoposter


def test_echo_worker_runs_and_returns_success():
    res = echo_worker.run({"a": 1})
    assert isinstance(res, dict)
    assert res.get("status") == "success"


def test_shopee_worker_runs_and_returns_success():
    res = shopee_worker.run({"product": "x"})
    assert isinstance(res, dict)
    assert res.get("status") == "success"


def test_tiktok_worker_runs_and_returns_success():
    res = tiktok_worker.run({"video": "x"})
    assert isinstance(res, dict)
    assert res.get("status") == "success"


def test_content_worker_runs_and_returns_success():
    res = content_worker.run({"title": "t"})
    assert isinstance(res, dict)
    assert res.get("status") == "success"


def test_facebook_autoposter_wrapper_exists_and_returns_dict_on_empty_payload():
    # Calling with empty payload should not raise; original implementation returns error dict when content missing.
    res = facebook_autoposter.run({})
    assert isinstance(res, dict)
    assert "status" in res
