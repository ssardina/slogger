"""
Run in-place (no install needed) from the repo root:
    python -m slogger.test
"""
import os

from . import VERSION
from slogger.loguru_backend import setup_logging, log_indent, log_depth, set_depth


def test_basic_logging():
    print("\n--- test_basic_logging ---")
    log = setup_logging(level="DEBUG", colorize=False, flush=True)
    log.debug("debug message")
    log.info("info message")
    log.warning("warning message")
    log.error("error message")


def test_short_levels():
    print("\n--- test_short_levels ---")
    log = setup_logging(level="DEBUG", colorize=False, short_levels=True, flush=True)
    log.debug("short level debug")
    log.warning("short level warning")
    log.error("short level error")
    log.critical("short level critical")


def test_log_indent():
    print("\n--- test_log_indent ---")
    log = setup_logging(level="DEBUG", colorize=False, flush=True)
    log.info("depth 0")
    with log_indent():
        log.info("depth 1")
        with log_indent():
            log.info("depth 2")
            with log_indent():
                log.info("depth 3")
        log.info("back to depth 1")
    log.info("back to depth 0")


def test_log_depth():
    print("\n--- test_log_depth ---")
    setup_logging(level="DEBUG", colorize=False, flush=True)
    log_depth("INFO", "explicit depth 0", depth=0)
    log_depth("INFO", "explicit depth 2", depth=2)
    log_depth("DEBUG", "explicit depth 4", depth=4)


def test_set_depth():
    print("\n--- test_set_depth ---")
    log = setup_logging(level="DEBUG", colorize=False, flush=True)
    token = set_depth(3)
    log.info("set to depth 3")
    log.debug("still depth 3")
    # reset back
    from contextvars import ContextVar
    # restore by setting to 0
    set_depth(0)
    log.info("reset to depth 0")


def test_file_logging(tmp_path=None):
    print("\n--- test_file_logging ---")
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".log", delete=False) as f:
        logfile = f.name
    try:
        log = setup_logging(level="INFO", colorize=False, file=logfile, flush=True)
        log.info("written to file")
        log.warning("warning to file")
        with open(logfile) as f:
            contents = f.read()
        assert "written to file" in contents, "Expected log message not found in file"
        assert "warning to file" in contents, "Expected warning not found in file"
        print(f"  File log OK ({logfile}):")
        print("  " + contents.replace("\n", "\n  ").rstrip())
    finally:
        os.unlink(logfile)


if __name__ == "__main__":
    print(f"Running slogger tests (version: {VERSION})")
    test_basic_logging()
    test_short_levels()
    test_log_indent()
    test_log_depth()
    test_set_depth()
    test_file_logging()
    print("\nAll tests passed.")
