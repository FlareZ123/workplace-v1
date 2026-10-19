"""H17 K04 tail-gap coupling, source-only standalone test.
Usage: python agents/agent22/k04_tail_gap_coupling.py original-case.zip
Selected spool row129, acceptance commitments, route mask and K08 withheld.
"""
import hashlib
import random
import re
import sys
from pathlib import Path
from zipfile import ZipFile

SHA = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
ALL = 0xFFFFFFFF


def temper(x):
    x ^= x >> 11
    x ^= (x << 7) & 0x9D2C5680
    x ^= (x << 15) & 0xEFC60000
    x ^= x >> 18
    return x & ALL


def untemper(x):
    for shift, mask, iterations in ((18, None, 2), (15, 0xEFC60000, 3),
                                    (7, 0x9D2C5680, 5), (11, None, 4)):
        y = x
        for _ in range(iterations):
            x = y ^ (((x << shift) & mask) if mask is not None else (x >> shift))
    return x & ALL


def twist(a, b):
    both = (a & 0x80000000) | (b & 0x7FFFFFFF)
    return (both >> 1) ^ (0x9908B0DF if both & 1 else 0)


def inv_twist(z):
    odd = z >> 31
    return ((((z ^ (0x9908B0DF if odd else 0)) << 1) & ALL) | odd)


def read_rows(path):
    with ZipFile(path) as archive:
        original = archive.read("evidence/print/spool-reconstruction.log")
    assert hashlib.sha256(original).hexdigest() == SHA
    lines = [s for s in original.decode().splitlines() if s.startswith("2026-")]
    assert len(lines) == 133
    rows = []
    for line in lines:
        fields = dict(re.findall(r"([A-Z]+)=([^ ]+)", line))
        payload = bytes.fromhex(fields["PAYLOAD"])
        words = [untemper(int.from_bytes(payload[j:j+4], "little"))
                 for j in (0, 4, 8, 12)]
        rows.append((fields, words))
    return rows


def boundary(rows, src, mid, end):
    a, b, c = (rows[r][1][j] for r, j in (src, mid, end))
    matches = [bit for bit in (0, 1) if b ^ twist(bit << 31, a) == c]
    assert len(matches) == 1
    return matches[0]


def close(known):
    state = {p: (ALL, value) for p, value in known.items()}

    def add(p, mask, bits):
        old, prior = state.get(p, (0, 0))
        assert not ((bits ^ prior) & old & mask), ("contradiction", p)
        if (old | mask) == old:
            return False
        state[p] = (old | mask, prior | bits)
        return True

    while True:
        changed = False
        for end, (mask, word) in tuple(state.items()):
            middle = state.get(end - 227, (0, 0))
            if mask == ALL and middle[0] == ALL:
                x = inv_twist(word ^ middle[1])
                changed |= add(end - 624, 0x80000000, x & 0x80000000)
                changed |= add(end - 623, 0x7FFFFFFF, x & 0x7FFFFFFF)
        for first, (mask, word) in tuple(state.items()):
            successor = state.get(first + 1, (0, 0))
            middle = state.get(first + 397, (0, 0))
            end = state.get(first + 624, (0, 0))
            if not mask & 0x80000000 or successor[0] & 0x7FFFFFFF != 0x7FFFFFFF:
                continue
            step = twist(word, successor[1])
            if middle[0] == ALL:
                changed |= add(first + 624, ALL, middle[1] ^ step)
            if end[0] == ALL:
                changed |= add(first + 397, ALL, end[1] ^ step)
        if not changed:
            return state


GROUP = {
    12: -229, 43: 0, 66: 167, 96: 393, 128: 623,
    13: -216, 44: 11, 67: 179, 97: 405, 130: 631, 131: 635,
    45: 18, 98: 412, 132: 639,
}


def synthetic():
    for seed in (0, 1, 0x123456789, 0xBAD5EED):
        rng = random.Random(seed)
        state = [untemper(rng.getrandbits(32)) for _ in range(1800)]
        for t in range(1100):
            assert state[t + 624] == state[t + 397] ^ twist(state[t], state[t + 1])
        observed = {p + j: state[500 + p + j]
                    for p in GROUP.values() for j in range(4)}
        recovered = close(observed)
        for t in (16, 17, 409, 410):
            assert recovered[t] == (ALL, state[500 + t])
    print("synthetic_MT_controls", "4/4 PASS")


def source(rows):
    # Row44's consecutive words, and two independently inverted first-word anchors.
    assert rows[97][1][3] ^ twist(rows[44][1][0], rows[44][1][1]) == rows[131][1][0]
    assert boundary(rows, (44, 0), (97, 2), (130, 3)) == 0
    assert boundary(rows, (45, 0), (98, 2), (132, 2)) == 1
    print("three_source_witnesses", "PASS")
    print("exact_conditional_identity", "g44=g97=g131+3")
    observed = {pos + j: rows[row][1][j]
                for row, pos in GROUP.items() for j in range(4)}
    state = close(observed)
    for pos, width, expected in ((16, 3, 7), (17, 3, 1),
                                 (409, 2, 0), (410, 3, 6)):
        mask, value = state.get(pos, (0, 0))
        assert mask == ALL and temper(value) >> (32-width) == expected
    assert rows[45][0]["CLASS"] == "STORES"
    assert rows[97][0]["DEST"] == "store"
    assert rows[98][0]["CLASS"] == "LABEL"
    print("tail_zero_hypothesis_samplers", "X16:7 reject; X17:1 STORES; X409:0 store; X410:6 reject")
    print("selected_row129_read", False)
    print("K04_recovered_bits", 0)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python k04_tail_gap_coupling.py original-case.zip")
    synthetic()
    source(read_rows(Path(sys.argv[1])))
