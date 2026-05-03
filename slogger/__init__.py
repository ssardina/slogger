from .loguru_backend import (
    setup_logging,
    log_indent,
    log_depth,   # (rename this, see below)
    set_depth,   # (new function to set depth directly, useful for async contexts
)

__all__ = ["setup_logging", "log_indent", "log_depth"]