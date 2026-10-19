"""Source-only K04 printer CLASS predecessor test.

Run from repo root: python agents/agent7/k04_class_boundary_sft.py
Never loads selected row129 payload, mask, acceptance, nonce or verifier.
"""
import hashlib
import re
import struct
from collections import defaultdict
from pathlib import Path

SOURCE = Path("resources/evidence/print/spool-reconstruction.log")
EXPECTED = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
MATRIX_A = 0x9908B0DF


def untemper(y):
    for shift, direction, mask in (
        (18, "r", 0), (15, "l", 0xEFC60000),
        (7, "l", 0x9D2C5680), (11, "r", 0)
    ):
        output = y
        for _ in range(7):
            output = y ^ (
                output >> shift if direction == "r"
                else (output << shift) & mask
            )
        y = output
    return y & 0xFFFFFFFF


def temper(y):
    y ^= y >> 11
    y ^= (y << 7) & 0x9D2C5680
    y ^= (y << 15) & 0xEFC60000
    return (y ^ (y >> 18)) & 0xFFFFFFFF


def twist(a, b):
    t = ((a & 0x80000000) | (b & 0x7FFFFFFF)) >> 1
    return t ^ (MATRIX_A if b & 1 else 0)


def untwist_parts(v):
    odd = v >> 31
    x = v ^ (MATRIX_A if odd else 0)
    return ((x & 0x40000000) << 1, ((x & 0x3FFFFFFF) << 1) | odd)


def main():
    original = SOURCE.read_bytes()
    assert hashlib.sha256(original).hexdigest() == EXPECTED
    rows = []
    for line in original.decode().splitlines():
        match = re.search(r"CLASS=(\w+) PAYLOAD=([0-9A-F]{32}) DEST=(\w+)", line)
        if match:
            index = len(rows)
            # The disputed selected coupon is completely withheld.
            words = None if index == 129 else [
                untemper(w) for w in struct.unpack("<4I", bytes.fromhex(match[2]))
            ]
            rows.append((match[1], match[3], words))
    assert len(rows) == 133 and rows[129][2] is None

    # Independently find the 25 exact ordinary MT recurrence witnesses.
    observed = defaultdict(list)
    for i, (_, _, words) in enumerate(rows):
        if words is not None:
            for col, value in enumerate(words):
                observed[value].append((i, col))
    witnesses = []
    for i, (_, _, words) in enumerate(rows):
        if words is None:
            continue
        for a in range(3):
            t = twist(words[a], words[a + 1])
            for j in range(i + 20, min(i + 66, len(rows))):
                middle = rows[j][2]
                if middle is None:
                    continue
                for b, value in enumerate(middle):
                    for k, c in observed.get(value ^ t, []):
                        if j + 20 <= k <= j + 41:
                            witnesses.append((i, a, j, b, k, c))
    assert len(witnesses) == 25

    # Recover source-anchored relative MT positions, with consistency checks.
    graph = defaultdict(list)
    for i, a, j, b, k, c in witnesses:
        for left, right, delta in (
            (i, j, a + 397 - b), (i, k, a + 624 - c)
        ):
            graph[left].append((right, delta))
            graph[right].append((left, -delta))
    offsets, groups = {}, []
    for start in sorted(graph):
        if start in offsets:
            continue
        offsets[start] = 0
        group, stack = [], [start]
        while stack:
            node = stack.pop()
            group.append(node)
            for neighbor, delta in graph[node]:
                expected = offsets[node] + delta
                if neighbor not in offsets:
                    offsets[neighbor] = expected
                    stack.append(neighbor)
                else:
                    assert offsets[neighbor] == expected
        groups.append(group)
    assert len(groups) == 14

    # A known 227-apart middle/future pair determines parts of the
    # predecessor state. Two adjacent pairs determine its full 32 bits.
    predecessor = {}
    for group in groups:
        for middle in group:
            for future in group:
                if future <= middle:
                    continue
                parts = {}
                for a in range(4):
                    for b in range(4):
                        if offsets[future] + b - offsets[middle] - a == 227:
                            t = offsets[middle] + a - 397
                            diff = rows[future][2][b] ^ rows[middle][2][a]
                            parts[t] = untwist_parts(diff)
                for t, (_, low31) in parts.items():
                    if t + 1 not in parts:
                        continue
                    full = low31 | parts[t + 1][0]
                    for row in group:
                        if offsets[row] - 1 == t + 1:
                            if row in predecessor:
                                assert predecessor[row] == full
                            predecessor[row] = full

    expected = {
        3: ("RECOVER", 0x482F6361, 2),
        13: ("STORES", 0x8F878FB0, 1),
        38: ("RECOVER", 0x820D840E, 2),
        45: ("STORES", 0xB37E7885, 1),
    }
    assert set(predecessor) == set(expected)
    for row, (label, state, code) in sorted(expected.items()):
        assert (rows[row][0], predecessor[row], temper(predecessor[row]) >> 29) == (
            label, state, code
        )
        print(f"row{row} CLASS={label} X[s-1]={state:08X} upper3={code}")

    # Fifth held-out label, conditional on independent published group-44
    # placement s97=s44+394, s130=s44+620 (42-witness closure).
    pairs = [
        untwist_parts(rows[97][2][j] ^ rows[130][2][j + 1])
        for j in range(3)
    ]
    row44 = pairs[1][1] | pairs[2][0]
    assert row44 == 0x0ACF4761
    assert temper(row44) >> 29 == 1 and rows[44][0] == "STORES"
    print(f"row44 conditional CLASS=STORES X[s-1]={row44:08X} upper3=1")

    # If the identical predecessor-to-CLASS coding extends to the special
    # recovery tail, p=627 implies X[p-1] is intact row128's final word.
    prior_code = temper(rows[128][2][3]) >> 29
    assert prior_code == 5 and rows[129][0] == "RECOVER"
    print(f"tail p=627 conditional CLASS test: known upper3={prior_code}, "
          "expected RECOVER=2 -> mismatch")
    print("No target bits recovered; no change to K04/K08 acceptance.")


if __name__ == "__main__":
    main()
