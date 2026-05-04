# slogger: My own Logging System for Python

A personal logger based on [loguru](https://github.com/delgan/loguru), with some custom features that I find useful in my projects:

- Indentation per depth level for better readability.
- Colouring of log messages based on log level.
- Rotating file.
- Custom timezone (useful when running on servers with UTC time).

## Installation

```console
$ pip install git+https://github.com/ssardina/slogger.git
```

## Example

From the entry point of your application:

```python
from slogger import logger, setup_logging
setup_logging(colorize=True, short_levels=False, indent=2, force=False)
logger.remove(0)  # Remove default logger to prevent duplicate logs.
```

Then elsewhere in your code:

```python
from slogger import logger, log_indent


logger.info("Start")

with log_indent():
    logger.info("Nested")   
```


## Development and testing:

Logger is based on [loguru](https://github.com/delgan/loguru).

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
