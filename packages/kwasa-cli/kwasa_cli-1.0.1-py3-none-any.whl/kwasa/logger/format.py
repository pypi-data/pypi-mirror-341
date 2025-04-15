import logging
from .color import LEVEL_COLORS
from colored import style, fore

LOG_FORMAT = "[%(asctime)s] - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class ColoredFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        level_color = LEVEL_COLORS.get(record.levelno, fore("white"))
        message = super().format(record)
        return f"{level_color}{message}{style('reset')}"
