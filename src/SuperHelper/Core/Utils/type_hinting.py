# This module contains the type hinting extensions.
import os
from typing import TypeVar

__all__ = [
    "Generic",
    "PathLike",
]

# Generic type, i.e. any type
Generic: type = TypeVar("Generic")

# PathLike type, which can be passed as argument to I/O function
PathLike: type = TypeVar("PathLike", str, bytes, os.PathLike)
