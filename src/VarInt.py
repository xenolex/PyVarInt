from typing import MutableSequence, BinaryIO

from src.utils import to_bytes


class Base:
    @staticmethod
    def encode(value) -> bytes:
        raise NotImplementedError

    @staticmethod
    def decode(buffer) -> int:
        raise NotImplementedError


class GroupVarintEncoding(Base):
    """
    Group Varint Encoding (GVE).
    """

    @staticmethod
    def decode(buffer: BinaryIO) -> int:
        """Group Varint Encoding"""
        pass


class PrefixVarint(Base):
    """
    Prefix Varint
    """


class UnsignedLEB128(Base):
    """
    Unsigned Little Endian Base 128 (LEB128)
    """

    @staticmethod
    def encode(value) -> bytes:
        """Encode a Unsigned Little Endian Base 128 (LEB128) from a buffer."""
        result = bytearray()
        while True:
            # Extract the lowest 7 bits
            byte = value & 0x7F
            # Right shift the value by 7 bits
            value >>= 7
            # If there's more data to encode, set the high bit
            if value != 0:
                byte |= 0x80

            result.append(byte)

            if value == 0:
                break

        return bytes(result)

    @staticmethod
    def decode(buffer: BinaryIO) -> int:
        """Decode a Unsigned Little Endian Base 128 (LEB128) from a buffer."""
        shift = 0
        result = 0

        while True:
            i = ord(buffer.read(1))
            result |= (i & 0x7f) << shift
            shift += 7
            if not (i & 0x80):
                break

        return result


class SignedLEB128(Base):
    """
    Signed Little Endian Base 128 (LEB128)
    https://en.wikipedia.org/wiki/LEB128
    """

    @staticmethod
    def encode(value: int) -> bytes:
        """Encode a signed integer using LEB128 encoding."""
        result = bytearray()
        while True:
            byte = value & 0x7f
            value >>= 7
            # Sign extension
            if value == 0 and byte & 0x40 == 0:
                result.append(byte)
                break
            elif value == -1 and byte & 0x40 != 0:
                result.append(byte)
                break
            else:
                result.append(byte | 0x80)
        return bytes(result)

    @staticmethod
    def decode(buffer: BinaryIO) -> int:
        """Decode a Signed Little Endian Base 128 (LEB128) from a buffer."""
        result = 0
        shift = 0

        while True:
            item = ord(buffer.read(1))
            result |= (item & 0x7F) << shift
            # Check if this is the last byte
            if not (item & 0x80):
                # Sign extend if necessary
                if shift < 64 and (item & 0x40):
                    result |= ~0 << (shift + 7)
                break
            shift += 7
        return result


class VariableLengthQuantity(Base):
    """
    Variable-Length Quantity (VLQ)

    https://en.wikipedia.org/wiki/Variable-length_quantity
    """

    @staticmethod
    def encode(value) -> bytes:
        """Encode a variable-length quantity."""
        tmp_arr = []
        buffer = value & 0x7f
        tmp_arr.append(buffer)
        while value := value >> 7:
            buffer = (value & 0x7f) | 0x80
            tmp_arr.append(buffer)

        return b''.join(to_bytes(i) for i in tmp_arr[::-1])

    @staticmethod
    def decode(buffer: BinaryIO) -> int:
        """Decode a variable-length quantity from a buffer."""
        tmp_arr: MutableSequence = []
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


