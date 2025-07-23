import sys
from loguru import logger

def setup_logging(level: str = "INFO"):
    """Configure loguru logging for CLI."""
    logger.remove()
    logger.add(
        sys.stderr,
        level=level,
        format=custom_format,
        colorize=True
    )

    logger.level("INFO", color="<b><green>")

def custom_format(record):
    level = record['level'].name
    padding = " " * (10 - len(level) - 2)
    return f'[<level>{level}</level>]{padding} {record["message"]}\n'