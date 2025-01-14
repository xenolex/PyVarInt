from io import BytesIO

import pytest

from PyVarInt.algorithms import UnrealEngineSingedVLQ

PARAMS = [
    [b'\xff\xff\xff\xff\xff', -34359738367],
    [b'\xc0\x80\x80\x80 ', -4294967296],
    [b'\xc1\x80\x80\x80 ', -4294967297],
    [b'\xc0\x80\x80\x80\x10', -2147483648],
    [b'\xff\xff\xff\xff\x0f', -2147483647],
    [b'\xc0\x80\x80\x80\x01', -134217728],
    [b'\xff\xff\xff\x7f', -134217727],
    [b'\xc0\x80\x80@', -67108864],
    [b'\xff\xff\xff?', -67108863],
    [b'\xc0\x80\x80\x01', -1048576],
    [b'\xff\xff\x7f', -1048575],
    [b'\xd8\xc3\x06', -53464],
    [b'\xd7\xc3\x06', -53463],
    [b'\xc0\x80\x01', -8192],
    [b'\xff\x7f', -8191],
    [b'\xc0@', -4096],
    [b'\xff?', -4095],
    [b'\xe6\x02', -166],
    [b'\xe5\x02', -165],
    [b'\xca\x01', -74],
    [b'\xc9\x01', -73],
    [b'\xc0\x01', -64],
    [b'\xbf', -63],
    [b'\x00', 0],
    [b'?', 63],
    [b'@\x01', 64],
    [b'I\x01', 73],
    [b'J\x01', 74],
    [b'e\x02', 165],
    [b'f\x02', 166],
    [b'\x7f?', 4095],
    [b'@@', 4096],
    [b'\x7f\x7f', 8191],
    [b'@\x80\x01', 8192],
    [b'W\xc3\x06', 53463],
    [b'X\xc3\x06', 53464],
    [b'\x7f\xff\x7f', 1048575],
    [b'@\x80\x80\x01', 1048576],
    [b'\x7f\xff\xff?', 67108863],
    [b'@\x80\x80@', 67108864],
    [b'\x7f\xff\xff\xff\x0f', 2147483647],
    [b'@\x80\x80\x80\x10', 2147483648],
    [b'A\x80\x80\x80 ', 4294967297],
    [b'@\x80\x80\x80 ', 4294967296],
    [b'\x7f\xff\xff\xff\xff', 34359738367],
]


@pytest.mark.parametrize("expected,integer", PARAMS)
def test_encode_unreal_signed_vlq(expected, integer):
    assert UnrealEngineSingedVLQ.encode(integer) == expected


@pytest.mark.parametrize("byte, expected", PARAMS)
def test_decode_unreal_signed_vlq(byte, expected):
    buffer = BytesIO(byte)
    assert UnrealEngineSingedVLQ.decode(buffer) == expected
