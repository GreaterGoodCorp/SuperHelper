class BitOps:
    @staticmethod
    def is_bit_set(i: int, pos: int) -> bool:
        return bool(i & (1 << pos))

    @staticmethod
    def set_bit(i: int, pos: int) -> int:
        if BitOps.is_bit_set(i, pos):
            return i
        else:
            return i + (1 << pos)

    @staticmethod
    def unset_bit(i: int, pos: int) -> int:
        if not BitOps.is_bit_set(i, pos):
            return i
        else:
            return i - (1 << pos)


__all__ = ["BitOps"]
