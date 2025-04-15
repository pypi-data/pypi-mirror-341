import logging
from colored import fore

LEVEL_COLORS = {
    logging.DEBUG: fore("cyan"),
    logging.INFO: fore("green"),
    logging.WARNING: fore("yellow"),
    logging.ERROR: fore("red"),
    logging.CRITICAL: fore("magenta"),
}
