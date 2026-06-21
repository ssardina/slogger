import datetime
from zoneinfo import ZoneInfo


SHORT_LEVELS = {
    "WARNING": "WARN",
    "ERROR": "ERR",
    "CRITICAL": "CRIT",
    "DEBUG": "DEBG",
}

DEFAULT_INDENT = 2

# https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
DEFAULT_TIMEZONE: ZoneInfo = ZoneInfo("Australia/Melbourne")
UTC: ZoneInfo = ZoneInfo("UTC")

LOG_RECORD_BUILTIN_ATTRS = {
    "args",
    "asctime",
    "created",
    "exc_info",
    "exc_text",
    "filename",
    "funcName",
    "levelname",
    "levelno",
    "lineno",
    "module",
    "msecs",
    "message",
    "msg",
    "name",
    "pathname",
    "process",
    "processName",
    "relativeCreated",
    "stack_info",
    "thread",
    "threadName",
    "taskName",
}
