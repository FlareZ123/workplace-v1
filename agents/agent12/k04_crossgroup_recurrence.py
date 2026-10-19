"""K04: tighten printer skip bounds using MT19937 closure after joining source groups.

Usage: python agents/agent12/k04_crossgroup_recurrence.py case-export.zip
Source-only; printer row129, recovery commitments and route sheets withheld.
"""
import math
import sys
from pathlib import Path

AGENTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AGENTS / 'agent31'))
from k04_mt_recursive_peel import rows, groups, close_group
sys.path.insert(0, str(AGENTS / 'agent23'))
from k04_mt_rowstart import discover

ALL = 0xFFFFFFFF
A = 0x9908B0DF


def twist(first, second):
    mixed = (first & 0x80000000) | (second & 0x7FFFFFFF)
    return ((mixed >> 1) ^ (A if mixed & 1 else 0)) & ALL


def extend(state):
    state = dict(state)

    def add(index, mask, bits):
        old_mask, old_bits = state.get(index, (0, 0))
        if (old_bits ^ bits) & old_mask & mask:
            raise ValueError('contradictory MT state bits')
        if old_mask | mask == old_mask:
            return False
        state[index] = old_mask | mask, old_bits | bits
        return True

    while True:
        changed = False
        for end, (mask, word) in list(state.items()):
            mid = end - 227
            if mask == ALL and state.get(mid, (0, 0))[0] == ALL:
                delta = word ^ state[mid][1]
                low = delta >> 31
                first = (((delta ^ (A if low else 0)) << 1) | low) & ALL
                changed |= add(end - 624, 0x80000000, first & 0x80000000)
                changed |= add(end - 623, 0x7FFFFFFF, first & 0x7FFFFFFF)
        for index, (mask, first) in list(state.items()):
            if not (mask & 0x80000000):
                continue
            next_mask, second = state.get(index + 1, (0, 0))
            if next_mask & 0x7FFFFFFF != 0x7FFFFFFF:
                continue
            mid_mask, mid = state.get(index + 397, (0, 0))
            end_mask, end = state.get(index + 624, (0, 0))
            delta = twist(first, second)
            if mid_mask == ALL:
                changed |= add(index + 624, ALL, mid ^ delta)
            if end_mask == ALL:
                changed |= add(index + 397, ALL, end ^ delta)
        if not changed:
            return state


def bounds(source):
    values = rows(source)
    assert not values[129], 'source-selected K04 row must be withheld'
    grouped = groups(source, values)
    states = {root: close_group(group, values)[0] for root, group in grouped.items()}
    group_of = {}
    offset = {}
    for root, group in grouped.items():
        for row, start in group:
            group_of[row] = root
            offset[row] = start

    def can_join(row, gap, close):
        left, right = group_of[row], group_of[row + 1]
        if left == right:
            return offset[row + 1] - offset[row] == gap + 4
        shift = gap + 4 + offset[row] - offset[row + 1]
        merged = dict(states[left])
        for p, (mask, bits) in states[right].items():
            position = p + shift
            old_mask, old_bits = merged.get(position, (0, 0))
            if (old_bits ^ bits) & old_mask & mask:
                return False
            merged[position] = old_mask | mask, old_bits | bits
        if close:
            try:
                extend(merged)
            except ValueError:
                return False
        return True

    prior = {}
    stronger = {}
    for row in range(132):
        if row in (128, 129):
            continue
        prior[row] = next((g for g in range(65) if can_join(row, g, False)), 0)
        stronger[row] = next((g for g in range(65) if can_join(row, g, True)), 0)
    assert not [(r, prior[r], stronger[r]) for r in prior if stronger[r] < prior[r]]
    differences = [(r, prior[r], stronger[r]) for r in prior if stronger[r] > prior[r]]
    assert differences == [(30, 1, 2), (53, 2, 3), (63, 0, 1),
                           (82, 2, 3), (113, 2, 3), (126, 1, 2)], differences

    within, boundary = discover(source)
    assert len(within) == 25 and len(boundary) == 17

    def interval(floors):
        edges = []
        def equal(a, b, d):
            edges.extend(((a, b, d), (b, a, -d)))
        for (a, j), (b, k), (c, l) in within:
            equal(a, b, 397 + j - k)
            equal(a, c, 624 + j - l)
        for a, bit, (b, k), (c, l) in boundary:
            equal(a, b, 396 - k)
            equal(a, c, 623 - l)
        for r in range(132):
            edges.append((r + 1, r, -4 - floors.get(r, 0)))
        def shortest(a, b):
            d = [math.inf] * 133
            d[a] = 0
            for _ in range(133):
                changed = False
                for x, y, weight in edges:
                    if d[y] > d[x] + weight:
                        d[y] = d[x] + weight
                        changed = True
                if not changed:
                    break
            assert not changed, 'inconsistent source chronology'
            return d[b]
        return -shortest(129, 0), shortest(0, 129)

    assert interval({}) == (917, 971)
    assert interval(prior) == (922, 971)
    assert interval(stronger) == (923, 971)
    return differences, prior, stronger, interval(stronger)


def main(path):
    improvements, old, new, window = bounds(path)
    print('selected_row_129_withheld', True)
    print('original_42_witnesses', 42)
    print('baseline_positive_gap_floors', sum(v > 0 for v in old.values()))
    print('recurrence_positive_gap_floors', sum(v > 0 for v in new.values()))
    print('strictly_improved_transitions', improvements)
    print('source_conditional_s129_minus_s0', window)
    print('original_K04_and_K08_UNRESOLVED')


if __name__ == '__main__':
    main(Path(sys.argv[1]))
