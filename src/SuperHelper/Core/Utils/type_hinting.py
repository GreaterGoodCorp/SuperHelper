import os
from typing import TypeVar

__all__ = [
    "Generic",
    "PathLike",
]

Generic: type = TypeVar("Generic")
PathLike: type = TypeVar("PathLike", str, bytes, os.PathLike)
