# huffman-py

Teeworlds huffman compression ported to python.

This is not a general purpose compression library. It uses the teeworlds frequency table
and is intended to be used for teeworlds networking.

## example usage

```python
from huffman import Huffman

huffman = Huffman()
decompressed = huffman.decompress(bytes([
    174, 149, 19, 92, 9, 87, 194,
    22, 177, 86, 220, 218, 34, 56,
    185, 18, 156, 168, 184, 1
]))
print(decompressed)
# => b'hello world'

compressed = huffman.compress(b'hello world')
print(compressed)
# => b'\xae\x95\x13\\\tW\xc2\x16\xb1V\xdc\xda"8\xb9\x12\x9c\xa8\xb8\x01'
```

## similar projects

- teeworlds huffman (ruby) https://github.com/ChillerDragon/huffman-tw
- teeworlds huffman (rust) https://github.com/edg-l/rustyman

