"""Original K04 CLASS/DEST strict two-sampler discriminator on an indexed spool.

Read-only. Disputed row129, K04 mask, commitments and REC8 verifier withheld.
Usage: python agents/agent11/k04_strict_sampler_source_sft.py ORIGINAL_ZIP INDEX_VECTOR_JSON
"""
import json
import random
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "agents" / "agent33"))
from k04_global_target_projection import (
    source_rows, state_expressions, tempered_expressions, untemper,
)

CLASS = {"LABEL": 0, "STORES": 1, "RECOVER": 2}
DEST = {"store": 0, "desk": 1, "bench": 2}


def known_high_bits(rows, starts):
    """Use intact 132-row MT equations only to infer gap-output high bits."""
    terms = state_expressions(starts[-1] + 3)
    basis = {}
    for r, words in enumerate(rows):
        for j, observed in enumerate(words):
            for bit, expr in enumerate(terms[starts[r] + j]):
                value = (expr << 1) | ((observed >> bit) & 1)
                while value and value.bit_length() - 1 in basis:
                    value ^= basis[value.bit_length() - 1]
                if value == 1:
                    raise ValueError(("Original source MT conflict", r, j, bit))
                if value:
                    basis[value.bit_length() - 1] = value

    known = {}
    for r in range(127):
        for index in range(starts[r] + 4, starts[r + 1]):
            bits = {}
            tempered = tempered_expressions(terms[index])
            for bit in (29, 30, 31):
                value = tempered[bit] << 1
                while value and value.bit_length() - 1 in basis:
                    value ^= basis[value.bit_length() - 1]
                if value in (0, 1):
                    bits[bit] = value
            known[index] = bits
    return known, len(basis)


def permits(bits, width, allowed):
    return any(all(((code >> (bit - (32 - width))) & 1) == value
                   for bit, value in bits.items() if bit >= 32 - width)
               for code in allowed)


def contradiction_rows(rows, starts, classes, dests):
    known, rank = known_high_bits(rows, starts)
    failed = []
    for r in range(127):
        left, right = starts[r] + 4, starts[r + 1]
        possible = False
        for split in range(left + 1, right):
            if (all(permits(known[i], 2, {dests[r]} if i == split - 1 else {3})
                    for i in range(left, split))
                and all(permits(known[i], 3, {classes[r + 1]} if i == right - 1
                                else {3, 4, 5, 6, 7})
                        for i in range(split, right))):
                possible = True
                break
        if not possible:
            failed.append(r)
    return failed, rank


def original_labels(original_zip):
    with zipfile.ZipFile(original_zip) as archive:
        raw = archive.read("evidence/print/spool-reconstruction.log").decode()
    lines = [line for line in raw.splitlines() if line.startswith("2026-")]
    assert len(lines) == 133
    classes = [CLASS[re.search(r"CLASS=(\w+)", line).group(1)] for line in lines]
    dests = [DEST[re.search(r"DEST=(\w+)", line).group(1)] for line in lines]
    return classes, dests


def synthetic_control():
    rng = random.Random(5426)
    starts, classes, destinations, rows = [], [], [], []
    index = 0
    for r in range(133):
        if r < 128:
            while True:
                klass = rng.getrandbits(3)
                index += 1
                if klass <= 2:
                    break
        else:
            klass = 2
        classes.append(klass)
        starts.append(index)
        rows.append([untemper(rng.getrandbits(32)) for _ in range(4)])
        index += 4
        if r < 128:
            while True:
                dest = rng.getrandbits(2)
                index += 1
                if dest <= 2:
                    break
        else:
            dest = 0
        destinations.append(dest)
    rows[129] = []
    failed, rank = contradiction_rows(rows, starts, classes, destinations)
    assert failed == [], failed
    print("Synthetic true-two-sampler control PASS; source rank", rank)


def main(original_zip, index_json):
    synthetic_control()
    starts = json.loads(Path(index_json).read_text(encoding="utf8"))["row_starts"]
    rows = source_rows(Path(original_zip))
    classes, destinations = original_labels(original_zip)
    failed, rank = contradiction_rows(rows, starts, classes, destinations)
    assert rank == 15305, rank
    assert len(failed) == 30, failed
    print("Original intact-source rank", rank)
    print("Index955 strict-sampler impossible transitions", len(failed))
    print("Original zero-based transition numbers", failed)
    print("Model-conditional falsifier; original K04 coupon and K08 remain unknown.")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
