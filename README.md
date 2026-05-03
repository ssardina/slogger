# slogger: My own Logging System for Python

Features:

- Identation per depth level for better readability.
- Coloring of log messages based on log level.
- Rotating file.
- Custom timezone (useful when running on servers with UTC time).

## Installation

```console
$ pip install git+https://github.com/yourname/slogger.git
```

## Example

```python
from slogger import setup_logging, log_indent, logger

setup_logging()

logger.info("Start")

with log_indent():
    logger.info("Nested")
```
