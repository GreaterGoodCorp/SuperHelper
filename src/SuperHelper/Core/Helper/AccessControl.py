# This module defines helper functions regarding access control
import ctypes
import os


def is_root() -> bool:
    try:
        return os.getuid() == 0
    except AttributeError:
        return ctypes.windll.shell32.IsUserAnAdmin()
