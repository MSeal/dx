import logging
import logging.config
import sys
from typing import Optional

import structlog

from dx.settings import settings

# Timestamp format applied to both vanilla and structlog messages
timestamper = structlog.processors.TimeStamper(fmt=settings.DATETIME_STRING_FORMAT)

# Pre-processing for Vanilla Log messages
pre_chain = [
    # Add extra attributes of LogRecord objects to the event dictionary
    # so that values passed in the extra parameter of log methods pass
    # through to log output.
    structlog.stdlib.ExtraAdder(),
]

# Pre-processing for Structlog messages
structlog.configure(
    processors=[
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)


# List of processors to be applied after pre-processing both vanilla
# and structlog messages, but before a final processor that formats
# the logs into JSON format or colored terminal output.
shared_processors = [
    # log level / logger name, effects coloring in ConsoleRenderer(colors=True)
    structlog.stdlib.add_log_level,
    structlog.stdlib.add_logger_name,
    # timestamp format
    timestamper,
    # To see all CallsiteParameterAdder options:
    # https://www.structlog.org/en/stable/api.html?highlight=CallsiteParameterAdder#structlog.processors.CallsiteParameterAdder
    # more options include module, pathname, process, process_name, thread, thread_name
    structlog.processors.CallsiteParameterAdder(
        {
            structlog.processors.CallsiteParameter.FILENAME,
            structlog.processors.CallsiteParameter.FUNC_NAME,
            structlog.processors.CallsiteParameter.LINENO,
        }
    ),
    # Any structlog.contextvars.bind_contextvars included in middleware/functions
    structlog.contextvars.merge_contextvars,
    # strip _record and _from_structlog keys from event dictionary
    structlog.stdlib.ProcessorFormatter.remove_processors_meta,
]


def configure_logging(app_level: Optional[int] = None):
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "color": {
                    "()": structlog.stdlib.ProcessorFormatter,
                    "processors": shared_processors
                    + [
                        structlog.dev.ConsoleRenderer(colors=True),
                    ],
                    "foreign_pre_chain": pre_chain,
                },
            },
            "handlers": {
                "default": {
                    "class": "logging.StreamHandler",
                    "formatter": "color",
                    "stream": sys.stdout,
                },
            },
            "loggers": {
                "dx": {
                    "handlers": ["default"],
                    "level": "WARNING",
                    "propagate": True,
                },
            },
        }
    )
    # Example of setting one specific logger at a level lower than loggers config
    logging.getLogger("dx").setLevel(app_level or settings.LOG_LEVEL)
