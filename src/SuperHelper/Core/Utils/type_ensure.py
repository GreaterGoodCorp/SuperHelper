from typing import NoReturn
from types import FunctionType, GeneratorType


def _is_obj_of_type(t: type, obj: ...) -> bool:
    return type(obj) == t


def _raise_type_error(t: type, obj: ..., name: str) -> NoReturn:
    if name is not None:
        raise TypeError(f"The expected type of '{name}' is {t.__name__} (given '{type(obj).__name__}' instead)")
    else:
        raise TypeError(f"The expected type is {t.__name__} (given '{type(obj).__name__}' instead)")


def _raise_on_failure(b: bool, t: type, obj: ..., name: str) -> None:
    return _raise_type_error(t, obj, name) if not b else None


def _ensure_obj_of_type(t: type, obj: ..., name: str = None) -> None:
    return _raise_on_failure(_is_obj_of_type(t, obj), t, obj, name)


class TypeCheck:
    @staticmethod
    def ensure_custom(t: type, obj: ..., name: str = None) -> None:
        return _ensure_obj_of_type(t, obj, name)

    @staticmethod
    def ensure_int(obj: ..., name: str = None) -> None:
        return _ensure_obj_of_type(int, obj, name)

    @staticmethod
    def ensure_float(obj: ..., name: str = None) -> None:
        return _ensure_obj_of_type(float, obj, name)

    @staticmethod
    def ensure_complex(obj: ..., name: str = None) -> None:
        return _ensure_obj_of_type(complex, obj, name)

    @staticmethod
    def ensure_str(obj: ..., name: str = None) -> None:
        return _ensure_obj_of_type(str, obj, name)

    @staticmethod
    def ensure_bytes(obj: ..., name: str = None) -> None:
        return _ensure_obj_of_type(bytes, obj, name)

    @staticmethod
    def ensure_bytearray(obj: ..., name: str = None) -> None:
        return _ensure_obj_of_type(bytearray, obj, name)

    @staticmethod
    def ensure_list(obj: ..., name: str = None) -> None:
        return _ensure_obj_of_type(list, obj, name)

    @staticmethod
    def ensure_tuple(obj: ..., name: str = None) -> None:
        return _ensure_obj_of_type(tuple, obj, name)

    @staticmethod
    def ensure_dict(obj: ..., name: str = None) -> None:
        return _ensure_obj_of_type(dict, obj, name)

    @staticmethod
    def ensure_set(obj: ..., name: str = None) -> None:
        return _ensure_obj_of_type(set, obj, name)

    @staticmethod
    def ensure_frozenset(obj: ..., name: str = None) -> None:
        return _ensure_obj_of_type(frozenset, obj, name)

    @staticmethod
    def ensure_generator(obj: ..., name: str = None) -> None:
        return _ensure_obj_of_type(GeneratorType, obj, name)

    @staticmethod
    def ensure_memoryview(obj: ..., name: str = None) -> None:
        return _ensure_obj_of_type(memoryview, obj, name)

    @staticmethod
    def ensure_function(obj: ..., name: str = None) -> None:
        return _ensure_obj_of_type(FunctionType, obj, name)
