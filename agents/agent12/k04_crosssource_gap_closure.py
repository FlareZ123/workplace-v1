"""K04: cross-source MT state closure using the published TRP2/RC17 links.

Usage: python agents/agent12/k04_crosssource_gap_closure.py case-export.zip
Source-selected row129 and K04 acceptance material excluded.
"""
import sys
from pathlib import Path
from k04_crossgroup_recurrence import extend, bounds

AGENTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AGENTS / 'agent31'))
from k04_mt_recursive_peel import rows, groups, close_group
sys.path.insert(0, str(AGENTS / 'agent23'))
from k04_mt_rowstart import discover

BRIDGES = [(9, 40, 229), (7, 38, 230), (28, 59, 226)]


def investigate(path, bridges):
    values = rows(path)
    assert not values[129]
    source_groups = groups(path, values)
    within, boundary = discover(path)
    assert (len(within), len(boundary)) == (25, 17)
    parent = list(range(133))
    offset = [0] * 133

    def find(row):
        if parent[row] != row:
            older = parent[row]
            parent[row] = find(older)
            offset[row] += offset[older]
        return parent[row]

    def equal(a, b, distance):
        ra, rb = find(a), find(b)
        if ra == rb:
            assert offset[b] - offset[a] == distance
        else:
            parent[rb] = ra
            offset[rb] = distance + offset[a] - offset[b]

    for (a, j), (b, k), (c, l) in within:
        equal(a, b, 397 + j - k)
        equal(a, c, 624 + j - l)
    for a, bit, (b, k), (c, l) in boundary:
        equal(a, b, 396 - k)
        equal(a, c, 623 - l)
    for a, b, distance in bridges:
        equal(a, b, distance)

    merged = {}
    for old_root, original_entries in source_groups.items():
        new_root = find(old_root)
        original_state = close_group(original_entries, values)[0]
        shifted = merged.setdefault(new_root, {})
        for pos, (mask, bits) in original_state.items():
            p = pos + offset[old_root]
            prior_mask, prior_bits = shifted.get(p, (0, 0))
            assert not ((prior_bits ^ bits) & prior_mask & mask)
            shifted[p] = prior_mask | mask, prior_bits | bits
    merged = {root: extend(st) for root, st in merged.items()}

    def compatible(row, gap):
        ra, rb = find(row), find(row + 1)
        if ra == rb:
            return offset[row + 1] - offset[row] == 4 + gap
        shift = 4 + gap + offset[row] - offset[row + 1]
        union = dict(merged[ra])
        for pos, (mask, bits) in merged[rb].items():
            p = pos + shift
            pm, pv = union.get(p, (0, 0))
            if (pv ^ bits) & pm & mask:
                return False
            union[p] = pm | mask, pv | bits
        try:
            extend(union)
        except ValueError:
            return False
        return True

    return {r: next((g for g in range(65) if compatible(r, g)), 0)
            for r in range(132) if r not in (128, 129)}


def main(path):
    _, _, printer, window = bounds(path)
    cross = investigate(path, BRIDGES)
    strict = [(r, printer[r], cross[r]) for r in printer if cross[r] > printer[r]]
    assert strict == [(7, 1, 2), (9, 0, 2)], strict
    assert all(cross[r] >= printer[r] for r in printer)
    print('printer_pair_recurrence_strict_floors', 6)
    print('TRP2_RC17_conditional_bridges', BRIDGES)
    print('new_crosssource_gap_floors', strict)
    print('crosssource_positive_floors', sum(v > 0 for v in cross.values()))
    conditional = investigate(path, BRIDGES + [(80, 81, 6)])
    sampler_extra = [(r, cross[r], conditional[r]) for r in cross if conditional[r] > cross[r]]
    assert sampler_extra == [(111, 0, 1)], sampler_extra
    print('optional_sampler_row80_to81_additional_floor', sampler_extra)
    print('K04_row129_relative_window_not_tightened', window)
    print('no_original_K04_or_K08_acceptance')


if __name__ == '__main__':
    main(Path(sys.argv[1]))
