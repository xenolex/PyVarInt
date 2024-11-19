from typing import BinaryIO


def vlq(buffer: BinaryIO) -> int:
    """Decode a variable-length quantity from a buffer."""
    tmp_arr = []
    result = 0
    while True:
        i = ord(buffer.read(1))
        tmp_arr.append(i & 0x7f)
        if not (i & 0x80):
            break
    for shift, item in enumerate(tmp_arr[::-1]):
        tmp_arr[shift] = item << shift * 7
    for item in tmp_arr:
        result |= item
    return result


def sql_lite4_vli(buffer: BinaryIO) -> int:
    """Decode a SQLite4 variable-length integer from a buffer."""
    value = ord(buffer.read(1))
    if value <= 240:
        return value
    if value <= 248:
        return 240 + 256 * (value - 241) + ord(buffer.read(1))
    if value == 249:
        return 2288 + 256 * ord(buffer.read(1)) + ord(buffer.read(1))
    if value == 250:
        return int.from_bytes(buffer.read(3), 'big')
    if value == 251:
        return int.from_bytes(buffer.read(4), 'big')
    if value == 252:
        return int.from_bytes(buffer.read(5), 'big')
    if value == 253:
        return int.from_bytes(buffer.read(6), 'big')
    if value == 254:
        return int.from_bytes(buffer.read(7), 'big')
    if value == 255:
        return int.from_bytes(buffer.read(8), 'big')


def unreal_signed_vlq(buffer: BinaryIO) -> int:
    """Decode an Unreal Engine signed variable-length quantity from a buffer."""
    value = 0
    b0 = ord(buffer.read(1))
    if b0 & 0x40:
        b1 = ord(buffer.read(1))
        if b1 & 0x80:
            b2 = ord(buffer.read(1))
            if b2 & 0x80:
                b3 = ord(buffer.read(1))
                if b3 & 0x80:
                    value = ord(buffer.read(1))
                value = (value << 7) + (b3 & 0x7F)
            value = (value << 7) + (b2 & 0x7F)
        value = (value << 7) + (b1 & 0x7F)
    value = (value << 6) + (b0 & 0x3F)

    return -value if b0 & 0x80 else value


def leb128(buffer: BinaryIO) -> int:
    pass


def uleb128(buffer: BinaryIO) -> int:
    """Decode an unsigned little-endian base-128 integer from a buffer."""
    shift = 0
    result = 0
    while True:
        i = ord(buffer.read(1))
        result |= (i & 0x7f) << shift
        shift += 7
        if not (i & 0x80):
            break

    return result
