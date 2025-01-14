from io import BytesIO

import pytest

from PyVarInt.algorithms import PrefixVarint

PARAMS = [
    [b'\x01', 0],
    [b'\xff', 127],
    [b'\xe2\x02', 184],
    [b'\xe2\x03', 248],
    [b'\xc2#', 2288],
    [b'\xfc\xff\x07', 65535],
    [b'\xf8\xff\xff\x0f', 16777215],
    [b'\xf0\xff\xff\xff\x1f', 4294967295],
    [b'\xc0\xff\xff\xff\xff\xff\x7f', 281474976710655],
    [b'\x80\xff\xff\xff\xff\xff\xff\xff', 72057594037927935],
    [b'\x00\x00\x00\x00\x00\x00\x00\x00\x01', 72057594037927936]
]


@pytest.mark.parametrize("expected,integer", PARAMS)
def test_encode_prefix_varint(expected, integer):
    assert PrefixVarint.encode(integer) == expected


@pytest.mark.parametrize("byte, expected", PARAMS)
def test_decode_prefix_varint(byte, expected):
    buffer = BytesIO(byte)
    assert PrefixVarint.decode(buffer) == expected
