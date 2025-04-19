"""
inlines sentry_sdk.integrations.loguru and sentry_sdk.integrations.logging, so we can make some changes.
i'm intentionally keeping most of the old logic so this still behaves roughly as expected/documented.

The changes so far (could be out of date):
- adds `strip_extra` to the breadcrumb handler
"""
import enum
import logging
from datetime import datetime
from datetime import timezone
from fnmatch import fnmatch
from typing import Any
from typing import Dict

import sentry_sdk

# "This disables recording (both in breadcrumbs and as events) calls to a logger of a specific name.  Among other uses, many of our integrations
# use this to prevent their actions being recorded as breadcrumbs. Exposed to users as a way to quiet spammy loggers."
# We have to import it so that existing setters work properly
from sentry_sdk.integrations.logging import _IGNORED_LOGGERS
from sentry_sdk.utils import capture_internal_exceptions
from sentry_sdk.utils import current_stacktrace
from sentry_sdk.utils import event_from_exception
from sentry_sdk.utils import to_string


class SentryLoguruLoggingLevels(enum.IntEnum):
    TRACE = 5
    DEBUG = 10
    INFO = 20
    SUCCESS = 25
    WARNING = 30
    ERROR = 40
    CRITICAL = 50


class _BaseHandler(logging.Handler):
    COMMON_RECORD_ATTRS = frozenset(
        (
            "args",
            "created",
            "exc_info",
            "exc_text",
            "filename",
            "funcName",
            "levelname",
            "levelno",
            "linenno",
            "lineno",
            "message",
            "module",
            "msecs",
            "msg",
            "name",
            "pathname",
            "process",
            "processName",
            "relativeCreated",
            "stack",
            "tags",
            "taskName",
            "thread",
            "threadName",
            "stack_info",
        )
    )

    def _can_record(self, record: logging.LogRecord) -> bool:
        """Prevents ignored loggers from recording"""
        for logger in _IGNORED_LOGGERS:
            if fnmatch(record.name, logger):
                return False
        return True

    def _extra_from_record(self, record: logging.LogRecord) -> dict[str, object]:
        return {
            k: v
            for k, v in vars(record).items()
            if k not in self.COMMON_RECORD_ATTRS and (not isinstance(k, str) or not k.startswith("_"))
        }

    def _logging_to_event_level(self, record: logging.LogRecord) -> str:
        try:
            return SentryLoguruLoggingLevels(record.levelno).name.lower()
        except ValueError:
            return record.levelname.lower() if record.levelname else ""


class SentryEventHandler(_BaseHandler):
    """
    A logging handler that emits Sentry events for each log record

    Note that you do not have to use this class if the logging integration is enabled, which it is by default.
    """

    def emit(self, record: logging.LogRecord) -> Any:
        with capture_internal_exceptions():
            self.format(record)
            return self._emit(record)

    def _emit(self, record: logging.LogRecord) -> None:
        if not self._can_record(record):
            return

        client = sentry_sdk.get_client()
        if not client.is_active():
            return

        client_options = client.options

        # exc_info might be None or (None, None, None)
        #
        # exc_info may also be any falsy value due to Python stdlib being
        # liberal with what it receives and Celery's billiard being "liberal"
        # with what it sends. See
        # https://github.com/getsentry/sentry-python/issues/904
        if record.exc_info and record.exc_info[0] is not None:
            event, hint = event_from_exception(
                record.exc_info,
                client_options=client_options,
                mechanism={"type": "logging", "handled": True},
            )
        elif (record.exc_info and record.exc_info[0] is None) or record.stack_info:
            event = {}
            hint = {}
            with capture_internal_exceptions():
                event["threads"] = {
                    "values": [
                        {
                            "stacktrace": current_stacktrace(
                                include_local_variables=client_options["include_local_variables"],
                                max_value_length=client_options["max_value_length"],
                            ),
                            "crashed": False,
                            "current": True,
                        }
                    ]
                }
        else:
            event = {}
            hint = {}

        hint["log_record"] = record

        level = self._logging_to_event_level(record)
        if level in {"debug", "info", "warning", "error", "critical", "fatal"}:
            event["level"] = level  # type: ignore[typeddict-item]
        event["logger"] = record.name

        # Log records from `warnings` module as separate issues
        record_caputured_from_warnings_module = record.name == "py.warnings" and record.msg == "%s"
        if record_caputured_from_warnings_module:
            # use the actual message and not "%s" as the message
            # this prevents grouping all warnings under one "%s" issue
            msg = record.args[0]  # type: ignore

            event["logentry"] = {
                "message": msg,
                "params": (),
            }

        else:
            event["logentry"] = {
                "message": to_string(record.msg),
                "params": record.args,
            }

        event["extra"] = self._extra_from_record(record)

        sentry_sdk.capture_event(event, hint=hint)


class SentryBreadcrumbHandler(_BaseHandler):
    """
    A logging handler that records breadcrumbs for each log record.

    Note that you do not have to use this class if the logging integration is enabled, which it is by default.
    """

    def __init__(self, level: int = logging.NOTSET, strip_extra: bool = False) -> None:
        super().__init__(level=level)
        self.strip_extra = strip_extra

    def emit(self, record: logging.LogRecord) -> Any:
        with capture_internal_exceptions():
            self.format(record)
            return self._emit(record)

    def _emit(self, record: logging.LogRecord) -> None:
        if not self._can_record(record):
            return

        sentry_sdk.add_breadcrumb(self._breadcrumb_from_record(record), hint={"log_record": record})

    def _breadcrumb_from_record(self, record: logging.LogRecord) -> Dict[str, Any]:
        return {
            "type": "log",
            "level": self._logging_to_event_level(record),
            "category": record.name,
            "message": record.message,
            "timestamp": datetime.fromtimestamp(record.created, timezone.utc),
            "data": self._extra_from_record(record) if not self.strip_extra else {},
        }
