def to_bytes(value: int) -> bytes:
    return value.to_bytes(length=1, byteorder='big')
