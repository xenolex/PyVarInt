from typing_extensions import BinaryIO


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

class UnsignedLEB128(Base):
    """
    Unsigned Little Endian Base 128 (LEB128)
    """

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
    """
    pass

    # @staticmethod
    # def decode(buffer: BinaryIO) -> int:
    #     """Decode a Signed Little Endian Base 128 (LEB128) from a buffer."""
    #     shift = 0
    #     result = 0
    #     while True:
    #         i = ord(buffer.read(1))
    #         result |= (i & 0x7f) << shift
    #         shift += 7
    #         if not (i & 0x80):
    #             break
    #
    #     if (i & 0x40) and (shift < 8 * 4):
    #         result |= - (1 << shift)
    #
    #     return result

class VariableLengthQuantity(Base):
    """
    Variable-Length Quantity (VLQ)
    """

    @staticmethod
    def decode(buffer: BinaryIO) -> bytes:
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


class SQLite4VLI(Base):
    """
    SQLite4 Variable-Length Integer (VLI).

    https://sqlite.org/src4/doc/trunk/www/varint.wiki
    """

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
        if value == 255:
            return int.from_bytes(buffer.read(8), 'big')

    @staticmethod
    def encode(value) -> bytes:
        """Encode a SQLite4 variable-length integer."""

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


class UnrealEngineSingedVLQ(Base):
    """
    Unreal Engine signed variable-length quantity.
    """

    @staticmethod
    def encode(value: int) -> bytearray:
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
