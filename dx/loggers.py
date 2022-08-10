import logging
import sys
from typing import Optional

from dx.settings import settings


def get_logger(name: str, level: Optional[int] = None):
    logging.basicConfig(
        encoding="utf-8",
        force=True,
        format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        level=logging.DEBUG,
        stream=sys.stdout,
    )
    logger = logging.getLogger(name)
    logger.setLevel(level or settings.LOG_LEVEL)
    return logger
