"""K04 MT19937 post-twist reachability test (original evidence only).

SFT: run(source, fixture), where source is original case ZIP or extracted
directory, fixture is the published original-source-compatible p955 row index.
Selected spool row129 and all route, nonce, SHA commitments stay unread.
"""
from __future__ import annotations

import hashlib
import json
import random
import re
import struct
import zipfile
from pathlib import Path

A = 0x9908B0DF
SPOOL = "evidence/print/spool-reconstruction.log"
SPOOL_SHA = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"


def untemper(y: int) -> int:
    for shift, direction, mask in (
        (18, "right", 0xFFFFFFFF),
        (15, "left", 0xEFC60000),
        (7, "left", 0x9D2C5680),
        (11, "right", 0xFFFFFFFF),
    ):
        original = y
        for _ in range(6):
            y = (original ^ (y >> shift if direction == "right" else
                             (y << shift) & mask)) & 0xFFFFFFFF
    return y


def symbolic(max_index: int, shift: int) -> list[list[int]]:
    words = [[1 << (32 * t + bit) for bit in range(32)]
             for t in range(624)]
    for t in range(624, max_index + shift + 1):
        predecessor = words[t - 624]
        next_word = words[t - 623]
        middle = words[t - 227]
        words.append([
            middle[bit]
            ^ (predecessor[31] if bit == 30 else
               next_word[bit + 1] if bit < 30 else 0)
            ^ (next_word[0] if (A >> bit) & 1 else 0)
            for bit in range(32)
        ])
    return words


def reduce_row(row: int, basis: dict[int, int]) -> int:
    while row:
        pivot = row.bit_length() - 1
        if pivot not in basis:
            return row
        row ^= basis[pivot]
    return 0


def rank(vectors: list[int]) -> int:
    basis: dict[int, int] = {}
    for row in vectors:
        row = reduce_row(row, basis)
        if row:
            basis[row.bit_length() - 1] = row
    return len(basis)


def source_rows(source: Path) -> list[list[int]]:
    if source.is_dir():
        raw = (source / SPOOL).read_bytes()
    else:
        with zipfile.ZipFile(source) as archive:
            raw = archive.read(SPOOL)
    assert hashlib.sha256(raw).hexdigest() == SPOOL_SHA
    rows: list[list[int]] = []
    for line in raw.splitlines():
        hit = re.search(rb"PAYLOAD=([0-9A-F]{32})", line)
        if hit is not None:
            packed = bytes.fromhex(hit.group(1).decode("ascii"))
            rows.append([untemper(word) for word in struct.unpack("<4I", packed)])
    assert len(rows) == 133
    rows[129] = []
    return rows


def projection(source: Path, starts: list[int], shift: int) -> tuple[int, int, int]:
    records = source_rows(source)
    words = symbolic(max(starts) + 3, shift)
    basis: dict[int, int] = {}
    for record_index, record in enumerate(records):
        for j, word in enumerate(record):
            expression = words[starts[record_index] + j + shift]
            for bit, term in enumerate(expression):
                row = reduce_row((term << 1) | ((word >> bit) & 1), basis)
                assert row != 1, ("Original-source contradiction", record_index, j, bit)
                if row:
                    basis[row.bit_length() - 1] = row

    quotient: dict[int, int] = {}
    fixed = 0
    for j in range(4):
        for term in words[starts[129] + j + shift]:
            residual = reduce_row(term << 1, basis)
            if residual in (0, 1):
                fixed += 1
            else:
                residual = reduce_row(residual >> 1, quotient)
                if residual:
                    quotient[residual.bit_length() - 1] = residual
    print(f"shift={shift}: original rank={len(basis)}, selected quotient="
          f"{len(quotient)}/128, individually fixed untempered bits={fixed}")
    return len(basis), len(quotient), fixed


def seeded_positive_controls() -> None:
    terms = symbolic(955, 624)
    for seed in (0, 1, 20261020):
        rng = random.Random(seed)
        register = rng.getstate()[1][:624]
        initial = sum(word << (32 * i) for i, word in enumerate(register))
        expected = [untemper(rng.getrandbits(32)) for _ in range(956)]
        for index in (0, 1, 2, 3, 5, 227, 397, 623, 624, 955):
            got = sum(((expression & initial).bit_count() & 1) << bit
                      for bit, expression in enumerate(terms[index + 624]))
            assert got == expected[index], (seed, index, got, expected[index])
        print(f"real CPython MT seed={seed}: ten exact state predictions PASS")

    first = symbolic(1247, 0)
    first_rank = rank([v for word in first[:624] for v in word])
    image_rank = rank([v for word in first[624:1248] for v in word])
    print(f"unrestricted rank={first_rank}, post-twist reachability rank={image_rank}")
    assert (first_rank, image_rank) == (19968, 19937)


def run(source: Path, fixture: Path) -> None:
    starts = json.loads(fixture.read_text("utf-8"))["row_starts"]
    assert len(starts) == 133 and starts[0] == 0 and starts[129] == 955
    assert all(starts[i + 1] >= starts[i] + 4 for i in range(132))
    seeded_positive_controls()
    unrestricted = projection(source, starts, shift=0)
    reachable = projection(source, starts, shift=624)
    assert unrestricted == (15305, 128, 0)
    assert reachable == (15305, 128, 0)
    print("Conclusion: all 128 selected untempered coupon bits remain independent "
          "even after true post-twist MT reachability is imposed.")


if __name__ == "__main__":
    run(Path("resources"), Path("results/h17-k04-source-consistent-index955.json"))
