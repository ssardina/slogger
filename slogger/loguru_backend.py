import sys
from datetime import datetime

from loguru import logger

from contextvars import ContextVar
from contextlib import contextmanager

from .config import DEFAULT_INDENT, DEFAULT_TIMEZONE, SHORT_LEVELS

# Context variable for depth (thread-safe, async-safe)
_log_depth = ContextVar("log_depth", default=0)


_sink_ids = []
_current_formatter = None


def make_formatter(
    indent=DEFAULT_INDENT, timezone=DEFAULT_TIMEZONE, colorize=True, short_levels=False, level_width=7
):
    """Return a loguru format function configured with the given options."""

    def formatter(record):
        depth = record["extra"].get("depth", _log_depth.get())
        indent_str = " " * indent * depth

        dt = datetime.fromtimestamp(record["time"].timestamp(), tz=timezone)
        time_str = dt.strftime("%Y-%m-%dT%H:%M:%S")

        level = record["level"].name
        if short_levels:
            level = SHORT_LEVELS.get(level, level)
        name = record["name"]
        # escape the braces in the message to prevent loguru from trying to format them
        msg = record["message"].replace("{", "{{").replace("}", "}}")

        if colorize:
            return (
                f"<green>{time_str}</green> "
                f"<level>{level:<{level_width}}</level> | "
                f"[<cyan>{name}</cyan>] - "
                f"{indent_str}<level>{msg}</level>\n"
            )
        else:
            return f"{time_str} [{name}] {level:<{level_width}} | {indent_str}{msg}\n"

    return formatter


def setup_logging(
    level="INFO",
    indent=DEFAULT_INDENT,
    timezone=DEFAULT_TIMEZONE,
    colorize=True,
    file=None,
    short_levels=False,
    flush=False
):
    global _sink_ids, _current_formatter

    # remove only our sinks
    for sid in _sink_ids:
        logger.remove(sid)
    _sink_ids.clear()

    if flush:
        # remove all handlers
        logger.remove()

    formatter = make_formatter(
        indent=indent, timezone=timezone, colorize=colorize, short_levels=short_levels, level_width=4 if short_levels else 7
    )
    _current_formatter = formatter

    sid = logger.add(
        sys.stdout,
        level=level,
        format=formatter,
        colorize=colorize,
    )
    _sink_ids.append(sid)

    if file:
        add_file_sink(file, level=level, formatter=formatter)

    return logger


def add_file_sink(file, level="INFO", formatter=None, rotation="3 MB", retention=3):
    """Add a rotating file sink to the logger. Can be called after setup_logging."""
    global _sink_ids
    if formatter is None:
        formatter = _current_formatter or make_formatter(colorize=False)
    sid = logger.add(
        file,
        level=level,
        format=formatter,
        colorize=True,
        rotation=rotation,
        retention=retention,
    )
    _sink_ids.append(sid)
    return sid


def get_formatter():
    # logger._core.handlers[sid]._format
    return _current_formatter


def log_depth(level, message, depth=0, **kwargs):
    """Helper function to log with depth (indentation). Usage:

    log_with_depth("INFO", "Hello", depth=2)
    """
    logger.bind(depth=depth).log(level, message, **kwargs)


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
