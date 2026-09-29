"""Central logging setup shared by every module."""
import logging
import os

LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "expense_tracker.log")


def get_logger(name: str) -> logging.Logger:
    """Return a logger writing INFO+ to the log file and WARNING+ to the console.

    Handlers are added only once per logger, so calling this repeatedly is safe.
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.INFO)

        file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
        )
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        console_handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
        logger.addHandler(console_handler)

    return logger
