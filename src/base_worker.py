from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseWorker(ABC):
    """Abstract base class for all workers.

    Required methods:
    - run(self, **kw) -> Dict[str, Any]
    - healthcheck(self) -> bool
    """

    description: str = ""
    category: str = ""
    version: str = "1.0"

    @abstractmethod
    def run(self, **kw) -> Dict[str, Any]:
        """Execute the task. Return a dict with at least a 'status' key."""
        raise NotImplementedError

    @abstractmethod
    def healthcheck(self) -> bool:
        """Return True when the worker is ready to run tasks."""
        raise NotImplementedError
