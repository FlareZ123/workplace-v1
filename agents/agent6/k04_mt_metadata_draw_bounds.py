"""K04 conditional row-start bounds under regular-class metadata draw floors.

Read-only: python agents/agent6/k04_mt_metadata_draw_bounds.py original-case.zip
Selected row129 withheld by the existing SHA-pinned witness discoverer.
No acceptance, mask, K04 candidate or K08 phrase read.
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "agent23"))
from k04_mt_rowstart import discover


def constraints(within, boundary, minimum):
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
        # 0..126: both sides are regular rows, rest require only four words.
        edges.append((r + 1, r, -(minimum if r < 127 else 4)))
    return edges


def shortest(edges, start, end):
    dist = [math.inf] * 133
    dist[start] = 0
    for _ in range(132):
        changed = False
        for a, b, weight in edges:
            if dist[a] + weight < dist[b]:
                dist[b] = dist[a] + weight
                changed = True
        if not changed:
            break
    if any(dist[a] + weight < dist[b] for a, b, weight in edges):
        raise ValueError("negative cycle: draw-floor hypothesis contradicted")
    return dist[end]


def interval(edges, start, end):
    return (-shortest(edges, end, start),
            shortest(edges, start, end))


def main(source):
    within, boundary = discover(source)
    assert (len(within), len(boundary)) == (25, 17)
    print("selected_row_129_withheld", True)
    print("source_only_witnesses", len(within) + len(boundary))
    for floor in (4, 5, 6, 7):
        edges = constraints(within, boundary, floor)
        try:
            target = interval(edges, 0, 129)
            gap = interval(edges, 43, 44)
        except ValueError:
            print("regular_transition_minimum", floor, "INFEASIBLE")
            assert floor == 7
            continue
        print("regular_transition_minimum", floor,
              "s129_relative_to_s0", target,
              "target_indices", target[1] - target[0] + 1,
              "s44_minus_s43", gap)
        assert {
            4: ((917, 971), (11, 65)),
            5: ((931, 963), (11, 43)),
            6: ((945, 955), (11, 21)),
        }[floor] == (target, gap)
    print("K04_K08_UNRESOLVED")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python k04_mt_metadata_draw_bounds.py original-case.zip")
    main(Path(sys.argv[1]))
