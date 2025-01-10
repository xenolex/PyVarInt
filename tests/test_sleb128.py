from io import BytesIO

import pytest

from src.VarInt import SignedLEB128

PARAMS = [
    [b'\x80\x80\x80\x80\x80\x80\x80\x80\x7f', -72057594037927936],
    [b'\x80\x80\x80\x80\x7f', -268435456],
    [b'\x9b\xf1Y', -624485],
    [b'\xc0\xbb\x78', -123456],
    [b'\xff\x7e', -129],
    [b'\x80\x7f', -128],
    [b'\x81\x7f', -127],
    [b'\x7e',-2],
    [b'\x00', 0],
    [b'\xff\x00', 127],
    [b'\x80\x01', 128],
    [b'\xe5\x8e\x26', 624485],
    [b'\x80\x80\x80\x80\x01', 268435456],
    [b'\x80\x80\x80\x80\x80\x80\x80\x80\x01', 72057594037927936],

]


@pytest.mark.parametrize("byte,expected", PARAMS)
def test_decode_sleb128(byte, expected):
    buffer = BytesIO(byte)
    assert SignedLEB128.decode(buffer) == expected

@pytest.mark.parametrize("expected,byte", PARAMS)
def test_encode_sleb128(byte, expected):
    assert SignedLEB128.encode(byte) == expected
