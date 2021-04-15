import os
from typing import TypeVar

Generic: type = TypeVar("Generic")
PathLike: type = TypeVar("PathLike", str, bytes, os.PathLike)
