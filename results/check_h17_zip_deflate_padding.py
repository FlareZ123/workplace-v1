"""Audit the exact RFC 1951 final-block padding of a preservation ZIP.

Pure Python 3 standard library. Read-only with respect to the ZIP.
This counts ordinary ZIP/DEFLATE transport padding, not archive-key bytes.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import struct
import zipfile
import zlib


class BitReader:
    def __init__(self, data: bytes):
        self.data = data
        self.pos = 0

    def bits(self, n: int) -> int:
        if self.pos + n > 8 * len(self.data):
            raise ValueError("Truncated DEFLATE bitstream")
        value = 0
        for shift in range(n):
            value |= ((self.data[self.pos >> 3] >> (self.pos & 7)) & 1) << shift
            self.pos += 1
        return value

    def one(self) -> int:
        return self.bits(1)

    def align(self) -> None:
        self.pos = (self.pos + 7) & ~7


class Huffman:
    def __init__(self, lengths: list[int]):
        counts = Counter(n for n in lengths if n)
        if any(n < 0 or n > 15 for n in lengths):
            raise ValueError("Invalid Huffman code length")
        self.max_bits = max(counts, default=0)
        if not self.max_bits:
            raise ValueError("Empty Huffman tree")
        code = 0
        next_code = {}
        for length in range(1, self.max_bits + 1):
            code = (code + counts[length - 1]) << 1
            if code + counts[length] > (1 << length):
                raise ValueError("Oversubscribed Huffman tree")
            next_code[length] = code
        self.symbols = {}
        for symbol, length in enumerate(lengths):
            if length:
                self.symbols[(length, next_code[length])] = symbol
                next_code[length] += 1

    def read(self, reader: BitReader) -> int:
        code = 0
        for length in range(1, self.max_bits + 1):
            code = (code << 1) | reader.one()
            value = self.symbols.get((length, code))
            if value is not None:
                return value
        raise ValueError("Invalid Huffman code")


LENGTH_BASE = [
    3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 15, 17, 19, 23, 27,
    31, 35, 43, 51, 59, 67, 83, 99, 115, 131, 163, 195, 227, 258,
]
LENGTH_EXTRA = [
    0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2,
    3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 0,
]
DISTANCE_BASE = [
    1, 2, 3, 4, 5, 7, 9, 13, 17, 25, 33, 49, 65, 97, 129,
    193, 257, 385, 513, 769, 1025, 1537, 2049, 3073, 4097,
    6145, 8193, 12289, 16385, 24577,
]
DISTANCE_EXTRA = [0, 0, 0, 0] + [n for n in range(1, 14) for _ in range(2)]
CODE_ORDER = [16, 17, 18, 0, 8, 7, 9, 6, 10, 5, 11, 4, 12, 3, 13, 2, 14, 1, 15]


def dynamic_trees(reader: BitReader) -> tuple[Huffman, Huffman | None]:
    hlit = reader.bits(5) + 257
    hdist = reader.bits(5) + 1
    hclen = reader.bits(4) + 4
    clen = [0] * 19
    for i in range(hclen):
        clen[CODE_ORDER[i]] = reader.bits(3)
    tree = Huffman(clen)
    lengths = []
    while len(lengths) < hlit + hdist:
        symbol = tree.read(reader)
        if symbol <= 15:
            lengths.append(symbol)
        elif symbol == 16:
            if not lengths:
                raise ValueError("Repeat-before-first code length")
            lengths.extend([lengths[-1]] * (reader.bits(2) + 3))
        elif symbol == 17:
            lengths.extend([0] * (reader.bits(3) + 3))
        elif symbol == 18:
            lengths.extend([0] * (reader.bits(7) + 11))
        else:
            raise ValueError("Unexpected code-length symbol")
    if len(lengths) != hlit + hdist:
        raise ValueError("Code-length repeat overshot table")
    return Huffman(lengths[:hlit]), (
        Huffman(lengths[hlit:]) if any(lengths[hlit:]) else None
    )


def inspect_deflate(compressed: bytes) -> dict:
    reader = BitReader(compressed)
    output_length = 0
    block_types = []
    while True:
        final = reader.one()
        block_type = reader.bits(2)
        if block_type == 0:
            block_types.append("stored")
            reader.align()
            length = reader.bits(16)
            complement = reader.bits(16)
            if complement != (length ^ 65535):
                raise ValueError("Incorrect stored-block length complement")
            end = reader.pos + length * 8
            if end > len(compressed) * 8:
                raise ValueError("Truncated stored block")
            reader.pos = end
            output_length += length
        elif block_type in (1, 2):
            block_types.append("fixed" if block_type == 1 else "dynamic")
            if block_type == 1:
                literal_tree = Huffman(
                    [8] * 144 + [9] * 112 + [7] * 24 + [8] * 8
                )
                distance_tree = Huffman([5] * 32)
            else:
                literal_tree, distance_tree = dynamic_trees(reader)
            while True:
                symbol = literal_tree.read(reader)
                if symbol < 256:
                    output_length += 1
                elif symbol == 256:
                    break
                elif 257 <= symbol <= 285:
                    index = symbol - 257
                    size = LENGTH_BASE[index] + reader.bits(LENGTH_EXTRA[index])
                    if distance_tree is None:
                        raise ValueError("Backreference without distance tree")
                    dist_code = distance_tree.read(reader)
                    if dist_code >= len(DISTANCE_BASE):
                        raise ValueError("Reserved distance code")
                    distance = (
                        DISTANCE_BASE[dist_code]
                        + reader.bits(DISTANCE_EXTRA[dist_code])
                    )
                    if distance > min(32768, output_length):
                        raise ValueError("Invalid backward distance")
                    output_length += size
                else:
                    raise ValueError("Reserved literal/length code")
        else:
            raise ValueError("Reserved DEFLATE block type")
        if final:
            break
    if (reader.pos + 7) // 8 != len(compressed):
        raise ValueError("Bytes remain after final DEFLATE block")
    slack = (-reader.pos) % 8
    padding_value = compressed[-1] >> (8 - slack) if slack else 0
    return {
        "blocks": block_types,
        "uncompressed_size": output_length,
        "unused_final_bits": slack,
        "padding_value": padding_value,
    }


def audit_zip(path: Path) -> dict:
    source = path.read_bytes()
    if hashlib.sha256(source).hexdigest() != (
        "a801d9b32715305b4a889e3c091a88455090a5c4bd56b6cf7f6c07ba8e4527ec"
    ):
        raise ValueError("Source ZIP SHA-256 does not match preservation export")
    padding = Counter()
    block_types = Counter()
    total_blocks = 0
    nonzero = []
    first_stream = None
    with zipfile.ZipFile(path) as archive:
        for info in archive.infolist():
            offset = info.header_offset
            header = struct.unpack_from("<IHHHHHIIIHH", source, offset)
            if header[0] != 0x04034B50 or info.compress_type != zipfile.ZIP_DEFLATED:
                raise ValueError("Unexpected local ZIP header or compression")
            start = offset + 30 + header[-2] + header[-1]
            compressed = source[start:start + info.compress_size]
            result = inspect_deflate(compressed)
            if zlib.decompress(compressed, -15) != archive.read(info):
                raise ValueError(f"Decoded bytes mismatch: {info.filename}")
            if result["uncompressed_size"] != info.file_size:
                raise ValueError(f"Decoded length mismatch: {info.filename}")
            total_blocks += len(result["blocks"])
            block_types.update(result["blocks"])
            padding[result["unused_final_bits"]] += 1
            if result["padding_value"]:
                nonzero.append(info.filename)
            if first_stream is None:
                first_stream = compressed

        if first_stream is None:
            raise ValueError("Empty ZIP")
        original = inspect_deflate(first_stream)
        if original["unused_final_bits"] == 0:
            raise ValueError("First member has no slack for positive control")
        flipped = first_stream[:-1] + bytes([first_stream[-1] ^ 0x80])
        changed = inspect_deflate(flipped)
        if zlib.decompress(flipped, -15) != zlib.decompress(first_stream, -15):
            raise ValueError("Padding control modified decompressed data")
        if not changed["padding_value"]:
            raise ValueError("Padding mutation control was not detected")

        return {
            "source_sha256": hashlib.sha256(source).hexdigest(),
            "members": len(archive.infolist()),
            "blocks": total_blocks,
            "block_types": dict(sorted(block_types.items())),
            "unused_final_bit_distribution": {
                str(k): v for k, v in sorted(padding.items())
            },
            "total_unused_final_bits": sum(k * v for k, v in padding.items()),
            "nonzero_padding_members": nonzero,
            "mutation_control": {
                "original_padding_value": original["padding_value"],
                "mutated_padding_value": changed["padding_value"],
                "decompressed_bytes_unchanged": True,
            },
        }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("zip_path", type=Path)
    args = parser.parse_args()
    print(json.dumps(audit_zip(args.zip_path), indent=2))


if __name__ == "__main__":
    main()
