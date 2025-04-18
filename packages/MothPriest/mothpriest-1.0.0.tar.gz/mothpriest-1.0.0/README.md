# MothPriest

Python module for creating intuitive file parsers.

Imagine you have a file with the following structure:

| Field | Size (Bytes) | Value |
|----------|----------|----------|
| Magic | 6 | "STRING" |
| StringSize | 4 | uint32 (little endian) size String in bytes |
| String | StringSize | string data for this file |

MothPriest makes parsing and editing this file simple:

```Python
from io import BytesIO
from mothpriest.parsers import *

parser = BlockParser(
    "root",
    [
        MagicParser("STRING", "Magic"),
        IntegerParser("StringSize", size=4, little_endian=True, signed=False),
        StringParser("String", size="StringSize") # Note the reference back to StringSize
    ]
)

data = b"STRING\x1A\x00\x00\x00Lorem ipsum dolor sit amet"
with BytesIO(data) as buffer:
    parser(buffer)

assert parser['String'] == "Lorem ipsum dolor sit amet"

parser['String'] = "The quick brown fox jumps over the lazy dog"
# StringSize is now inconsistent with String, but there is no need to manually update

with BytesIO() as buffer:
    parser.unparse(buffer)
    buffer.seek(0)
    output_data = buffer.read()

# Note how StringSize is updated automatically
assert output_data == b"STRING\x2B\x00\x00\x00The quick brown fox jumps over the lazy dog"
```
