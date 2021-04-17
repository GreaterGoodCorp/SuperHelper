import functools
import os
import stat
import enum
from typing import Callable

from SuperHelper.Core.Utils import PathLike

__all__ = [
    "FP",
    "FileOps",
]


class FP(enum.Flag):
    R_USR = enum.auto()
    W_USR = enum.auto()
    X_USR = enum.auto()
    R_GRP = enum.auto()
    W_GRP = enum.auto()
    X_GRP = enum.auto()
    R_OTH = enum.auto()
    W_OTH = enum.auto()
    X_OTH = enum.auto()


class FileOps:
    @staticmethod
    @functools.cache
    def get_stat(path: PathLike) -> os.stat_result:
        return os.stat(path)

    @staticmethod
    def is_user_own(uid: int, path: PathLike):
        return FileOps.get_stat(path).st_uid == uid

    @staticmethod
    def is_roots(path: PathLike):
        return FileOps.is_user_own(0, path)

    @staticmethod
    def is_mine(path: PathLike):
        return FileOps.is_user_own(os.getuid(), path)

    @staticmethod
    def is_owner_readable(path: PathLike):
        return FileOps.get_stat(path).st_mode & stat.S_IRUSR

    @staticmethod
    def is_owner_writable(path: PathLike):
        return FileOps.get_stat(path).st_mode & stat.S_IWUSR

    @staticmethod
    def is_owner_executable(path: PathLike):
        return FileOps.get_stat(path).st_mode & stat.S_IXUSR

    @staticmethod
    def is_group_readable(path: PathLike):
        return FileOps.get_stat(path).st_mode & stat.S_IRGRP

    @staticmethod
    def is_group_writable(path: PathLike):
        return FileOps.get_stat(path).st_mode & stat.S_IWGRP

    @staticmethod
    def is_group_executable(path: PathLike):
        return FileOps.get_stat(path).st_mode & stat.S_IXGRP

    @staticmethod
    def is_other_readable(path: PathLike):
        return FileOps.get_stat(path).st_mode & stat.S_IROTH

    @staticmethod
    def is_other_writable(path: PathLike):
        return FileOps.get_stat(path).st_mode & stat.S_IWOTH

    @staticmethod
    def is_other_executable(path: PathLike):
        return FileOps.get_stat(path).st_mode & stat.S_IXOTH

    @staticmethod
    def check_fp(path: PathLike, fp: FP):
        flag_match: dict[FP, Callable[[PathLike], bool]] = {
            FP.R_USR: FileOps.is_owner_readable,
            FP.W_USR: FileOps.is_owner_writable,
            FP.X_USR: FileOps.is_owner_executable,
            FP.R_GRP: FileOps.is_group_readable,
            FP.W_GRP: FileOps.is_group_writable,
            FP.X_GRP: FileOps.is_group_executable,
            FP.R_OTH: FileOps.is_other_readable,
            FP.W_OTH: FileOps.is_other_writable,
            FP.X_OTH: FileOps.is_other_executable,
        }
        final = True
        for f in FP:
            if f & fp:
                final &= bool(flag_match[f](path))
        return final
