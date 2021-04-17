# This module defines the FP enum, to specify file permission flags, and the FileOps class, a utility class to check
# file ownership and permissions.
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
    """
    Contains file permission flags.

    R = Read

    W = Write

    X = Execute

    USR = User (file owner)

    GRP = Group owner

    OTH = Other users/groups
    """
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
    """
    A utility class for file ownership and permissions.
    """
    @staticmethod
    @functools.cache
    def get_stat(path: PathLike) -> os.stat_result:
        """Gets the `stat` of file pointed by the path.

        This function is decorated by @cache to reduce the amount of syscall, since `os.stat` is an expensive function.

        :param path: Path to the file to check
        :type path: PathLike
        :return: An os.stat_result instance containing the stat of the file
        :rtype: os.stat_result
        """
        return os.stat(path)

    @staticmethod
    def is_user_own(uid: int, path: PathLike) -> bool:
        """Checks if the file is owned by the user with `uid`.

        :param uid: The UID of the user
        :type uid: int
        :param path: Path to the file to check
        :type path: PathLike
        :return: True if the file is owned by the uid, otherwise False
        :rtype: bool
        """
        return FileOps.get_stat(path).st_uid == uid

    @staticmethod
    def is_roots(path: PathLike) -> bool:
        """Check if the file is owned by `root`.

        :param path: Path to the file to check
        :type path: PathLike
        :return: True if the file is owned by root, otherwise False
        :rtype: bool
        """
        return FileOps.is_user_own(0, path)

    @staticmethod
    def is_mine(path: PathLike) -> bool:
        """Checks if the file is owned by the current user.

        :param path: Path to the file to check
        :type path: PathLike
        :return: True if the file is owned by the current user, otherwise False
        :rtype: bool
        """
        return FileOps.is_user_own(os.getuid(), path)

    @staticmethod
    def is_owner_readable(path: PathLike) -> bool:
        """Checks if the owner of the file can read it.

        :param path: Path to the file to check
        :type path: PathLike
        :return: True if the file is readable by its owner, otherwise False
        :rtype: bool
        """
        return FileOps.get_stat(path).st_mode & stat.S_IRUSR

    @staticmethod
    def is_owner_writable(path: PathLike) -> bool:
        """Checks if the owner of the file can write to it.

        :param path: Path to the file to check
        :type path: PathLike
        :return: True if the file is writable by its owner, otherwise False
        :rtype: bool
        """
        return FileOps.get_stat(path).st_mode & stat.S_IWUSR

    @staticmethod
    def is_owner_executable(path: PathLike) -> bool:
        """Checks if the owner of the file can execute it.

        :param path: Path to the file to check
        :type path: PathLike
        :return: True if the file is executable by its owner, otherwise False
        :rtype: bool
        """
        return FileOps.get_stat(path).st_mode & stat.S_IXUSR

    @staticmethod
    def is_group_readable(path: PathLike) -> bool:
        """Checks if the group owner of the file can read it.

        :param path: Path to the file to check
        :type path: PathLike
        :return: True if the file is readable by its group owner, otherwise False
        :rtype: bool
        """
        return FileOps.get_stat(path).st_mode & stat.S_IRGRP

    @staticmethod
    def is_group_writable(path: PathLike) -> bool:
        """Checks if the group owner of the file can write to it.

        :param path: Path to the file to check
        :type path: PathLike
        :return: True if the file is writable by its group owner, otherwise False
        :rtype: bool
        """
        return FileOps.get_stat(path).st_mode & stat.S_IWGRP

    @staticmethod
    def is_group_executable(path: PathLike) -> bool:
        """Checks if the group owner of the file can execute it.

        :param path: Path to the file to check
        :type path: PathLike
        :return: True if the file is executable by its group owner, otherwise False
        :rtype: bool
        """
        return FileOps.get_stat(path).st_mode & stat.S_IXGRP

    @staticmethod
    def is_other_readable(path: PathLike) -> bool:
        """Checks if the other users or groups can read the file.

        :param path: Path to the file to check
        :type path: PathLike
        :return: True if the file is readable by them, otherwise False
        :rtype: bool
        """
        return FileOps.get_stat(path).st_mode & stat.S_IROTH

    @staticmethod
    def is_other_writable(path: PathLike) -> bool:
        """Checks if the other users or groups can write the file.

        :param path: Path to the file to check
        :type path: PathLike
        :return: True if the file is writable by them, otherwise False
        :rtype: bool
        """
        return FileOps.get_stat(path).st_mode & stat.S_IWOTH

    @staticmethod
    def is_other_executable(path: PathLike) -> bool:
        """Checks if the other users or groups can execute the file.

        :param path: Path to the file to check
        :type path: PathLike
        :return: True if the file is executable by them, otherwise False
        :rtype: bool
        """
        return FileOps.get_stat(path).st_mode & stat.S_IXOTH

    @staticmethod
    def check_fp(path: PathLike, fp: FP) -> bool:
        """Checks if the file contains the specified file permissions.

        :param path: Path to the file to check
        :type path: PathLike
        :param fp: The flags of the file permissions to check.
        :type fp: FP
        :return: True if all the flags are valid, otherwise False
        :rtype: bool
        """
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
