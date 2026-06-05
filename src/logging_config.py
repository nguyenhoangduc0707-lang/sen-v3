import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

import structlog

from .config import settings

def configure_logging(level: str | None = None, log_name: str = "system"):
    valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
    actual_level = settings.LOG_LEVEL
    actual_log_name = log_name

    if level:
        if level.upper() in valid_levels:
            actual_level = level
        else:
            actual_log_name = level.split(".")[-1]

    lvl = actual_level
    # Configure standard logging
    root = logging.getLogger()
    root.setLevel(getattr(logging, lvl.upper(), logging.INFO))

    if not any(isinstance(handler, logging.StreamHandler) for handler in root.handlers):
        ch = logging.StreamHandler()
        ch.setLevel(getattr(logging, lvl.upper(), logging.INFO))
        ch.setFormatter(logging.Formatter("%(message)s"))
        root.addHandler(ch)

    # File handler - rotate daily. If the log file is locked, keep console logging alive.
    try:
        if not any(isinstance(handler, TimedRotatingFileHandler) for handler in root.handlers):
            log_file = Path("logs") / f"{actual_log_name}.log"
            log_file.parent.mkdir(parents=True, exist_ok=True)
            fh = TimedRotatingFileHandler(log_file, when="midnight", backupCount=30, encoding="utf-8")
            fh.setLevel(getattr(logging, lvl.upper(), logging.INFO))
            fh.setFormatter(logging.Formatter("%(message)s"))
            root.addHandler(fh)
    except OSError:
        pass

    # Configure structlog for structured output
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="%Y-%m-%dT%H:%M:%SZ", utc=True),
            structlog.stdlib.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    return structlog.get_logger()
