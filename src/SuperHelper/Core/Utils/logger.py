# This module provides a function to initialise the top-level logger
import logging


class TracebackInfoFilter(logging.Filter):
    """Clear or restore the exception on log records"""

    def __init__(self, clear=True):
        super().__init__()
        self.clear = clear

    def filter(self, record):
        if self.clear:
            record._exc_info_hidden, record.exc_info = record.exc_info, None
            # clear the exception traceback text cache, if created.
            record.exc_text = None
        elif hasattr(record, "_exc_info_hidden"):
            record.exc_info = record._exc_info_hidden
            del record._exc_info_hidden
        return True


def initialise_core_logger(logging_path: str) -> logging.Logger:
    logger = logging.getLogger("SuperHelper")
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(logging_path, mode="a+")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter("[%(asctime)s](%(name)s) %(levelname)s: %(message)s"))
    fh.addFilter(TracebackInfoFilter(clear=False))
    ch = logging.StreamHandler()
    ch.setLevel(logging.WARNING)
    ch.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    ch.addFilter(TracebackInfoFilter())
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger
