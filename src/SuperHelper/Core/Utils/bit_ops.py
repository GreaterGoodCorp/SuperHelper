# This module defines the BitOps class, a utility class for bitwise operations.
__all__ = ["BitOps"]


class BitOps:
    """
    A utility class for bitwise operations.
    """

    @staticmethod
    def is_bit_set(i: int, pos: int) -> bool:
        """Checks if the `pos`-th bit of the integer `i` is set.

        :param i: The integer to check
        :type i: int
        :param pos: The zero-indexed position of the bit (from LSB) to check
        :type pos: int
        :return: True if the specified bit is set, otherwise False
        :rtype: bool
        """
        return bool(i & (1 << pos))

    @staticmethod
    def set_bit(i: int, pos: int) -> int:
        """Sets the the `pos`-th bit of the integer `i`.

        :param i: The integer to modify
        :type i: int
        :param pos: The zero-indexed position of the bit (from LSB) to set
        :type pos: int
        :return: The integer with the specified bit set
        :rtype: int
        """
        if BitOps.is_bit_set(i, pos):
            return i
        else:
            return i + (1 << pos)

    @staticmethod
    def unset_bit(i: int, pos: int) -> int:
        """Unsets the the `pos`-th bit of the integer `i`.

        :param i: The integer to modify
        :type i: int
        :param pos: The zero-indexed position of the bit (from LSB) to unset
        :type pos: int
        :return: The integer with the specified bit unset
        :rtype: int
        """
        if not BitOps.is_bit_set(i, pos):
            return i
        else:
            return i - (1 << pos)
