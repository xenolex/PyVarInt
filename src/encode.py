from typing import BinaryIO


def gve(buffer: BinaryIO) -> int:
    """Group Varint Encoding"""
    pass


def sql_lite4_vli(value: int) -> bytearray:
    """Encode a SQLite4 variable-length integer.
    https://sqlite.org/src4/doc/trunk/www/varint.wiki
    """

    def _add_bytes(value: int, num_bytes: int) -> list[int]:
        arr = []
        for i in range((num_bytes) * 8 - 8, -8, -8):
            arr.append((value >> i) & 0xFF)
        return arr

    if value <= 240:
        return bytearray([value])
    if value <= 2287:
        return bytearray([241 + (value - 240) // 256, (value - 240) % 256])
    if value <= 67823:
        return bytearray([249, (value - 2288) // 256, (value - 2288) % 256])
    if value <= 16777215:
        return bytearray([250] + _add_bytes(value, num_bytes=3))
    if value <= 4294967295:
        return bytearray([251] + _add_bytes(value, num_bytes=4))
    if value <= 1099511627775:
        return bytearray([252] + _add_bytes(value, num_bytes=5))
    if value <= 281474976710655:
        return bytearray([253] + _add_bytes(value, num_bytes=6))
    if value <= 72057594037927935:
        return bytearray([254] + _add_bytes(value, num_bytes=7))
    return bytearray([255] + _add_bytes(value, num_bytes=8))


def unreal_signed_vlq(value: int) -> bytearray:
    """Encode an Unreal Engine signed variable-length quantity."""
    arr = bytearray()
    abs_value = abs(value)
    b0 = ((0 if value >= 0 else 0x80) +
          (abs_value if abs_value < 0x40 else ((abs_value & 0x3F) + 0x40)))
    arr.append(b0)

    if b0 & 0x40:
        abs_value >>= 6
        b1 = (abs_value if abs_value < 0x80 else ((abs_value & 0x7F) + 0x80))
        arr.append(b1)
        if b1 & 0x80:
            abs_value >>= 7
            b2 = (abs_value if abs_value < 0x80 else ((abs_value & 0x7F) + 0x80))
            arr.append(b2)
            if b2 & 0x80:
                abs_value >>= 7
                b3 = (abs_value if abs_value < 0x80 else ((abs_value & 0x7F) + 0x80))
                arr.append(b3)
                if b3 & 0x80:
                    abs_value >>= 7
                    b4 = abs_value
                    arr.append(b4)

    return arr
