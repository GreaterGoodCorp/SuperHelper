# This module defines the TypeCheck class, a utility class for type checking functions.
from types import FunctionType, GeneratorType

__all__ = [
    "TypeCheck",
]


def _raise_type_error(t: type, obj: ..., name: str) -> None:
    """Raises TypeError for the specified object.

    :param t: The expected type of the object
    :type t: type
    :param obj: The object to raise
    :type obj: object
    :param name: Name of the object
    :type name: str
    """
    if name is not None:
        raise TypeError(f"The expected type of '{name}' is {t.__name__} (given '{type(obj).__name__}' instead)")
    else:
        raise TypeError(f"The expected type is {t.__name__} (given '{type(obj).__name__}' instead)")


def _raise_on_failure(b: bool, t: type, obj: ..., name: str) -> None:
    """Raises TypeError if failed to match correct type.

    :param b: Whether the type is correct
    :type b: bool
    :param t: The expected type of the object
    :type t: type
    :param obj: The object to raise
    :type obj: object
    :param name: Name of the object
    :type name: str
    """
    return _raise_type_error(t, obj, name) if not b else None


def _ensure_obj_of_type(t: type, obj: ..., name: str = None) -> None:
    """Ensures the object is of the expected type.

    :param t: The expected type of the object
    :type t: type
    :param obj: The object to check
    :type obj: object
    :param name: The name of the object
    :type name: str
    """
    return _raise_on_failure(type(obj) == t, t, obj, name)


class TypeCheck:
    """
    A utility class for type checking functions.
    """

    @staticmethod
    def ensure_custom(t: type, obj: ..., name: str = None) -> None:
        """Ensures the object is of the expected type.

        :param t: The expected type of the object
        :type t: type
        :param obj: The object to check
        :type obj: object
        :param name: The name of the object
        :type name: str
        """
        return _ensure_obj_of_type(t, obj, name)

    @staticmethod
    def ensure_int(obj: ..., name: str = None) -> None:
        """Ensures the object is of type `int`.

        :param obj: The object to check
        :type obj: object
        :param name: The name of the object
        :type name: str
        """
        return _ensure_obj_of_type(int, obj, name)

    @staticmethod
    def ensure_float(obj: ..., name: str = None) -> None:
        """Ensures the object is of type `float`.

        :param obj: The object to check
        :type obj: object
        :param name: The name of the object
        :type name: str
        """
        return _ensure_obj_of_type(float, obj, name)

    @staticmethod
    def ensure_complex(obj: ..., name: str = None) -> None:
        """Ensures the object is of type `float`.

        :param obj: The object to check
        :type obj: object
        :param name: The name of the object
        :type name: str
        """
        return _ensure_obj_of_type(complex, obj, name)

    @staticmethod
    def ensure_str(obj: ..., name: str = None) -> None:
        """Ensures the object is of type `str`.

        :param obj: The object to check
        :type obj: object
        :param name: The name of the object
        :type name: str
        """
        return _ensure_obj_of_type(str, obj, name)

    @staticmethod
    def ensure_bytes(obj: ..., name: str = None) -> None:
        """Ensures the object is of type `bytes`.

        :param obj: The object to check
        :type obj: object
        :param name: The name of the object
        :type name: str
        """
        return _ensure_obj_of_type(bytes, obj, name)

    @staticmethod
    def ensure_bytearray(obj: ..., name: str = None) -> None:
        """Ensures the object is of type `bytearray`.

        :param obj: The object to check
        :type obj: object
        :param name: The name of the object
        :type name: str
        """
        return _ensure_obj_of_type(bytearray, obj, name)

    @staticmethod
    def ensure_list(obj: ..., name: str = None) -> None:
        """Ensures the object is of type `list`.

        :param obj: The object to check
        :type obj: object
        :param name: The name of the object
        :type name: str
        """
        return _ensure_obj_of_type(list, obj, name)

    @staticmethod
    def ensure_tuple(obj: ..., name: str = None) -> None:
        """Ensures the object is of type `tuple`.

        :param obj: The object to check
        :type obj: object
        :param name: The name of the object
        :type name: str
        """
        return _ensure_obj_of_type(tuple, obj, name)

    @staticmethod
    def ensure_dict(obj: ..., name: str = None) -> None:
        """Ensures the object is of type `dict`.

        :param obj: The object to check
        :type obj: object
        :param name: The name of the object
        :type name: str
        """
        return _ensure_obj_of_type(dict, obj, name)

    @staticmethod
    def ensure_set(obj: ..., name: str = None) -> None:
        """Ensures the object is of type `set`.

        :param obj: The object to check
        :type obj: object
        :param name: The name of the object
        :type name: str
        """
        return _ensure_obj_of_type(set, obj, name)

    @staticmethod
    def ensure_frozenset(obj: ..., name: str = None) -> None:
        """Ensures the object is of type `frozenset`.

        :param obj: The object to check
        :type obj: object
        :param name: The name of the object
        :type name: str
        """
        return _ensure_obj_of_type(frozenset, obj, name)

    @staticmethod
    def ensure_generator(obj: ..., name: str = None) -> None:
        """Ensures the object is a generator.

        :param obj: The object to check
        :type obj: object
        :param name: The name of the object
        :type name: str
        """
        return _ensure_obj_of_type(GeneratorType, obj, name)

    @staticmethod
    def ensure_memoryview(obj: ..., name: str = None) -> None:
        """Ensures the object is of type `memoryview`.

        :param obj: The object to check
        :type obj: object
        :param name: The name of the object
        :type name: str
        """
        return _ensure_obj_of_type(memoryview, obj, name)

    @staticmethod
    def ensure_function(obj: ..., name: str = None) -> None:
        """Ensures the object is a function.

        :param obj: The object to check
        :type obj: object
        :param name: The name of the object
        :type name: str
        """
        return _ensure_obj_of_type(FunctionType, obj, name)
