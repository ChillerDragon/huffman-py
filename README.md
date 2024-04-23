# huffman-py

Teeworlds huffman compression ported to python. Work in progress.

This is not a general purpose compression library. It uses the teeworlds frequency table
and is intended to be used for teeworlds networking.

## example usage

```python
from huffman import Huffman

huffman = Huffman()
decompressed = huffman.decompress(bytes([174, 149, 19, 92, 9, 87, 194, 22, 177, 86, 220, 218, 34, 56, 185, 18, 156, 168, 184, 1]))
print(decompressed) # => b'hello world'
```

## similar projects

- teeworlds huffman (ruby) https://github.com/ChillerDragon/huffman-tw
- teeworlds huffman (rust) https://github.com/edg-l/rustyman

