"""Conditional source-only K04 global inverse-triplet mixed-integer placement.

Run: python agents/agent1/k04_global_inverse_milp.py ORIGINAL_EXPORT.zip
Requires scipy, numpy and agents/agent23/k04_mt_rowstart.py.
Excludes disputed spool row129, masks, K04/K08 commitments, and verifier.
"""
import random
import re
import struct
import sys
import time
import zipfile
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import coo_matrix

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "agent23"))
from k04_mt_rowstart import discover, untemper

N = 133


def untwist(delta):
    parity = delta >> 31
    return (((delta ^ (0x9908B0DF if parity else 0)) << 1) | parity) & 0xFFFFFFFF


def read_source(path):
    within, boundary = discover(path)  # SHA-pinned by upstream source reader.
    assert (len(within), len(boundary)) == (25, 17)
    with zipfile.ZipFile(path) as archive:
        raw = archive.read("evidence/print/spool-reconstruction.log").decode()
    words = []
    for line in raw.splitlines():
        if line.startswith("2026-"):
            payload = bytes.fromhex(re.search(r"PAYLOAD=([0-9A-F]{32})", line)[1])
            words.append([untemper(value) for value in struct.unpack("<4I", payload)])
    assert len(words) == N
    words[129] = []  # The disputed K04 ACK is never a constraint or control.
    equalities = []
    for (a, j), (b, k), (c, l) in within:
        equalities.extend(((a, b, 397 + j - k), (a, c, 624 + j - l)))
    for a, bit, (b, k), (c, l) in boundary:
        equalities.extend(((a, b, 396 - k), (a, c, 623 - l)))
    return words, equalities


def contradictions(starts, words):
    seen = {starts[r] + j: val for r, row in enumerate(words)
            for j, val in enumerate(row)}
    locations = {starts[r] + j: (r, j) for r, row in enumerate(words)
                 for j, _ in enumerate(row)}
    failures = []
    for middle, value in seen.items():
        preceding = middle - 397
        end = preceding + 624
        if end not in seen:
            continue
        implied = untwist(value ^ seen[end])
        if preceding in seen and (implied ^ seen[preceding]) & 0x80000000:
            failures.append(("msb", locations[preceding],
                             locations[middle], locations[end]))
        if preceding + 1 in seen and (implied ^ seen[preceding + 1]) & 0x7FFFFFFF:
            failures.append(("low31", locations[preceding + 1],
                             locations[middle], locations[end]))
    return failures


def solve(equalities, cuts, time_limit=20):
    size = N + 4 * len(cuts)
    rr, cc, vv, lows, highs = [], [], [], [], []

    def add(coefficients, low=-np.inf, high=np.inf):
        index = len(lows)
        lows.append(low)
        highs.append(high)
        for variable, coefficient in coefficients.items():
            if coefficient:
                rr.append(index)
                cc.append(variable)
                vv.append(coefficient)

    for a, b, distance in equalities:
        add({a: -1, b: 1}, distance, distance)
    for row in range(N - 1):
        minimum = 6 if row < 127 else 4
        add({row: -1, row + 1: 1}, minimum, 24)

    # Each inverse-triplet mismatch forbids BOTH proposed relative
    # distances holding simultaneously. These are conditional MT no-goods.
    BIG = 5000
    for number, (kind, (a, i), (b, j), (c, k)) in enumerate(cuts):
        anchor = i - (1 if kind == "low31" else 0)
        d1, d2 = 397 + anchor - j, 624 + anchor - k
        tests = (({a: -1, b: 1}, d1, True),
                 ({a: -1, b: 1}, d1, False),
                 ({a: -1, c: 1}, d2, True),
                 ({a: -1, c: 1}, d2, False))
        for q, (expr, delta, below) in enumerate(tests):
            selected = N + 4 * number + q
            row = dict(expr)
            row[selected] = BIG if below else -BIG
            if below:
                add(row, high=delta - 1 + BIG)
            else:
                add(row, low=delta + 1 - BIG)
        add({N + 4 * number + q: 1 for q in range(4)}, low=1)

    matrix = coo_matrix((np.asarray(vv, dtype=float),
                        (np.asarray(rr), np.asarray(cc))),
                        shape=(len(lows), size)).tocsc()
    minimum = np.zeros(size)
    maximum = np.full(size, 3168.)
    maximum[0] = 0
    maximum[N:] = 1
    objective = np.zeros(size)
    objective[132] = 1
    result = milp(
        c=objective,
        integrality=np.ones(size),
        bounds=Bounds(minimum, maximum),
        constraints=LinearConstraint(matrix, np.asarray(lows), np.asarray(highs)),
        options={"time_limit": time_limit, "mip_rel_gap": 0.0},
    )
    if result.x is None:
        return result, None
    return result, [int(round(x)) for x in result.x[:N]]


def main(path):
    words, equalities = read_source(path)
    known = set()
    cuts = []
    certified_lower = 957
    for iteration in range(21):
        result, positions = solve(equalities, cuts)
        if result.status != 0 or positions is None:
            print("solver_partial_or_unavailable", iteration, result.message)
            break
        certified_lower = max(certified_lower, int(round(result.fun)))
        failures = contradictions(positions, words)
        print("iteration", iteration, "no_goods", len(cuts),
              "minimum_final_source_index", positions[132],
              "newly_contradicted_triplets", len(failures))
        if not failures:
            print("global_consistent_layout", positions)
            break
        fresh = [item for item in failures if item not in known]
        if not fresh:
            print("stalled_without_complete_layout")
            break
        for item in fresh:
            known.add(item)
            cuts.append(item)
        if len(cuts) >= 500:
            print("cut_budget_reached")
            break
    # A genuine MT stream must never yield any negative recurrence witness
    # when actual output indices are used, even for sparse observed rows.
    seeds = (0x3341, 777, 20261019)
    actual_starts = list(range(0, 133 * 6, 6))
    for seed in seeds:
        rng = random.Random(seed)
        outputs = [untemper(rng.getrandbits(32)) for _ in range(1000)]
        fixture = [outputs[actual_starts[r]:actual_starts[r] + 4]
                   if r != 129 else [] for r in range(N)]
        assert not contradictions(actual_starts, fixture)
    print("true_MT_sparse_positive_controls", len(seeds))
    print("certified_lower_bound_s132", certified_lower)
    print("known_target_bits_recovered", 0)
    print("selected_ACK_omitted", True)


if __name__ == "__main__":
    main(Path(sys.argv[1]))
