# This module contains the type hinting extensions.
import os
from typing import TypeVar

__all__ = [
    "PathLike",
]

# PathLike type, which can be passed as argument to I/O function
PathLike: type = TypeVar("PathLike", str, bytes, os.PathLike)
