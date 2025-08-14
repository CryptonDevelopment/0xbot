import logging

import structlog
from structlog import wrap_logger


def add_handlers(logger: logging.Logger) -> logging.Logger:
    log_formatter = logging.Formatter(
        "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    logger.addHandler(console_handler)


def get_logger(logger: logging.Logger) -> logging.Logger:
    root_logger = add_handlers(logging.getLogger(logger))

    log = wrap_logger(
        root_logger,
        processors=[
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(sort_keys=True),
        ],
    )
    return log
