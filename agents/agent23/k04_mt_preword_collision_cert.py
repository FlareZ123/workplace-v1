"""Prove MT stream spacing from newly inverse-recovered predecessor words.

Run: python agents/agent23/k04_mt_preword_collision_cert.py original-case.zip
Only original SHA-pinned printer source; selected row129 withheld; no REC8 hash.
"""
import sys
from pathlib import Path
from k04_mt_inverse_peel import rows, groups, recover
from k04_mt_rowstart import discover


def certificates(source):
    observed = rows(source)
    reconstructed = groups(source, observed)
    floors = {}
    for root, members in reconstructed.items():
        full, partial, evidence = recover(members, observed)
        for row, start in members:
            if not (1 <= row < 128):
                continue
            suffix = 0
            while start - suffix - 1 in full:
                suffix += 1
            if not suffix:
                continue
            for extra in range(suffix):
                delta = 4 + extra
                overlap = [(j, full[start-j], observed[row-1][delta-j])
                           for j in range(1, suffix+1) if 0 <= delta-j < 4]
                assert any(a != b for j, a, b in overlap), (row, delta, overlap)
            floors[row-1] = suffix
    return floors


def distance_bounds(within, boundary, floors):
    edges = []

    def equal(a, b, distance):
        edges.extend(((a,b,distance),(b,a,-distance)))

    for (a,j),(b,k),(c,l) in within:
        equal(a,b,397+j-k)
        equal(a,c,624+j-l)
    for a,bit,(b,k),(c,l) in boundary:
        equal(a,b,396-k)
        equal(a,c,623-l)
    for r in range(132):
        edges.append((r+1,r,-4-floors.get(r,0)))

    def shortest(start, end):
        distances = [float("inf")] * 133
        distances[start] = 0
        for _ in range(132):
            changed = False
            for a,b,weight in edges:
                if distances[a]+weight < distances[b]:
                    distances[b] = distances[a]+weight
                    changed = True
            if not changed:
                break
        assert not any(distances[a]+weight < distances[b]
                       for a,b,weight in edges)
        return int(distances[end])

    return lambda a,b: (-shortest(b,a),shortest(a,b))


def main(source):
    floors = certificates(source)
    assert floors == {
        2:1, 3:3, 12:1, 13:1, 27:1, 29:1,
        33:2, 37:2, 43:2, 44:2
    }
    within, boundary = discover(source)
    bounds = distance_bounds(within, boundary, floors)
    assert bounds(0,129) == (919,971)
    assert bounds(43,44) == (11,63)
    print("per_transition_min_skipped_words", sorted(floors.items()))
    print("selected_first_word_relative_range", bounds(0,129))
    print("row43_to_row44_output_distance", bounds(43,44))
    print("selected_row129_withheld", True)
    print("K04_K08_UNRESOLVED")


if __name__ == "__main__":
    if len(sys.argv)!=2:
        raise SystemExit("usage: python k04_mt_preword_collision_cert.py original-case.zip")
    main(Path(sys.argv[1]))
