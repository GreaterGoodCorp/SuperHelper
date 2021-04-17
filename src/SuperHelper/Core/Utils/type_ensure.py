# This module defines the TypeCheck class, a utility class for type checking functions.
import os
from types import FunctionType, GeneratorType
from typing import Union

from SuperHelper.Core.Utils import PathLike

__all__ = [
    "TypeCheck",
]


def _raise_type_error(t: type, obj: ..., name: str) -> None:
    if name is not None:
        raise TypeError(f"The expected type of '{name}' is {t.__name__} (given '{type(obj).__name__}' instead)")
    else:
        raise TypeError(f"The expected type is {t.__name__} (given '{type(obj).__name__}' instead)")


def _raise_on_failure(b: bool, t: type, obj: ..., name: str) -> None:
    return _raise_type_error(t, obj, name) if not b else None


def _ensure_obj_of_type(t: Union[type, list, tuple], obj: ..., name: str = None) -> None:
    if type(t) == type:
        return _raise_on_failure(isinstance(obj, t), t, obj, name)
    return _raise_on_failure(isinstance(obj, t[1:]), t[1], obj, name)


class TypeCheck:
    """
    A utility class for type checking functions.
    """

    @staticmethod
    def ensure_custom(t: type, obj: ..., name: str = None) -> None:
        """Ensures the object is of the expected type.

        Args:
            t (type): The expected type of the object.
            obj (object): The object to check.
            name (str): The name of the object.

        Returns:
            None
        Raises:
            TypeError: The type of the object is not the specified type.
        """
        return _ensure_obj_of_type(t, obj, name)

    @staticmethod
    def ensure_bool(obj: ..., name: str = None) -> None:
        """Ensures the object is of type `bool`.

        Args:
            obj (object): The object to check.
            name (str): The name of the object.

        Returns:
            None

        Raises:
            TypeError: The type of the object is not the specified type.
        """
        return _ensure_obj_of_type(bool, obj, name)

    @staticmethod
    def ensure_int(obj: ..., name: str = None) -> None:
        """Ensures the object is of type `int`.

        Args:
            obj (object): The object to check.
            name (str): The name of the object.

        Returns:
            None

        Raises:
            TypeError: The type of the object is not the specified type.
        """
        return _ensure_obj_of_type(int, obj, name)

    @staticmethod
    def ensure_float(obj: ..., name: str = None) -> None:
        """Ensures the object is of type `float`.

        Args:
            obj (object): The object to check.
            name (str): The name of the object.

        Returns:
            None

        Raises:
            TypeError: The type of the object is not the specified type.
        """
        return _ensure_obj_of_type(float, obj, name)

    @staticmethod
    def ensure_complex(obj: ..., name: str = None) -> None:
        """Ensures the object is of type `complex`.

        Args:
            obj (object): The object to check.
            name (str): The name of the object.

        Returns:
            None

        Raises:
            TypeError: The type of the object is not the specified type.
        """
        return _ensure_obj_of_type(complex, obj, name)

    @staticmethod
    def ensure_str(obj: ..., name: str = None) -> None:
        """Ensures the object is of type `str`.

        Args:
            obj (object): The object to check.
            name (str): The name of the object.

        Returns:
            None

        Raises:
            TypeError: The type of the object is not the specified type.
        """
        return _ensure_obj_of_type(str, obj, name)

    @staticmethod
    def ensure_bytes(obj: ..., name: str = None) -> None:
        """Ensures the object is of type `bytes`.

        Args:
            obj (object): The object to check.
            name (str): The name of the object.

        Returns:
            None

        Raises:
            TypeError: The type of the object is not the specified type.
        """
        return _ensure_obj_of_type(bytes, obj, name)

    @staticmethod
    def ensure_bytearray(obj: ..., name: str = None) -> None:
        """Ensures the object is of type `bytearray`.

        Args:
            obj (object): The object to check.
            name (str): The name of the object.

        Returns:
            None

        Raises:
            TypeError: The type of the object is not the specified type.
        """
        return _ensure_obj_of_type(bytearray, obj, name)

    @staticmethod
    def ensure_list(obj: ..., name: str = None) -> None:
        """Ensures the object is of type `list`.

        Args:
            obj (object): The object to check.
            name (str): The name of the object.

        Returns:
            None

        Raises:
            TypeError: The type of the object is not the specified type.
        """
        return _ensure_obj_of_type(list, obj, name)

    @staticmethod
    def ensure_tuple(obj: ..., name: str = None) -> None:
        """Ensures the object is of type `tuple`.

        Args:
            obj (object): The object to check.
            name (str): The name of the object.

        Returns:
            None

        Raises:
            TypeError: The type of the object is not the specified type.
        """
        return _ensure_obj_of_type(tuple, obj, name)

    @staticmethod
    def ensure_dict(obj: ..., name: str = None) -> None:
        """Ensures the object is of type `dict`.

        Args:
            obj (object): The object to check.
            name (str): The name of the object.

        Returns:
            None

        Raises:
            TypeError: The type of the object is not the specified type.
        """
        return _ensure_obj_of_type(dict, obj, name)

    @staticmethod
    def ensure_set(obj: ..., name: str = None) -> None:
        """Ensures the object is of type `set`.

        Args:
            obj (object): The object to check.
            name (str): The name of the object.

        Returns:
            None

        Raises:
            TypeError: The type of the object is not the specified type.
        """
        return _ensure_obj_of_type(set, obj, name)

    @staticmethod
    def ensure_frozenset(obj: ..., name: str = None) -> None:
        """Ensures the object is of type `frozenset`.

        Args:
            obj (object): The object to check.
            name (str): The name of the object.

        Returns:
            None

        Raises:
            TypeError: The type of the object is not the specified type.
        """
        return _ensure_obj_of_type(frozenset, obj, name)

    @staticmethod
    def ensure_generator(obj: ..., name: str = None) -> None:
        """Ensures the object is a generator.

        Args:
            obj (object): The object to check.
            name (str): The name of the object.

        Returns:
            None

        Raises:
            TypeError: The type of the object is not the specified type.
        """
        return _ensure_obj_of_type(GeneratorType, obj, name)

    @staticmethod
    def ensure_memoryview(obj: ..., name: str = None) -> None:
        """Ensures the object is of type `memoryview`.

        Args:
            obj (object): The object to check.
            name (str): The name of the object.

        Returns:
            None

        Raises:
            TypeError: The type of the object is not the specified type.
        """
        return _ensure_obj_of_type(memoryview, obj, name)

    @staticmethod
    def ensure_function(obj: ..., name: str = None) -> None:
        """Ensures the object is a function.

        Args:
            obj (object): The object to check.
            name (str): The name of the object.

        Returns:
            None

        Raises:
            TypeError: The type of the object is not the specified type.
        """
        return _ensure_obj_of_type(FunctionType, obj, name)

    @staticmethod
    def ensure_path_like(obj: ..., name: str = None):
        """Ensures the object can be used as a path.

        Args:
            obj (object): The object to check.
            name (str): The name of the object.

        Returns:
            None

        Raises:
            TypeError: The type of the object is not the specified type.
        """
        return _ensure_obj_of_type((PathLike, str, bytes, os.PathLike), obj, name)
