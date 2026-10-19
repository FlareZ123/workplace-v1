"""Reconstruct unknown MT19937 state words via exact inverse twists.

Usage: python agents/agent23/k04_mt_inverse_peel.py original-case.zip
Read-only, source-pinned, row129 withheld, no acceptance/route lookup.
"""
import hashlib
import re
import struct
import sys
from collections import defaultdict
from pathlib import Path
from zipfile import ZipFile

from k04_mt_rowstart import discover, untemper, SHA, SPOOL

A = 0x9908B0DF
ALL = 0xFFFFFFFF


def inverse_twist(value):
    bit = value >> 31
    mixed = (((value ^ (A if bit else 0)) << 1) | bit) & ALL
    assert (mixed >> 1) ^ (A if mixed & 1 else 0) == value
    return mixed


def rows(source):
    with ZipFile(source) as archive:
        raw = archive.read(SPOOL)
    assert hashlib.sha256(raw).hexdigest() == SHA
    payloads = [bytes.fromhex(s) for s in re.findall(rb"PAYLOAD=([A-F0-9]{32})", raw)]
    assert len(payloads) == 133
    values = [list(map(untemper, struct.unpack("<4I", p))) for p in payloads]
    values[129] = []
    return values


def groups(source, values):
    # The row-start reproducer independently checks 25 within-row and 17
    # first-word predecessors against the SHA-pinned original ZIP.
    within, boundary = discover(source)
    assert len(within) == 25 and len(boundary) == 17
    parent = list(range(133))
    offset = [0] * 133

    def find(x):
        if parent[x] != x:
            p = parent[x]
            root = find(p)
            offset[x] += offset[p]
            parent[x] = root
        return parent[x]

    def equal(a, b, d):
        ra, rb = find(a), find(b)
        va, vb = offset[a], offset[b]
        if ra == rb:
            assert vb - va == d
        else:
            parent[rb] = ra
            offset[rb] = d + va - vb

    for (a, j), (b, k), (c, l) in within:
        equal(a, b, 397 + j - k)
        equal(a, c, 624 + j - l)
    for a, bit, (b, k), (c, l) in boundary:
        equal(a, b, 396 - k)
        equal(a, c, 623 - l)

    result = defaultdict(list)
    for row in range(133):
        result[find(row)].append((row, offset[row]))
    return result


def recover(group, values):
    observed = {}
    for row, start in group:
        for j, word in enumerate(values[row]):
            position = start + j
            assert position not in observed or observed[position] == word
            observed[position] = word
    state = {p: (ALL, v) for p, v in observed.items()}
    evidence = defaultdict(list)

    def apply(p, mask, bits, witness):
        oldmask, oldvalue = state.get(p, (0, 0))
        assert ((oldvalue ^ bits) & (oldmask & mask)) == 0
        state[p] = (oldmask | mask, oldvalue | bits)
        evidence[p].append(witness)

    for end in sorted(observed):
        mid = end - 227
        if mid not in observed:
            continue
        k = end - 624
        mixed = inverse_twist(observed[mid] ^ observed[end])
        apply(k, 0x80000000, mixed & 0x80000000, (mid, end))
        apply(k + 1, 0x7FFFFFFF, mixed & 0x7FFFFFFF, (mid, end))
    full = {p: v for p, (mask, v) in state.items()
            if p not in observed and mask == ALL}
    partial = {p: (mask, v) for p, (mask, v) in state.items()
               if p not in observed and mask != ALL}
    return full, partial, evidence


def main(source):
    values = rows(source)
    clusters = groups(source, values)
    total_full = total_partial = 0
    for root, entries in sorted(clusters.items()):
        full, partial, evidence = recover(entries, values)
        total_full += len(full)
        total_partial += len(partial)
        if full:
            print("group", root, "rows", len(entries),
                  "new_full_words", len(full))
            for pos, val in sorted(full.items()):
                print("  relative_index", pos,
                      "untempered", f"{val:08X}", "source_pairs", evidence[pos])
        if any(row == 44 for row, _ in entries):
            assert full[-2] == 0x27D820C7
            assert full[-1] == 0x0ACF4761
    assert (total_full, total_partial) == (30, 34)
    print("total_new_full_words", total_full)
    print("total_new_partial_words", total_partial)
    # A separate consistency identity reconstructs source row44 word0
    # entirely from intact row97 word2/3 and row130/131 tail word3/0.
    predecessor = inverse_twist(values[130][3] ^ values[97][2])
    successor = inverse_twist(values[131][0] ^ values[97][3])
    predicted = (successor & 0x80000000) | (predecessor & 0x7FFFFFFF)
    assert predicted == values[44][0]
    print("independently_reconstructed_row44_first_word", f"{predicted:08X}")
    print("original_known_word_match", True)
    print("K04_K08_UNRESOLVED")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python k04_mt_inverse_peel.py original-case.zip")
    main(Path(sys.argv[1]))
