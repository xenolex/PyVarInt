from io import BytesIO

import pytest

from src.VarInt import SQLite4VLI

PARAMS = [
    [b'\x00', 0],
    [b'\xf0', 240],
    [b'\xf1\x01', 241],
    [b'\xf1\x08', 248],
    [b'\xf1\t', 249],
    [b'\xf1\n', 250],
    [b'\xf1\x0b', 251],
    [b'\xf1\x0c', 252],
    [b'\xf1\r', 253],
    [b'\xf1\x0e',254],
    [b'\xf1\x0f', 255],
    [b'\xf1\x10', 256],
    [b'\xf8\xff', 2287],
    [b'\xf9\x00\x00', 2288],
    [b'\xf9\xff\xff', 67823],
    [b'\xfa\x01\x08\xf0', 67824],
    [b'\xfa\xff\xff\xff', 16777215],
    [b'\xfb\x01\x00\x00\x00', 16777216],
    [b'\xfb\xff\xff\xff\xff', 4294967295],
    [b'\xfc\x01\x00\x00\x00\x00', 4294967296],
    [b'\xfc\xff\xff\xff\xff\xff', 1099511627775],
    [b'\xfd\x01\x00\x00\x00\x00\x00', 1099511627776],
    [b'\xfd\xff\xff\xff\xff\xff\xff', 281474976710655],
    [b'\xfe\x01\x00\x00\x00\x00\x00\x00', 281474976710656],
    [b'\xfe\xff\xff\xff\xff\xff\xff\xff', 72057594037927935],
    [b'\xff\x01\x00\x00\x00\x00\x00\x00\x00', 72057594037927936],
]


@pytest.mark.parametrize("expected,integer", PARAMS)
def test_encode_sql_lite4_vli(expected, integer):
    assert SQLite4VLI.encode(integer) == bytearray(expected)


@pytest.mark.parametrize("byte, expected", PARAMS)
def test_decode_sql_lite4_vli(byte, expected):
    buffer = BytesIO(byte)
    assert SQLite4VLI.decode(buffer) == expected
