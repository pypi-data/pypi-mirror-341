from __future__ import annotations

import logging
import sys
from typing import ClassVar


class CustomFormatter(logging.Formatter):
    """A custom logger formatter"""

    grey = "\x1b[38;20m"
    blue = "\x1b[34;20m"
    green = "\x1b[32;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format_str = "%(module)s - %(funcName)s: %(message)s"
    FORMATS: ClassVar[dict[int, str]] = {
        logging.DEBUG: f"{blue}%(levelname)s{reset} {format_str}",
        logging.INFO: f"{green}%(levelname)s{reset} {format_str}",
        logging.WARNING: f"{yellow}%(levelname)s{reset} {format_str}",
        logging.ERROR: f"{red}%(levelname)s{reset} {format_str}",
        logging.CRITICAL: f"{bold_red}%(levelname)s{reset} {format_str}",
    }

    def format(self, record: logging.LogRecord) -> str:
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, "%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


logging.captureWarnings(True)
handler = logging.StreamHandler(sys.stdout)
formatter = CustomFormatter()
handler.setFormatter(formatter)
logging.getLogger().addHandler(handler)
logger = logging.getLogger("cross_bones")
logger.setLevel(logging.INFO)
