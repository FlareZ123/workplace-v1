"""Deterministic standalone tests for the H-17 RFC1951 ZIP padding reader.

Run from the same directory as check_h17_zip_deflate_padding.py.
Optionally pass the original preservation ZIP to validate its pinned audit.
"""
from __future__ import annotations

import argparse
from collections import Counter
import random
import zlib
from pathlib import Path

import check_h17_zip_deflate_padding as reader


SIZES = (0, 1, 2, 7, 15, 31, 32, 127, 128, 255, 256, 1024, 2048, 4096)
LEVELS = (0, 1, 6, 9)
STRATEGIES = {
    "default": zlib.Z_DEFAULT_STRATEGY,
    "filtered": zlib.Z_FILTERED,
    "huffman": zlib.Z_HUFFMAN_ONLY,
    "rle": zlib.Z_RLE,
    "fixed": zlib.Z_FIXED,
}


def make_data(size: int, shape: str, seed: int) -> bytes:
    if shape == "zero":
        return bytes(size)
    if shape == "range":
        return bytes(i % 256 for i in range(size))
    if shape == "repeat":
        return (b"S0\x00\xffREC8" * ((size + 7) // 8))[:size]
    return random.Random(seed).randbytes(size)


def compress_raw(data: bytes, level: int, strategy: int, mode: str) -> bytes:
    compressor = zlib.compressobj(level=level, wbits=-15, strategy=strategy)
    if mode == "single":
        return compressor.compress(data) + compressor.flush()
    if mode == "parts":
        a = len(data) // 3
        return (
            compressor.compress(data[:a])
            + compressor.compress(data[a : 2 * a])
            + compressor.compress(data[2 * a :])
            + compressor.flush()
        )
    third = len(data) // 3
    return (
        compressor.compress(data[:third]) + compressor.flush(zlib.Z_SYNC_FLUSH)
        + compressor.compress(data[third : 2 * third]) + compressor.flush(zlib.Z_SYNC_FLUSH)
        + compressor.compress(data[2 * third :]) + compressor.flush()
    )


def run_synthetic() -> None:
    count = 0
    block_types = Counter()
    positive_padding = 0
    for level in LEVELS:
        for strategy_name, strategy in STRATEGIES.items():
            per_variant = 0
            for size in SIZES:
                for shape in ("zero", "range", "repeat", "random"):
                    data = make_data(size, shape, 0xCE617 + size * 31 + level)
                    for mode in ("single", "parts", "flush"):
                        encoded = compress_raw(data, level, strategy, mode)
                        parsed = reader.inspect_deflate(encoded)
                        assert zlib.decompress(encoded, -15) == data
                        assert parsed["uncompressed_size"] == len(data), (
                            level, strategy_name, size, shape, mode, parsed
                        )
                        assert parsed["padding_value"] == 0, (
                            level, strategy_name, size, shape, mode, parsed
                        )
                        block_types.update(parsed["blocks"])
                        if parsed["unused_final_bits"]:
                            altered = encoded[:-1] + bytes([encoded[-1] ^ 0x80])
                            changed = reader.inspect_deflate(altered)
                            assert changed["padding_value"] != 0
                            assert zlib.decompress(altered, -15) == data
                            assert changed["uncompressed_size"] == len(data)
                            positive_padding += 1
                        count += 1
                        per_variant += 1
            print(f"PASS: level={level} strategy={strategy_name} ",
                  f"synthetic_streams={per_variant}")
    assert count == len(LEVELS) * len(STRATEGIES) * len(SIZES) * 4 * 3
    assert block_types["stored"] and block_types["fixed"] and block_types["dynamic"]
    assert positive_padding > 0
    print(f"PASS: synthetic total={count}, block_types={dict(block_types)}, ",
          f"in-memory_padding_mutations={positive_padding}")


def run_invalid() -> None:
    cases = {
        "empty_stream": b"",
        "reserved_block_type": bytes([7]),
        "truncated_stored_header": bytes([1]),
        "truncated_stored_body": bytes([1, 1, 0, 254, 255]),
        "extra_trailing_byte": bytes([3, 0, 0]),
    }
    for name, value in cases.items():
        try:
            reader.inspect_deflate(value)
        except ValueError:
            print(f"PASS: malformed stream rejected: {name}")
        else:
            raise AssertionError(f"Malformed stream accepted: {name}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("zip_path", nargs="?", help="Optional original source ZIP")
    args = parser.parse_args()
    run_synthetic()
    run_invalid()
    if args.zip_path:
        audit = reader.audit_zip(Path(args.zip_path))
        assert audit["members"] == 43
        assert audit["blocks"] == 43
        assert audit["block_types"] == {"dynamic": 42, "fixed": 1}
        assert audit["total_unused_final_bits"] == 151
        assert not audit["nonzero_padding_members"]
        assert audit["mutation_control"]["mutated_padding_value"] == 4
        print("PASS: original pinned H-17 ZIP, 43 blocks, 151 zero slack bits")
    print("ALL DEFLATE PARSER TESTS PASSED")


if __name__ == "__main__":
    main()
