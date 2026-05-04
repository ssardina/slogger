# slogger_loguru.py

import sys

from loguru import logger

from contextvars import ContextVar
from datetime import datetime
from zoneinfo import ZoneInfo


# Context variable for depth (thread-safe, async-safe)
_log_depth = ContextVar("log_depth", default=0)

DEFAULT_INDENT = 2
DEFAULT_TIMEZONE = ZoneInfo("Australia/Melbourne")

SHORT_LEVELS = {
    "WARNING": "WARN",
    "ERROR": "ERR",
    "CRITICAL": "CRIT",
    "DEBUG": "DEBG",
}

_sink_ids = []


def setup_logging(
    level="INFO",
    indent=DEFAULT_INDENT,
    timezone=DEFAULT_TIMEZONE,
    colorize=True,
    file=None,
    short_levels=False,
    force=False
):
    global _sink_ids

    # remove only our sinks
    for sid in _sink_ids:
        logger.remove(sid)
    _sink_ids.clear()

    if force:
        # remove handlers added by other libraries
        logger.remove()
        

    def formatter(record):
        depth = record["extra"].get("depth", _log_depth.get())
        indent_str = " " * indent * depth

        # timezone-aware time
        dt = datetime.fromtimestamp(record["time"].timestamp(), tz=timezone)
        time_str = dt.strftime("%Y-%m-%dT%H:%M:%S")

        level = record["level"].name
        if short_levels:
            level = SHORT_LEVELS.get(level, level)
        name = record["name"]
        msg = record["message"]

        if colorize:
            return (
                f"<green>{time_str}</green> "
                f"<level>{level:<7}</level> | "
                f"[<cyan>{name}</cyan>] - "
                f"{indent_str}<level>{msg}</level>\n"
            )
        else:
            return f"{time_str} [{name}] {level:<7} | {indent_str}{msg}\n"

    sid = logger.add(
        sys.stdout,
        level=level,
        format=formatter,
        colorize=colorize,
    )
    _sink_ids.append(sid)

    if file:
        sid = logger.add(
            file,
            level=level,
            format=formatter,
            colorize=False,
            rotation="3 MB",
            retention=3,
        )
        _sink_ids.append(sid)

    return logger


"""Helper function to log with depth (indentation). Usage:

log_with_depth("INFO", "Hello", depth=2)
"""


def log_depth(level, message, depth=0, **kwargs):
    logger.bind(depth=depth).log(level, message, **kwargs)



"""Context manager to increase log depth for a block of code.

with log_indent():
    logger.info("Level 1")

    with log_indent():
        logger.info("Level 2")
"""
from contextlib import contextmanager
@contextmanager
def log_indent():
    token = _log_depth.set(_log_depth.get() + 1)
    try:
        yield
    finally:
        _log_depth.reset(token)



def set_depth(depth: int):
    return _log_depth.set(depth)
