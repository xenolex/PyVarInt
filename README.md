# Variable-Length Integer Encoding Schemes

This Python module provides implementations of various variable-length integer encoding schemes. These encoding methods are designed to efficiently store integers by using fewer bytes for smaller numbers while maintaining the ability to store larger numbers when needed.

## Features

- Multiple encoding schemes implemented:
  - PrefixVarint (WebAssembly-inspired)
  - Unsigned LEB128 (Little Endian Base 128)
  - Signed LEB128
  - Variable-Length Quantity (VLQ)
  - SQLite4 Variable-Length Integer (VLI)
  - LeSQLite (Little-endian SQLite variant)
  - LeSQLite2 (Alternative little-endian SQLite variant)
  - Unreal Engine Signed VLQ

## Installation

Clone this repository and run `./setup.sh` to install the module and its dependencies.

```bash
git clone https://github.com/xenolex/PyVarInt.git

./setup.sh
```


## Usage

Each encoding scheme is implemented as a separate class. All classes provide two static methods:
- `encode(value: int) -> bytes`: Encodes an integer into a byte sequence
- `decode(buffer: BinaryIO | bytes) -> int`: Decodes a byte sequence back into an integer

### Example

```python
from PyVarInt import PrefixVarint, UnsignedLEB128

# Encoding
encoded_prefix = PrefixVarint.encode(123)
encoded_leb128 = UnsignedLEB128.encode(123)

# Decoding
decoded_prefix = PrefixVarint.decode(encoded_prefix)
decoded_leb128 = UnsignedLEB128.decode(encoded_leb128)
```

## Encoding Schemes Details

### PrefixVarint
- Optimized for modern CPUs with fast unaligned loads
- Similar compression ratio to LEB128
- Length can be determined from the first byte
- Supports values up to 64 bits

### LEB128 (Unsigned and Signed)
- Little Endian Base 128 encoding
- Uses 7 bits per byte for data, 1 bit for continuation
- Widely used in various formats and protocols

### Variable-Length Quantity (VLQ)
- Used in MIDI file format
- Similar to LEB128 but with different byte ordering

### SQLite4 VLI
- Optimized for small integers (0-240 in one byte)
- Variable number of bytes based on value range
- Efficient storage for common integer values

### LeSQLite and LeSQLite2
- WebAssembly-optimized variants of SQLite encoding
- Little-endian optimization for better performance
- Different byte range allocations for various integer sizes

### Unreal Engine Signed VLQ
- Custom implementation for Unreal Engine
- Supports signed integers
- Variable-length encoding optimized for game data

## Performance Considerations

- Each encoding scheme has different trade-offs in terms of:
  - Encoding/decoding speed
  - Memory usage
  - Compression ratio
  - CPU architecture optimization

## Dependencies

The module requires Python 3.6+ and uses only standard library modules:
- `io.BytesIO`
- `math.ceil`
- `typing`