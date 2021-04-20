# This module provides a function to initialise the top-level logger
import logging

from SuperHelper.Core.Utils import PathLike

__all__ = [
    "setup_core_logger",
]


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


def setup_core_logger(logging_path: PathLike, debug: bool = False) -> logging.Logger:
    """Sets up the core logger.

    Args:
        logging_path (PathLike): The path to the logging file.
        debug (bool): Whether to print debugging message.

    Returns:
        A `logging.Logger` instance with name set to `SuperHelper`.
    """
    logger = logging.getLogger("SuperHelper")
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(logging_path, mode="a+")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter("[%(asctime)s](%(name)s) %(levelname)s: %(message)s"))
    fh.addFilter(TracebackInfoFilter(clear=False))
    ch = logging.StreamHandler()
    if debug:
        ch.setLevel(logging.DEBUG)
    else:
        ch.setLevel(logging.WARNING)
    ch.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    if debug:
        ch.addFilter(TracebackInfoFilter(clear=False))
    else:
        ch.addFilter(TracebackInfoFilter())
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger
