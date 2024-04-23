from huffman import Huffman

def test_huffman():
    huffman = Huffman()
    compressed = b'\x4a\x42\x88\x4a\x6e\x16\xba\x31\x46\xa2\x84\x9e\xbf\xe2\x06'
    decompressed = huffman.decompress(compressed)
    expected = b'\x40\x02\x02\x02\x00\x40\x07\x03\x22\x01\x00\x01\x00\x01\x08\x40\x01\x04\x0b'
    assert decompressed == expected

def test_huffman_hello_world():
    huffman = Huffman()
    compressed = bytes([174, 149, 19, 92, 9, 87, 194, 22, 177, 86, 220, 218, 34, 56, 185, 18, 156, 168, 184, 1])
    decompressed = huffman.decompress(compressed)
    expected = b'hello world'
    assert decompressed == expected

def test_huffman_hello_world_compress():
    huffman = Huffman()
    compressed = huffman.compress(b'hello world')
    expected = bytes([174, 149, 19, 92, 9, 87, 194, 22, 177, 86, 220, 218, 34, 56, 185, 18, 156, 168, 184, 1])
    assert compressed == expected

def test_huffman_A():
    huffman = Huffman()
    compressed = bytes([188, 21, 55, 0])
    decompressed = huffman.decompress(compressed)
    expected = b'A'
    assert decompressed == expected

