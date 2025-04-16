# minakicoin/log/logger.py

import logging
from rich.console import Console
from rich.logging import RichHandler

# Console for pretty print
console = Console()

# Global logger setup
logger = logging.getLogger("minakicoin")
logger.setLevel(logging.DEBUG)

# Rich handler for colorized logs
rich_handler = RichHandler(console=console, show_time=True, show_level=True, show_path=False)
formatter = logging.Formatter("%(message)s")
rich_handler.setFormatter(formatter)

# Clear existing handlers and set rich handler
if logger.hasHandlers():
    logger.handlers.clear()

logger.addHandler(rich_handler)

# Aliased print
def log_info(msg): logger.info(msg)
def log_warn(msg): logger.warning(msg)
def log_error(msg): logger.error(msg)
def log_debug(msg): logger.debug(msg)
