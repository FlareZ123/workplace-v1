"""Original-spool K04 global-position inverse-MT triplet discriminator.

Usage: python agents/agent4/k04_global_inverse_triplet.py original-case.zip
Requires only Python stdlib and the repository's Agent23 witness scanner.
Does not read the disputed row129, K04/K08 commitments, or source mask.
"""
import random
import re
import struct
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "agent23"))
from k04_mt_rowstart import discover, untemper

STARTS = (
    0, 6, 12, 21, 29, 35, 41, 47, 57, 63, 74, 82, 89, 102, 110, 116,
    122, 128, 134, 140, 146, 152, 158, 164, 170, 176, 182, 188, 194, 200,
    207, 230, 236, 242, 249, 255, 261, 267, 279, 288, 294, 301, 308, 318,
    329, 336, 342, 348, 354, 360, 366, 372, 378, 394, 400, 406, 415, 422,
    428, 434, 440, 446, 453, 459, 471, 479, 485, 497, 505, 512, 518, 524,
    530, 536, 550, 556, 562, 568, 574, 580, 587, 593, 600, 624, 631, 637,
    643, 649, 655, 661, 667, 673, 679, 687, 695, 704, 711, 723, 730, 737,
    743, 749, 755, 761, 767, 776, 783, 789, 795, 801, 807, 816, 822, 829,
    853, 860, 869, 875, 881, 887, 893, 900, 906, 912, 918, 924, 930, 936,
    941, 945, 949, 953, 957,
)

def untwist(delta):
    """Return the packed MT twist predecessor-high/successor-low31 pair."""
    parity = delta >> 31
    return (((delta ^ (0x9908B0DF if parity else 0)) << 1) | parity) & 0xFFFFFFFF

def main(source):
    within, boundary = discover(source)  # SHA-pinned, selected row129 excluded
    assert (len(within), len(boundary)) == (25, 17)
    with zipfile.ZipFile(source) as z:
        lines = [x for x in z.read("evidence/print/spool-reconstruction.log")
                 .decode().splitlines() if x.startswith("2026-")]
    assert len(lines) == 133 and len(STARTS) == 133
    values = [
        [untemper(w) for w in struct.unpack(
            "<4I", bytes.fromhex(re.search(r"PAYLOAD=([0-9A-F]{32})", line).group(1))
        )] for line in lines
    ]
    values[129] = []
    edges = []

    def equality(a, b, displacement):
        assert STARTS[b] - STARTS[a] == displacement
        edges.extend(((a, b, displacement), (b, a, -displacement)))

    for (a, j), (b, k), (c, l) in within:
        equality(a, b, 397 + j - k)
        equality(a, c, 624 + j - l)
    for a, bit, (b, k), (c, l) in boundary:
        equality(a, b, 396 - k)
        equality(a, c, 623 - l)
    for r in range(132):
        floor = 6 if r < 127 else 4
        displacement = STARTS[r + 1] - STARTS[r]
        assert floor <= displacement <= 24
        edges.extend(((r, r + 1, floor), (r + 1, r, -24)))

    # Independent optimality certificate for the minimal 957-output span.
    lower = [float("-inf")] * 133
    lower[0] = 0
    for _ in range(132):
        for a, b, displacement in edges:
            if lower[a] + displacement > lower[b]:
                lower[b] = lower[a] + displacement
    assert all(lower[a] + displacement <= lower[b]
               for a, b, displacement in edges)
    assert lower[132] == STARTS[132] == 957

    observed = {STARTS[r] + j: word for r, ws in enumerate(values)
                for j, word in enumerate(ws)}
    location = {STARTS[r] + j: (r, j) for r, ws in enumerate(values)
                for j, _ in enumerate(ws)}
    assert len(observed) == 528
    mismatches = []
    tested = 0
    for middle in observed:
        t = middle - 397
        end = t + 624
        if end not in observed:
            continue
        implied = untwist(observed[middle] ^ observed[end])
        if t in observed:
            tested += 1
            if (implied ^ observed[t]) & 0x80000000:
                mismatches.append(("predecessor-msb", location[t],
                                   location[middle], location[end]))
        if t + 1 in observed:
            tested += 1
            if (implied ^ observed[t + 1]) & 0x7FFFFFFF:
                mismatches.append(("successor-low31", location[t + 1],
                                   location[middle], location[end]))
    assert tested == 134 and len(mismatches) == 49
    assert ("predecessor-msb", (0, 3), (54, 0), (83, 3)) in mismatches

    # Ground-truth MT stream: source-independent inversion calibration.
    rng = random.Random(20261019)
    x = [untemper(rng.getrandbits(32)) for _ in range(900)]
    assert all((untwist(x[t + 397] ^ x[t + 624]) >> 31) ==
               (x[t] >> 31) and
               (untwist(x[t + 397] ^ x[t + 624]) & 0x7FFFFFFF) ==
               (x[t + 1] & 0x7FFFFFFF) for t in range(276))
    print("source positive witnesses: 42")
    print("conditional minimal stream span: 957")
    print("full inverse-triplet checks:", tested, "contradictions:", len(mismatches))
    print("excluded index triple: X[3], X[400], X[627]")
    print("observed: 8A037AD0 AF4CF577 A52674B5")
    print("inferred X[3] high bit: 0; observed: 1")
    print("synthetic independent MT inversion: PASS")
    print("original K04 bytes: unrecovered")

if __name__ == "__main__":
    main(sys.argv[1])
