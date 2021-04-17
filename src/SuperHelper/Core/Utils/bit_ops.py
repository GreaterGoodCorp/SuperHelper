# This module defines the BitOps class, a utility class for bitwise operations.
__all__ = ["BitOps"]


class BitOps:
    """A utility class for bitwise operations."""

    @staticmethod
    def is_bit_set(i: int, pos: int) -> bool:
        """Checks if the `pos`-th bit of the integer `i` is set.

        Args:
            i (int): The integer to check.
            pos (int): The zero-indexed position of the bit (from LSB) to check.

        Returns:
            True if the specified bit is set, otherwise False
        """
        return bool(i & (1 << pos))

    @staticmethod
    def set_bit(i: int, pos: int) -> int:
        """Sets the the `pos`-th bit of the integer `i`.

        Args:
            i (int): The integer to modify.
            pos (int): The zero-indexed position of the bit (from LSB) to set.

        Returns:
            The integer with the specified bit set.
        """
        if BitOps.is_bit_set(i, pos):
            return i
        else:
            return i + (1 << pos)

    @staticmethod
    def unset_bit(i: int, pos: int) -> int:
        """Unsets the the `pos`-th bit of the integer `i`.

        Args:
            i (int): The integer to modify.
            pos (int): The zero-indexed position of the bit (from LSB) to unset.

        Returns:
            The integer with the specified bit unset.
        """
        if not BitOps.is_bit_set(i, pos):
            return i
        else:
            return i - (1 << pos)
