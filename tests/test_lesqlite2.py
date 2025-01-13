from io import BytesIO

import pytest

from src.algorithms import LeSQLite2

PARAMS = [
    [b'\x00', 0],
    [b'\xb1', 177],
    [b'\xb2\x00', 178],
    [b'\xf1\xff', 16561],
    [b'\xf2\x00\x00', 16562],
    [b'\xf9\xbfM', 524287],
    [b'\xfa\x00\x00\x08', 524288],
    [b'\xfb\xff\xff\xff\xff', 4294967295],
    [b'\xfc\xff\xff\xff\xff\xff', 1099511627775],
    [b'\xfd\xff\xff\xff\xff\xff\xff', 281474976710655],
    [b'\xfe\xff\xff\xff\xff\xff\xff\xff', 72057594037927935],
    [b'\xff\x00\x00\x00\x00\x00\x00\x00\x01', 72057594037927936]
]


@pytest.mark.parametrize("expected,integer", PARAMS)
def test_encode_lesqlite2(expected, integer):
    assert LeSQLite2.encode(integer) == expected


@pytest.mark.parametrize("byte, expected", PARAMS)
def test_decode_lesqlite2(byte, expected):
    buffer = BytesIO(byte)
    assert LeSQLite2.decode(buffer) == expected
