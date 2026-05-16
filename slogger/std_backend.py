import sys
import logging
from datetime import datetime
from zoneinfo import ZoneInfo
from contextvars import ContextVar
from contextlib import contextmanager

from .config import DEFAULT_INDENT, DEFAULT_TIMEZONE, SHORT_LEVELS

# Context variable for depth (thread-safe, async-safe)
_log_depth = ContextVar("log_depth", default=0)

# The root slogger logger; callers import this after setup_logging()
logger = logging.getLogger("slogger")

_handlers: list[logging.Handler] = []


class _SloggerFormatter(logging.Formatter):
    def __init__(self, indent=DEFAULT_INDENT, timezone=DEFAULT_TIMEZONE, short_levels=False, level_width=7):
        super().__init__()
        self.indent = indent
        self.timezone = timezone
        self.short_levels = short_levels
        self.level_width = level_width

    def format(self, record: logging.LogRecord) -> str:
        depth = getattr(record, "depth", _log_depth.get())
        indent_str = " " * self.indent * depth

        dt = datetime.fromtimestamp(record.created, tz=self.timezone)
        time_str = dt.strftime("%Y-%m-%dT%H:%M:%S")

        level = record.levelname
        if self.short_levels:
            level = SHORT_LEVELS.get(level, level)

        name = record.name
        msg = record.getMessage()

        return f"{time_str} [{name}] {level:<{self.level_width}} | {indent_str}{msg}"


def setup_logging(
    level="INFO",
    indent=DEFAULT_INDENT,
    timezone=DEFAULT_TIMEZONE,
    file=None,
    short_levels=False,
    flush=False,
    level_width=7,
):
    global _handlers

    root = logging.getLogger()

    # remove only our handlers
    for h in _handlers:
        root.removeHandler(h)
    _handlers.clear()

    if flush:
        root.handlers.clear()

    numeric_level = getattr(logging, level.upper(), logging.INFO)
    root.setLevel(numeric_level)

    formatter = _SloggerFormatter(
        indent=indent, timezone=timezone, short_levels=short_levels, level_width=level_width
    )

    console = logging.StreamHandler(sys.stdout)
    console.setLevel(numeric_level)
    console.setFormatter(formatter)
    root.addHandler(console)
    _handlers.append(console)

    if file:
        add_file_sink(file, level=level, formatter=formatter)

    return logger


def add_file_sink(file, level="INFO", formatter=None, max_bytes=3 * 1024 * 1024, backup_count=3):
    """Add a rotating file sink. Can be called after setup_logging."""
    from logging.handlers import RotatingFileHandler

    global _handlers
    numeric_level = getattr(logging, level.upper(), logging.INFO)

    if formatter is None:
        formatter = _SloggerFormatter()

    handler = RotatingFileHandler(file, maxBytes=max_bytes, backupCount=backup_count)
    handler.setLevel(numeric_level)
    handler.setFormatter(formatter)
    logging.getLogger().addHandler(handler)
    _handlers.append(handler)
    return handler


def log_depth(level, message, depth=0, **kwargs):
    """Log with explicit indentation depth."""
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    extra = {"depth": depth}
    extra.update(kwargs)
    logger.log(numeric_level, message, extra=extra)


def set_depth(depth: int):
    return _log_depth.set(depth)


@contextmanager
def log_indent():
    """Context manager to increase log depth for a block of code.

    with log_indent():
        logger.info("Level 1")

        with log_indent():
            logger.info("Level 2")
    """
    token = _log_depth.set(_log_depth.get() + 1)
    try:
        yield
    finally:
        _log_depth.reset(token)
