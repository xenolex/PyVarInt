from typing import BinaryIO


def gve(buffer: BinaryIO) -> int:
    """Group Varint Encoding"""
    pass


def unreal_signed_vlq(value: int) -> bytes:
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
