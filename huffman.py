#!/usr/bin/env python3

import functools

from typing import Optional

FREQUENCY_TABLE = [
	1 << 30,4545,2657,431,1950,919,444,482,2244,617,838,542,715,1814,304,240,754,212,647,186,
	283,131,146,166,543,164,167,136,179,859,363,113,157,154,204,108,137,180,202,176,
	872,404,168,134,151,111,113,109,120,126,129,100,41,20,16,22,18,18,17,19,
	16,37,13,21,362,166,99,78,95,88,81,70,83,284,91,187,77,68,52,68,
	59,66,61,638,71,157,50,46,69,43,11,24,13,19,10,12,12,20,14,9,
	20,20,10,10,15,15,12,12,7,19,15,14,13,18,35,19,17,14,8,5,
	15,17,9,15,14,18,8,10,2173,134,157,68,188,60,170,60,194,62,175,71,
	148,67,167,78,211,67,156,69,1674,90,174,53,147,89,181,51,174,63,163,80,
	167,94,128,122,223,153,218,77,200,110,190,73,174,69,145,66,277,143,141,60,
	136,53,180,57,142,57,158,61,166,112,152,92,26,22,21,28,20,26,30,21,
	32,27,20,17,23,21,30,22,22,21,27,25,17,27,23,18,39,26,15,21,
	12,18,18,27,20,18,15,19,11,17,33,12,18,15,19,18,16,26,17,18,
	9,10,25,22,22,17,20,16,6,16,15,20,14,18,24,335,1517 ]

HUFFMAN_EOF_SYMBOL = 256

HUFFMAN_MAX_SYMBOLS=HUFFMAN_EOF_SYMBOL+1
HUFFMAN_MAX_NODES=HUFFMAN_MAX_SYMBOLS*2-1

HUFFMAN_LUTBITS = 10
HUFFMAN_LUTSIZE = (1<<HUFFMAN_LUTBITS)
HUFFMAN_LUTMASK = (HUFFMAN_LUTSIZE-1)

class HuffmanConstructNode:
    def __init__(self, node_id, frequency):
        self.node_id = node_id
        self.frequency = frequency

def compare_nodes_by_frequency_desc(node1: HuffmanConstructNode, node2: HuffmanConstructNode) -> bool:
    return node2.frequency < node1.frequency

class Node:
    def __init__(self, bits, num_bits, symbol):
        self.bits = bits
        self.num_bits = num_bits
        self.leafs = [0, 0]
        self.symbol = symbol


class Huffman:
    def setbits_r(self, node: Node, bits: int, depth: int) -> None:
        if node.leafs[1] != 0xFFFF:
            self.setbits_r(self.nodes[node.leafs[1]], bits|(1<<depth), depth+1)
        if node.leafs[0] != 0xFFFF:
            self.setbits_r(self.nodes[node.leafs[0]], bits, depth+1)

        if node.num_bits != 0:
            node.bits = bits
            node.num_bits = depth

    def construct_tree(self, frequencies: list[int]) -> None:
        nodes_left: list[HuffmanConstructNode] = [HuffmanConstructNode(0, 0) for _ in range(0, HUFFMAN_MAX_SYMBOLS)]

        num_nodes_left = HUFFMAN_MAX_SYMBOLS

        for i in range(0, HUFFMAN_MAX_SYMBOLS):
            self.nodes[i].num_bits = 0xFFFFFFFF
            self.nodes[i].symbol = i
            self.nodes[i].leafs[0] = 0xFFFF
            self.nodes[i].leafs[1] = 0xFFFF

            if(i == HUFFMAN_EOF_SYMBOL):
                nodes_left[i].frequency = 1
            else:
                nodes_left[i].frequency = frequencies[i]

            nodes_left[i].node_id = i

        self.num_nodes = HUFFMAN_MAX_SYMBOLS

        while num_nodes_left > 1:
            nodes_left = sorted(nodes_left, key=functools.cmp_to_key(compare_nodes_by_frequency_desc))

            self.nodes[self.num_nodes].num_bits = 0
            self.nodes[self.num_nodes].leafs[0] = nodes_left[num_nodes_left-1].node_id
            self.nodes[self.num_nodes].leafs[1] = nodes_left[num_nodes_left-2].node_id
            nodes_left[num_nodes_left-2].node_id = self.num_nodes
            nodes_left[num_nodes_left-2].frequency = \
                nodes_left[num_nodes_left-1].frequency + \
                nodes_left[num_nodes_left-2].frequency

            self.num_nodes += 1
            num_nodes_left -= 1

        self.start_node = self.nodes[self.num_nodes-1]

        self.setbits_r(self.start_node, 0, 0)

    def __init__(self, frequencies: list[int]) -> None:
        self.nodes: list[Node] = [Node(0, 0, 0) for _ in range(0, HUFFMAN_MAX_NODES)]
        self.decoded_lut: list[Node] = [Node(0, 0, 0) for _ in range(0, HUFFMAN_LUTSIZE)]
        self.num_nodes = 0
        self.start_node = Node(0, 0, 0)

        self.construct_tree(frequencies)

        for i in range(0, HUFFMAN_LUTSIZE):
            bits = i
            k = -1
            node = self.start_node
            while k < HUFFMAN_LUTBITS:
                k += 1
                node = self.nodes[node.leafs[bits&1]]
                bits >>= 1

                if node.num_bits != 0:
                    self.decoded_lut[i] = node
                    break

            if k == HUFFMAN_LUTBITS:
                self.decoded_lut[i] = node

    def decompress(self, data: bytes) -> bytes:
        src_index = 0
        size = len(data)
        dst = bytearray()
        bits = 0
        bitcount = 0
        eof = self.nodes[HUFFMAN_EOF_SYMBOL]
        node: Optional[Node] = None

        while True:
            node = None
            if bitcount >= HUFFMAN_LUTBITS:
                node = self.decoded_lut[bits&HUFFMAN_LUTMASK]

            while bitcount < 24 and src_index < size:
                bits |= data[src_index] << bitcount
                bitcount += 8
                src_index += 1

            if not node:
                node = self.decoded_lut[bits&HUFFMAN_LUTMASK]

            if node.num_bits != 0:
                bits >>= node.num_bits
                bitcount -= node.num_bits
            else:
                bits >>= HUFFMAN_LUTBITS
                bitcount -= HUFFMAN_LUTBITS

                while True:
                    node = self.nodes[node.leafs[bits&1]]

                    bitcount -= 1
                    bits >>= 1

                    if node.num_bits != 0:
                        break

                    # no more bits, decoding error
                    if bitcount == 0:
                        print("no more bits")
                        return dst
            # check for eof
            if node == eof:
                break
            dst.append(node.symbol)
        return bytes(dst)


huffman = Huffman(FREQUENCY_TABLE)
a = huffman.decompress(bytes([174, 149, 19, 92, 9, 87, 194, 22, 177, 86, 220, 218, 34, 56, 185, 18, 156, 168, 184, 1]))

print(a)
