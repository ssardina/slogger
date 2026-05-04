from loguru import logger as _logger
from .loguru_backend import setup_logging, log_indent, log_depth

logger = _logger

__all__ = ["logger", "setup_logging", "log_indent", "log_depth"]

