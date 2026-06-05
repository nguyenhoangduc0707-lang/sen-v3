import inspect
import logging
import sys
from pathlib import Path

import pytest

# Ensure project root is importable
sys.path.insert(0, str(Path(".").resolve()))

from src.orchestrator import load_workers, registry

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


@pytest.fixture(scope="session")
def loaded_registry():
    """Load workers once per test session and return the registry mapping."""
    count = load_workers()
    logging.info(f"Fixture: discovered {count} workers")
    return registry


def test_registry_not_empty(loaded_registry):
    assert isinstance(loaded_registry, dict)
    assert len(loaded_registry) > 0, "Registry should contain at least one worker"


def test_worker_structure(loaded_registry):
    # pick a sample worker expected to exist
    sample = "video.youtube_dl"
    assert sample in loaded_registry, f"Expected worker '{sample}' in registry; got: {list(loaded_registry.keys())}"

    cls = loaded_registry[sample]
    # class should expose run and healthcheck
    assert hasattr(cls, "run") and callable(getattr(cls, "run"))
    assert hasattr(cls, "healthcheck") and callable(getattr(cls, "healthcheck"))

    # the class should not be abstract (must implement required ABC methods)
    assert not inspect.isabstract(cls), f"Worker class {cls!r} appears abstract; implement required methods"


def test_no_circular_imports(loaded_registry):
    # calling load_workers again should not crash and should be idempotent
    prev = len(loaded_registry)
    new_count = load_workers()
    assert new_count >= prev, "Reloading workers reduced registry size (possible import issue)"
