"""Find MT19937 twist-recurrence witnesses in original H-17 printer payloads.

Read-only structural test. Does not use original acceptance commitments or
predict a missing coupon. Run with an extracted resources/ folder, or an
original ZIP path as positional argument.
"""
import argparse
import hashlib
import random
import re
import struct
import zipfile
from collections import defaultdict
from pathlib import Path

SOURCE_SHA256 = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
PATH = "evidence/print/spool-reconstruction.log"


def source_rows(source):
    if source.is_file():
        with zipfile.ZipFile(source) as archive:
            raw = archive.read(PATH)
    else:
        raw = (source / PATH).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == SOURCE_SHA256
    rows = []
    for line in raw.decode("utf-8").splitlines():
        if not line.startswith("2026-"):
            continue
        m = re.search(r"PAYLOAD=([0-9A-F]{32})", line)
        assert m is not None
        rows.append(bytes.fromhex(m.group(1)))
    assert len(rows) == 133
    return rows


def undo_right(y, shift):
    x = y
    for _ in range(6):
        x = y ^ (x >> shift)
    return x & 0xFFFFFFFF


def undo_left(y, shift, mask):
    x = y
    for _ in range(6):
        x = y ^ ((x << shift) & mask)
    return x & 0xFFFFFFFF


def untemper(y):
    y = undo_right(y, 18)
    y = undo_left(y, 15, 0xEFC60000)
    y = undo_left(y, 7, 0x9D2C5680)
    return undo_right(y, 11)


def twist(a, b):
    y = (a & 0x80000000) | (b & 0x7FFFFFFF)
    return ((y >> 1) ^ (0x9908B0DF if y & 1 else 0)) & 0xFFFFFFFF


def detect(rows, endian="<", reversed_words=False):
    """Find exact x[k+624] == x[k+397] ^ twist(x[k],x[k+1]).

    Each source payload contributes four consecutive 32-bit outputs; do
    not require metadata calls between payloads to be fixed in number.
    Restrict triple rows to increasing source order, with x[k], x[k+1]
    adjacent inside the same payload.
    """
    words, pairs = [], []
    for row, payload in enumerate(rows):
        ws = struct.unpack(f"{endian}4I", payload)
        if reversed_words:
            ws = ws[::-1]
        ws = [untemper(w) for w in ws]
        words.extend((row, j, w) for j, w in enumerate(ws))
        pairs.extend((row, j, twist(ws[j], ws[j + 1])) for j in range(3))

    by_value = defaultdict(list)
    for row, j, w in words:
        by_value[w].append((row, j))

    witnesses = []
    for first_row, first_j, step in pairs:
        for mid_row, mid_j, middle in words:
            if mid_row <= first_row:
                continue
            for final_row, final_j in by_value.get(middle ^ step, ()):
                if final_row > mid_row:
                    witnesses.append(
                        ((first_row, first_j),
                         (mid_row, mid_j),
                         (final_row, final_j))
                    )
    return witnesses


def synthetic_positive():
    rng = random.Random(0x1234567)
    rows = []
    for _ in range(128):
        rng.choice(("RECOVER", "LABEL", "STORES"))
        rng.choice(("desk", "bench", "store"))
        rows.append(rng.randbytes(16))
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", nargs="?", type=Path, default=Path("resources"))
    args = parser.parse_args()
    original = source_rows(args.source)
    synthetic = synthetic_positive()
    synthetic_hits = detect(synthetic, "<")
    assert len(synthetic_hits) >= 10, "synthetic interleaved-MT positive control failed"
    print("synthetic_positive_total", len(synthetic_hits))

    for name, rows in (("original_regular", original[:128]), ("original_all", original)):
        for endian in ("<", ">"):
            hits = detect(rows, endian)
            by_tail = [h for h in hits if h[2][0] >= 128]
            print(name, "little" if endian == "<" else "big",
                  "total", len(hits), "tail", len(by_tail))
            if name == "original_all" and endian == "<":
                print("original_tail_witnesses_0_based_row_word", by_tail)
                assert len(hits) == 25
                assert len(by_tail) == 2
                assert by_tail == [
                    ((44, 0), (97, 3), (131, 0)),
                    ((45, 0), (98, 3), (132, 3)),
                ]
    print("K04_K08_REC8_status_unchanged")


if __name__ == "__main__":
    main()
