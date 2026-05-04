# slogger: My own Logging System for Python

Features:

- Identation per depth level for better readability.
- Coloring of log messages based on log level.
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
