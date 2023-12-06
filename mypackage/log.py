"""
log.py: logging config for this package
---------------------------------------


* Copyright: 2023 Dat Tran
* Authors: Dat Tran (hello@dats.bio)
* Date: 2023-12-06
* Version: 0.0.1


This is part of the mypackage package


License
-------
Proprietary License

"""


from __future__ import annotations
import logging
import structlog
from logging.handlers import RotatingFileHandler
from logging import NullHandler


def get_logger(**config: dict):
    """
    Get logger object given the logging config
    """

    if config is None:
        logger = logging.getLogger()
        logger.setLevel("NOTSET")
        logger.addHandler(NullHandler())
        return structlog.wrap_logger(logger)

    path = config.get("path", None)
    suffix = config.get("suffix")
    stdout = config.get("stdout", False)
    name = config.get("name")
    level = config.get("level", "DEBUG").upper()
    max_bytes = config.get("maxbytes", 10485760)
    backup_count = config.get("backupcount", 2)

    if isinstance(path, str):
        if path.endswith(".json"):
            path = path[:-5]
            ext = ".json"
        elif path.endswith(".log"):
            path = path[:-4]
            ext = ".log"
        else:
            ext = ".json"
    else:
        ext = ".json"

    # if separate sink is not set, then suffix is not used
    separate_sink = config.get("separate_sink", True)
    if not separate_sink:
        suffix = None

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # sink to nothingness
    if path is None and not stdout:
        logger.addHandler(NullHandler())
        return structlog.wrap_logger(logger)

    if path:
        if suffix:
            path += "_" + suffix
        path += ext
        file_handler = RotatingFileHandler(
            path, maxBytes=max_bytes, backupCount=backup_count
        )
        file_handler.setFormatter(logging.Formatter("%(message)s"))
        logger.addHandler(file_handler)

    if stdout:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter("%(message)s"))
        logger.addHandler(stream_handler)

    # config structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer(),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # return the structured logger
    return structlog.get_logger(name)