class SQLite4VLI(Base):
    """
    SQLite4 Variable-Length Integer (VLI).

    https://sqlite.org/src4/doc/trunk/www/varint.wiki
    """

    @staticmethod
    def encode(value) -> bytes:
        """Encode a SQLite4 variable-length integer."""

        def _add_bytes(number: int, num_bytes: int) -> bytes:
            b = b''
            for i in range(num_bytes * 8 - 8, -8, -8):
                b += to_bytes((number >> i) & 0xFF)
            return b

        if value <= 240:
            return to_bytes(value)
        if value <= 2287:
            return to_bytes(241 + (value - 240) // 256) + to_bytes((value - 240) % 256)
        if value <= 67823:
            return to_bytes(249) + to_bytes((value - 2288) // 256) + to_bytes((value - 2288) % 256)
        if value <= 16777215:
            return to_bytes(250) + _add_bytes(value, num_bytes=3)
        if value <= 4294967295:
            return to_bytes(251) + _add_bytes(value, num_bytes=4)
        if value <= 1099511627775:
            return to_bytes(252) + _add_bytes(value, num_bytes=5)
        if value <= 281474976710655:
            return to_bytes(253) + _add_bytes(value, num_bytes=6)
        if value <= 72057594037927935:
            return to_bytes(254) + _add_bytes(value, num_bytes=7)
        return to_bytes(255) + _add_bytes(value, num_bytes=8)

    @staticmethod
    def decode(buffer: BinaryIO) -> int:
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
        return int.from_bytes(buffer.read(8), 'big')


class LeSQLite(Base):
    """
    The SQLite variable-length integer encoding is biased towards integer distributions with more
    small numbers. It can encode the integers 0-240 in one byte.

    The encoding implemented here is modified for better performance with WebAssembly (little-endian SQLite).
    The first byte, B0 determines the encoding:

    0-184   1 byte    value = B0
    185-248 2 bytes   value = 185 + 256 * (B0 - 185) + B1
    249-255 3-9 bytes value = (B0 - 249 + 2) little-endian bytes following B0.
    This encoding packs more than 7 bits into 1 byte and a bit more than 14 bits into 2 bytes.
    This has a cost in encoding size since the 3-byte encoding only holds 16 bits.
    The 3+ byte encoded numbers are very fast to decode with an unaligned load instruction.
    """

    @staticmethod
    def encode(value) -> bytes:
        """Encode a leSQLite variable-length integer."""

        if value <= 184:
            return to_bytes(value)
        if value <= 16559:
            adjusted = value - 185
            return to_bytes(185 + adjusted // 256) + to_bytes(adjusted % 256)

        if value <= 65535:
            length = 2  # 16 bits
        elif value <= 16777215:
            length = 3  # 24 bits
        elif value <= 4294967295:
            length = 4  # 32 bits
        elif value <= 1099511627775:
            length = 5  # 40 bits
        elif value <= 281474976710655:
            length = 6  # 48 bits
        elif value <= 72057594037927935:
            length = 7  # 56 bits
        else:
            length = 8  # 64 bits

        result = bytearray()
        # First byte indicates the number of following bytes
        result.append(249 + length - 2)

        # Add the value bytes in little-endian order
        for i in range(length):
            result.append(value & 0xFF)
            value >>= 8

        return bytes(result)

    @staticmethod
    def decode(buffer: BinaryIO) -> int:
        """Decode a leSQLite variable-length integer from a buffer."""
        value = ord(buffer.read(1))
        if value <= 184:
            return value
        if value <= 248:
            return 185 + 256 * (value - 185) + ord(buffer.read(1))
        return int.from_bytes(buffer.read(value - 249 + 2), 'little')


class LeSQLite2(Base):
    """
    A second variation of the SQLite-inspired encoding has a smoother bump between
    the 2-byte and 3-byte encodings. It divides the values of the first byte into 4 ranges:

    The value of a 1-byte encoding.
    The high 6 bits of a 2-byte encoding.
    The high 3 bits of a 3-byte encoding.
    The number of bytes in a 4-9 byte encoding.
    The ranges are assigned like this:

    B0	Values	Formula
    0-177	177	B0
    178-241	2^14	178 + ((B0-178) << 8) + B[1]
    242-249	2^19	16562 + ((B0-242) << 16) + B[1..2]
    250-255	2^24..2^64	B0 - 250 + 3 little-endian bytes.
    This variant is a bit slower to decode than the first one because there are more cases.
    """

    @staticmethod
    def encode(value) -> bytes:
        """Encode a leSQLite2 variable-length integer."""

        if value <= 177:
            return to_bytes(value)
        if value <= 16561:
            adjusted = value - 178
            return to_bytes(178 + (adjusted >> 8)) + to_bytes(adjusted & 0xFF)

        if value <= 524287:
            adjusted = value - 16562
            return to_bytes(242 + (adjusted >> 16)) + to_bytes((adjusted >> 8) & 0xFF) + to_bytes(
                adjusted & 0xFF)

        if value <= 16777215:
            length = 3  # 24 bits
        elif value <= 4294967295:
            length = 4  # 32 bits
        elif value <= 1099511627775:
            length = 5  # 40 bits
        elif value <= 281474976710655:
            length = 6  # 48 bits
        elif value <= 72057594037927935:
            length = 7  # 56 bits
        else:
            length = 8  # 64 bits

        result = bytearray()
        # First byte indicates length
        result.append(250 + length - 3)

        # Add value bytes in little-endian order
        for i in range(length):
            result.append(value & 0xFF)
            value >>= 8

        return bytes(result)

    @staticmethod
    def decode(buffer: BinaryIO) -> int:
        """Decode a leSQLite2 variable-length integer from a buffer."""
        value = ord(buffer.read(1))
        if value <= 177:
            return value
        if value <= 241:
            return 178 + ((value - 178) << 8) + ord(buffer.read(1))
        if value <= 249:
            return 16562 + ((value - 242) << 16) + (ord(buffer.read(1)) << 8) + ord(buffer.read(1))
        return int.from_bytes(buffer.read(value - 250 + 3), 'little')


class UnrealEngineSingedVLQ(Base):
    """
    Unreal Engine signed variable-length quantity.

    https://web.archive.org/web/20100820185656/http://unreal.epicgames.com/Packages.htm#:~:
    text=a%20package%20file.-,Compact%20Indices.,-Compact%20indices%20exist
    """

    @staticmethod
    def encode(value: int) -> bytes:
        """Encode an Unreal Engine signed variable-length quantity."""
        b = b''
        abs_value = abs(value)
        b0 = ((0 if value >= 0 else 0x80) +
              (abs_value if abs_value < 0x40 else ((abs_value & 0x3F) + 0x40)))
        b += to_bytes(b0)

        if b0 & 0x40:
            abs_value >>= 6
            b1 = (abs_value if abs_value < 0x80 else ((abs_value & 0x7F) + 0x80))
            b += to_bytes(b1)
            if b1 & 0x80:
                abs_value >>= 7
                b2 = (abs_value if abs_value < 0x80 else ((abs_value & 0x7F) + 0x80))
                b += to_bytes(b2)
                if b2 & 0x80:
                    abs_value >>= 7
                    b3 = (abs_value if abs_value < 0x80 else ((abs_value & 0x7F) + 0x80))
                    b += to_bytes(b3)
                    if b3 & 0x80:
                        abs_value >>= 7
                        b4 = abs_value
                        b += to_bytes(b4)

        return b

    @staticmethod
    def decode(buffer: BinaryIO) -> int:
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
