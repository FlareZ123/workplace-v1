"""Source-only K04 index tightening from recovered MT word non-equality.

Run: python agents/agent6/k04_mt_word_nonoverlap.py original-case.zip
No acceptance, route, class-sampler or guessed metadata draws required.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "agent23"))
from k04_mt_inverse_peel import groups, rows
from k04_mt_rowstart import discover
from k04_mt_ternary_class_gate import close_group
from k04_mt_metadata_draw_bounds import constraints, interval


def main(source):
    words = rows(source)
    assert not words[129]
    clusters = groups(source, words)
    minimum = [4] * 132
    constrained = []
    for entries in clusters.values():
        full, _ = close_group(entries, words)
        for row, start in entries:
            if row == 0 or row == 130 or not words[row - 1]:
                continue
            distance = 4
            while distance < 80:
                # If preceding row ended at index start-distance+3,
                # reconstructed values at identical positions must agree.
                conflicts = [
                    (j, start - distance + j)
                    for j, previous_word in enumerate(words[row - 1])
                    if start - distance + j in full
                    and full[start - distance + j] != previous_word
                ]
                if not conflicts:
                    break
                distance += 1
            if distance > minimum[row - 1]:
                minimum[row - 1] = distance
                constrained.append((row - 1, row, distance))
    constrained.sort()
    expected = [
        (2,3,5), (3,4,7), (12,13,5), (13,14,5),
        (27,28,5), (29,30,5), (33,34,6), (37,38,6),
        (43,44,6), (44,45,6), (73,74,5), (92,93,6),
    ]
    assert constrained == expected

    within, boundary = discover(source)
    assert (len(within), len(boundary)) == (25, 17)
    edges = constraints(within, boundary, 4)
    edges[-132:] = [(r+1, r, -minimum[r]) for r in range(132)]
    selected = interval(edges, 0, 129)
    gap = interval(edges, 43, 44)
    assert selected == (919, 971)
    assert gap == (11, 63)
    print("selected_row129_withheld", True)
    print("source_only_nonoverlap_transition_floors", constrained)
    print("source_only_s129_minus_s0", selected,
          "number_of_possible_start_indices", selected[1]-selected[0]+1)
    print("source_only_s44_minus_s43", gap)
    print("no_metadata_generation_assumption", True)
    print("K04_K08_UNRESOLVED")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python k04_mt_word_nonoverlap.py original-case.zip")
    main(Path(sys.argv[1]))
