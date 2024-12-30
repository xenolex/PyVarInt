from io import BytesIO

import pytest

from src.VarInt import UnsignedLEB128

PARAMS = [
    [b'\x00', 0],
    [b'\x7f', 127],
    [b'\x80\x01', 128],
    [b'\xe5\x8e\x26', 624485],
    [b'\x80\x80\x80\x80\x01', 268435456],
    [b'\x80\x80\x80\x80\x80\x80\x80\x80\x01', 72057594037927936],

]


@pytest.mark.parametrize("byte,expected", PARAMS)
def test_decode_uleb128(byte, expected):
    buffer = BytesIO(byte)
    assert UnsignedLEB128.decode(buffer) == expected


@pytest.mark.parametrize("expected, integer", PARAMS)
def test_encode_uleb128(integer, expected):
    assert UnsignedLEB128.encode(integer) == expected
