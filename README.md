# slogger: My own Logging System for Python

A personal logger system with a custom features that I find useful in applications:

- Indentation per depth level for better readability.
- Colouring of log messages based on log level.
- Rotating file.
- Custom timezone (useful when running on servers with UTC time).

There are three implementations available:

1. **loguru_backend**: Based on [loguru](https://github.com/delgan/loguru), with some custom features that I find useful in my projects.
2. **logging_backend**: Based on Python's built-in `logging` module, with custom features for indentation and coloring. This is the original implementation I have used, but it is much more complex than the loguru one.
3. **std_backend**: A simple backend done by Claude that I have never tested!

## Installation

```console
$ pip install git+https://github.com/ssardina/slogger.git
```

## Example

From the entry point of your application:

```python
# slogger: https://github.com/ssardina/slogger
from slogger.loguru_backend import logger, setup_logging

LEVEL = "INFO"
# LEVEL = "DEBUG"
setup_logging(level=LEVEL, colorize=True, short_levels=True, indent=2, flush=False)
logger.remove(0)  # Remove default logger to prevent duplicate logs.
```

Then elsewhere in your code:

```python
from slogger.loguru_backend import logger, log_indent

logger.info("Start")

with log_indent():
    logger.info("Nested")
```

## Development and testing

### Versioning

Versioning is based on [setuptools_scm](https://github.com/pypa/setuptools_scm), which automatically generates the version number based on git tags. To update the version, simply create a new git tag following semantic versioning (e.g., `v1.0.0`), and the next time you run the tests or use the logger, it will reflect the new version.

### Testing

```shell
$ python -m slogger.test
Running slogger tests (version: 1.0.0)

--- test_basic_logging ---
2026-05-04T21:51:43 [__main__] DEBUG   | debug message
2026-05-04T21:51:43 [__main__] INFO    | info message
2026-05-04T21:51:43 [__main__] WARNING | warning message
2026-05-04T21:51:43 [__main__] ERROR   | error message

--- test_short_levels ---
2026-05-04T21:51:43 [__main__] DEBG    | short level debug
2026-05-04T21:51:43 [__main__] WARN    | short level warning
2026-05-04T21:51:43 [__main__] ERR     | short level error
2026-05-04T21:51:43 [__main__] CRIT    | short level critical

--- test_log_indent ---
2026-05-04T21:51:43 [__main__] INFO    | depth 0
2026-05-04T21:51:43 [__main__] INFO    |   depth 1
2026-05-04T21:51:43 [__main__] INFO    |     depth 2
2026-05-04T21:51:43 [__main__] INFO    |       depth 3
2026-05-04T21:51:43 [__main__] INFO    |   back to depth 1
2026-05-04T21:51:43 [__main__] INFO    | back to depth 0

--- test_log_depth ---
2026-05-04T21:51:43 [slogger.loguru_backend] INFO    | explicit depth 0
2026-05-04T21:51:43 [slogger.loguru_backend] INFO    |     explicit depth 2
2026-05-04T21:51:43 [slogger.loguru_backend] DEBUG   |         explicit depth 4

--- test_set_depth ---
2026-05-04T21:51:43 [__main__] INFO    |       set to depth 3
2026-05-04T21:51:43 [__main__] DEBUG   |       still depth 3
2026-05-04T21:51:43 [__main__] INFO    | reset to depth 0

--- test_file_logging ---
2026-05-04T21:51:43 [__main__] INFO    | written to file
2026-05-04T21:51:43 [__main__] WARNING | warning to file
  File log OK (/tmp/tmptw35ql7r.log):
  2026-05-04T21:51:43 [__main__] INFO    | written to file
  2026-05-04T21:51:43 [__main__] WARNING | warning to file

All tests passed.
```
