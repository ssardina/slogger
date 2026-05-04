from loguru import logger as _logger
from .loguru_backend import setup_logging, log_indent, log_depth, set_depth

logger = _logger

__all__ = ["logger", "setup_logging", "log_indent", "log_depth", "set_depth", "VERSION"]

try:
    # this requires the package to be installed!
    from importlib.metadata import version, PackageNotFoundError

    VERSION = version("slogger")
except PackageNotFoundError:
    VERSION = "dev"  # fallback version - running with python -m slogger
    
def get_version():
    return VERSION 

def __version__():    
    return get_version()
