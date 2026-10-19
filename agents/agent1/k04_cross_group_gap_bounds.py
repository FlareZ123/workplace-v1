"""K04 source-only skipped MT word lower bounds between distinct witness groups.

Run: python agents/agent1/k04_cross_group_gap_bounds.py original-case.zip
Selected row129 withheld; no K04 commitments or printer XOR mask read.
Uses independently recovered full/partial MT words from Agent31 and the
source-fixed 42 recurrence witness group coordinates of Agent23.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "agent31"))
from k04_mt_recursive_peel import rows, groups, close_group
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "agent23"))
from k04_mt_rowstart import discover


def experiment(path):
    values = rows(path)
    assert not values[129]
    clusters = groups(path, values)
    group_of = {}
    offset_of = {}
    group_state = {}
    for root, entries in clusters.items():
        state, _ = close_group(entries, values)
        group_state[root] = state
        for row, offset in entries:
            group_of[row] = root
            offset_of[row] = offset

    def compatible(a, b, distance):
        ra, rb = group_of[a], group_of[b]
        shift = distance + offset_of[a] - offset_of[b]
        aa, bb = group_state[ra], group_state[rb]
        for p, (mask, word) in aa.items():
            v = bb.get(p - shift)
            if v is not None and (word ^ v[1]) & mask & v[0]:
                return False
        return True

    def minimum_gap(row):
        if row in (128, 129):
            return 0
        if group_of[row] == group_of[row + 1]:
            return offset_of[row + 1] - offset_of[row] - 4
        for gap in range(65):
            if compatible(row, row + 1, 4 + gap):
                return gap
        # Unknown: a stronger bound requires examining larger skips.
        return 0

    floors = [minimum_gap(r) for r in range(132)]
    positive = [(r, g) for r, g in enumerate(floors) if g > 0]
    assert len(positive) == 46, positive
    assert floors[92] >= 3

    within, boundary = discover(path)
    assert (len(within), len(boundary)) == (25, 17)

    def window(added):
        edges = []
        def equal(a, b, delta):
            edges.append((a, b, delta))
            edges.append((b, a, -delta))
        for (a, j), (b, k), (c, l) in within:
            equal(a, b, 397 + j - k)
            equal(a, c, 624 + j - l)
        for a, bit, (b, k), (c, l) in boundary:
            equal(a, b, 396 - k)
            equal(a, c, 623 - l)
        for r in range(132):
            edges.append((r + 1, r, -4 - added[r]))

        def shortest(start, end):
            costs = [float("inf")] * 133
            costs[start] = 0
            for _ in range(132):
                changed = False
                for a, b, weight in edges:
                    if costs[a] + weight < costs[b]:
                        costs[b] = costs[a] + weight
                        changed = True
                if not changed:
                    break
            assert not any(costs[a] + weight < costs[b]
                           for a, b, weight in edges)
            return costs[end]
        return -shortest(129, 0), shortest(0, 129)

    original = window([0] * 132)
    tightened = window(floors)
    assert original == (917, 971), original
    assert tightened == (922, 971), tightened
    print("row129_source_withheld", True)
    print("positive_gap_floors", positive)
    print("original_42_witness_stream_window", original)
    print("cross_group_conflict_refined_window", tightened)
    print("K04_K08_UNRESOLVED")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python agents/agent1/k04_cross_group_gap_bounds.py original-case.zip")
    experiment(Path(sys.argv[1]))
