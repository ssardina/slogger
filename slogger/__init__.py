from loguru import logger as _logger
from .loguru_backend import (
    setup_logging,
    log_indent,
    log_depth,
    set_depth,
    add_file_sink,
    get_formatter,
)
from importlib.metadata import version, PackageNotFoundError

logger = _logger

__all__ = [
    "logger",
    "setup_logging",
    "log_indent",
    "log_depth",
    "set_depth",
    "VERSION",
    "add_file_sink",
    "get_formatter",
]

try:
    # this requires the package to be installed!
    VERSION = version("slogger")
except PackageNotFoundError:
    VERSION = "dev"  # fallback version - running with python -m slogger


def get_version():
    return VERSION


def __version__():
    return get_version()
