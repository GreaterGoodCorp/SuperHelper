# This module provides a function to initialise the top-level logger
import logging


def initialise_core_logger(logging_path: str):
    logger = logging.getLogger("SuperHelper")
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(logging_path, mode="w")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter("[%(asctime)s](%(name)s) %(levelname)s: %(message)s"))
    ch = logging.StreamHandler()
    ch.setLevel(logging.WARNING)
    ch.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger
