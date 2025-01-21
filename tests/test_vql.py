from io import BytesIO

import pytest

from PyVarInt.algorithms import VariableLengthQuantity

PARAMS = [
    [b'\x00', 0],
    [b'\x7f', 127],
    [b'\x81\x00', 128],
    [b'\x81\t', 137],
    [b'\x82\x66', 358],
    [b'\xc0\x00', 8192],
    [b'\xff\x7f', 16383],
    [b'\x81\x80\x00', 16384],
    [b'\x86\xc3\x17', 106903],
    [b'\xff\xff\x7f', 2097151],
    [b'\x81\x80\x80\x00', 2097152],
    [b'\xc0\x80\x80\x00', 134217728],
    [b'\xff\xff\xff\x7f', 268435455],
    [b'\x81\x80\x80\x80\x00', 268435456],
    [b'\x81\x80\x80\x80\x80\x80\x80\x80\x00', 72057594037927936]
]


@pytest.mark.parametrize("byte,expected", PARAMS)
def test_decode_vlq(byte, expected):
    buffer = BytesIO(byte)
    assert VariableLengthQuantity.decode(buffer) == expected
    assert VariableLengthQuantity.decode(byte) == expected


@pytest.mark.parametrize("expected,integer", PARAMS)
def test_encode_vlq(expected, integer):
    assert VariableLengthQuantity.encode(integer) == expected
