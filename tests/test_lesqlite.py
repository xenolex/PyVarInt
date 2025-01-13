from io import BytesIO

import pytest

from src.algorithms import LeSQLite

PARAMS = [
    [b'\x00', 0],
    [b'\xb8', 184],
    [b'\xb9?', 248],
    [b'\xc17', 2288],
    [b'\xf9\xff\xff', 65535],
    [b'\xfa\xff\xff\xff', 16777215],
    [b'\xfb\xff\xff\xff\xff', 4294967295],
    [b'\xfd\xff\xff\xff\xff\xff\xff', 281474976710655],
    [b'\xfe\xff\xff\xff\xff\xff\xff\xff', 72057594037927935],
    [b'\xff\x00\x00\x00\x00\x00\x00\x00\x01', 72057594037927936]
]


@pytest.mark.parametrize("expected,integer", PARAMS)
def test_encode_lesqlite(expected, integer):
    assert LeSQLite.encode(integer) == expected


@pytest.mark.parametrize("byte, expected", PARAMS)
def test_decode_lesqlite(byte, expected):
    buffer = BytesIO(byte)
    assert LeSQLite.decode(buffer) == expected
