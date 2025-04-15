from .format import ColoredFormatter
import logging
from .format import LOG_FORMAT, DATE_FORMAT


def get_logger(name: str = "Base") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        ch = logging.StreamHandler()
        ch.setFormatter(ColoredFormatter(LOG_FORMAT, datefmt=DATE_FORMAT))
        logger.addHandler(ch)
    return logger
