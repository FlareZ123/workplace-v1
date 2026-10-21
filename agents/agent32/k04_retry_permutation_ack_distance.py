"""Conditional H-17 K04 retry-copy minimum-distance witness.

Read-only use: python agents/agent32/k04_retry_permutation_ack_distance.py

The model is hypothetical: one fixed arbitrary permutation of 128 bit positions
maps job0417 requested attempt 1 -> selected attempt 2 -> requested attempt 3,
and maps job0420 first ACK -> second ACK.  The selected ACK is NOT a
source-integrity witness; use it only as a distance anchor.  No original
acceptance digest is used for model fitting or distance optimization.
"""
from collections import defaultdict
from pathlib import Path
from scipy.optimize import Bounds, LinearConstraint, milp
import numpy as np
import re


def to_bits(value):
    return [(byte >> i) & 1 for byte in value for i in range(8)]


def minimum_distance(a, b, c, d, t):
    groups = defaultdict(list)
    for i in range(128):
        groups[(a[i], b[i], c[i], d[i])].append(i)
    labels = sorted(groups)
    n = np.array([len(groups[g]) for g in labels], dtype=int)
    observed_ones = np.array(
        [sum(t[i] for i in groups[g]) for g in labels], dtype=int
    )

    def contribution(g, q):
        aa, bb, cc, dd = g
        vec = np.zeros(8, dtype=int)
        vec[4 * aa + 2 * q + bb] += 1
        vec[4 * q + 2 * cc + dd] -= 1
        return vec

    matrix = np.array(
        [contribution(g, 1) - contribution(g, 0) for g in labels]
    ).T
    rhs = -sum(
        (len(groups[g]) * contribution(g, 0) for g in labels),
        np.zeros(8, dtype=int),
    )
    m = len(labels)
    eye = np.eye(m)
    zeros = np.zeros((8, m))
    constraints = [
        LinearConstraint(np.c_[matrix, zeros], rhs, rhs),
        LinearConstraint(
            np.c_[eye, -eye], np.full(m, -np.inf), observed_ones
        ),
        LinearConstraint(
            np.c_[-eye, -eye], np.full(m, -np.inf), -observed_ones
        ),
    ]
    solution = milp(
        np.r_[np.zeros(m), np.ones(m)],
        integrality=np.r_[np.ones(m), np.zeros(m)],
        bounds=Bounds(np.zeros(2 * m), np.r_[n, np.full(m, 128)]),
        constraints=constraints,
        options={"mip_rel_gap": 0},
    )
    assert solution.success, solution.message
    counts = np.rint(solution.x[:m]).astype(int)
    assert np.array_equal(matrix @ counts, rhs)

    # Construct one closest intermediate Q, preferring the printed ACK bit
    # within each source quadruple group.  This is a witness, not the coupon.
    q = t.copy()
    for g, count in zip(labels, counts):
        indices = groups[g]
        indices = sorted(indices, key=lambda i: t[i], reverse=True)
        on = set(indices[:count])
        for i in indices:
            q[i] = int(i in on)
    distance = sum(qi != ti for qi, ti in zip(q, t))
    assert distance == round(solution.fun)

    # The eight equal counts are also sufficient for a bijective coordinate
    # map: pair equal triple-label buckets to construct a permutation.
    source = defaultdict(list)
    destination = defaultdict(list)
    for i in range(128):
        source[(a[i], q[i], b[i])].append(i)
        destination[(q[i], c[i], d[i])].append(i)
    assert {k: len(v) for k, v in source.items()} == {
        k: len(v) for k, v in destination.items()
    }
    permutation = [0] * 128
    for label, src_indices in source.items():
        for src, dest in zip(src_indices, destination[label]):
            permutation[dest] = src
    assert [a[permutation[i]] for i in range(128)] == q
    assert [q[permutation[i]] for i in range(128)] == c
    assert [b[permutation[i]] for i in range(128)] == d
    return distance, q



def count_nearest(a, b, c, d, t, distance):
    """Count distinct feasible intermediate Q strings at one Hamming radius.

    The 16 quadruple groups each contribute integer s_g and an independently
    countable number of coordinate choices.  Meet-in-the-middle dynamic
    programming tracks an independent row basis of the exact 8 triple-count
    equations.  It counts Q strings, not coordinate permutations.
    """
    from math import comb

    groups = defaultdict(list)
    for i in range(len(t)):
        groups[(a[i], b[i], c[i], d[i])].append(i)
    labels = sorted(groups)
    sizes = [len(groups[g]) for g in labels]
    target_ones = [sum(t[i] for i in groups[g]) for g in labels]

    def contribution(g, bit):
        aa, bb, cc, dd = g
        result = np.zeros(8, dtype=int)
        result[4 * aa + 2 * bit + bb] += 1
        result[4 * bit + 2 * cc + dd] -= 1
        return result

    full = np.array(
        [contribution(g, 1) - contribution(g, 0) for g in labels]
    ).T
    rhs = -sum(
        (len(groups[g]) * contribution(g, 0) for g in labels),
        np.zeros(8, dtype=int),
    )
    baseline = full @ np.array(target_ones, dtype=int)
    independent = []
    for j in range(8):
        if np.linalg.matrix_rank(full[independent + [j], :]) > len(independent):
            independent.append(j)
    matrix = full[independent, :]
    goal = (rhs - baseline)[independent]
    dimensions = len(independent)

    def half(start, stop):
        states = {(0, (0,) * dimensions): 1}
        for j in range(start, stop):
            updated = defaultdict(int)
            for (cost, offset), number in states.items():
                for s in range(sizes[j] + 1):
                    changed = abs(s - target_ones[j])
                    new_cost = cost + changed
                    if new_cost > distance:
                        continue
                    if s <= target_ones[j]:
                        ways = comb(target_ones[j], target_ones[j] - s)
                    else:
                        ways = comb(sizes[j] - target_ones[j], s - target_ones[j])
                    shift = matrix[:, j] * (s - target_ones[j])
                    new_offset = tuple(
                        offset[k] + int(shift[k]) for k in range(dimensions)
                    )
                    updated[(new_cost, new_offset)] += number * ways
            states = updated
        return states

    split = len(labels) // 2
    left = half(0, split)
    right = half(split, len(labels))
    total = 0
    for (cost, offset), number in left.items():
        complement = (
            distance - cost,
            tuple(int(goal[k]) - offset[k] for k in range(dimensions)),
        )
        total += number * right.get(complement, 0)
    return total


def tiny_exact_controls():
    """Blind 12-bit exhaustive controls of the DP count, fixed RNG seed."""
    from itertools import product
    rng = np.random.default_rng(20261021)
    for case in range(5):
        a = rng.integers(0, 2, 12).tolist()
        b = rng.integers(0, 2, 12).tolist()
        p = rng.permutation(12)
        q = [a[i] for i in p]
        c = [q[i] for i in p]
        d = [b[i] for i in p]
        t = rng.integers(0, 2, 12).tolist()
        counts = defaultdict(int)
        for x in product((0, 1), repeat=12):
            if sorted((a[i], x[i], b[i]) for i in range(12)) == sorted(
                (x[i], c[i], d[i]) for i in range(12)
            ):
                counts[sum(x[i] != t[i] for i in range(12))] += 1
        best = min(counts)
        dp_count = count_nearest(a, b, c, d, t, best)
        assert dp_count == counts[best]
        print(f"Tiny control {case+1}: min={best}, "
              f"exact Q count={dp_count} PASS")



def main():
    path = (Path(__file__).resolve().parents[2]
            / "resources/evidence/print/spool-reconstruction.log")
    records = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("2026"):
            continue
        fields = dict(re.findall(r"(\w+)=([^ ]+)", line))
        fields["ts"] = line.split()[0]
        records.append(fields)

    def pick(job, attempt, time):
        found = [r for r in records
                 if r["JOB"] == job
                 and r["ATTEMPT"] == str(attempt)
                 and r["ts"].endswith(time)]
        assert len(found) == 1
        return to_bits(bytes.fromhex(found[0]["PAYLOAD"]))

    a = pick("PS-261003-0417", 1, "18:01:00Z")
    c = pick("PS-261003-0417", 3, "18:03:00Z")
    b = pick("PS-261003-0420", 1, "17:00:00+00:00")
    d = pick("PS-261003-0420", 2, "18:25:00Z")
    printed = pick("PS-261003-0417", 2, "18:02:00Z")
    distance, q = minimum_distance(a, b, c, d, printed)
    print(f"Original conditional minimum Hamming distance: {distance}")
    print("Hypothetical nearest Q (NOT authenticated): "
          + bytes(sum(q[8*i+j] << j for j in range(8))
                  for i in range(16)).hex().upper())
    assert distance == 14
    count = count_nearest(a, b, c, d, printed, distance)
    print(f"Exact nearest Q candidate count: {count:,}")
    assert count == 1665398756
    tiny_exact_controls()
    # Source-selected ACK proximity is evidence for this copy model only if
    # unusually tight relative to unrelated printed 64-one coupon strings.
    # Keep the four source endpoints fixed and permute ACK bit positions.
    calibration_rng = np.random.default_rng(20261021)
    null_distances = [
        minimum_distance(a, b, c, d,
                         calibration_rng.permutation(printed).tolist())[0]
        for _ in range(100)
    ]
    at_most_observed = sum(value <= distance for value in null_distances)
    print(f"Matched-weight shuffled ACK control: {at_most_observed}/100 "
          f"at or below the actual distance {distance}")
    assert at_most_observed == 63

    rng = np.random.default_rng(20261021)
    for test in range(5):
        sa = rng.integers(0, 2, 128).tolist()
        sb = rng.integers(0, 2, 128).tolist()
        p = rng.permutation(128).tolist()
        sq = [sa[i] for i in p]
        sc = [sq[i] for i in p]
        sd = [sb[i] for i in p]
        st = sq.copy()
        for i in rng.choice(128, 6, replace=False):
            st[int(i)] ^= 1
        control_distance, _ = minimum_distance(sa, sb, sc, sd, st)
        assert control_distance <= 6
        print(f"Synthetic control {test + 1}: distance "
              f"{control_distance} <= 6 PASS")
    print("Complete: selected coupon not recovered; acceptance unchanged")


if __name__ == "__main__":
    main()
