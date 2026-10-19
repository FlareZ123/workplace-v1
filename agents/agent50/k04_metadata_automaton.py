"""Infer bounded ordinary-printer MT gaps from CLASS/DEST rejection samplers.
Usage: python agents/agent50/k04_metadata_automaton.py original-export.zip
Original selected row129 and all REC8 commitments, route and mask withheld.
"""
import math
import re
import sys
from pathlib import Path
from zipfile import ZipFile

AGENTS = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(AGENTS / 'agent12'), str(AGENTS / 'agent31'), str(AGENTS / 'agent23')]
from k04_crossgroup_recurrence import extend
from k04_mt_recursive_peel import rows, groups, close_group, temper
from k04_mt_rowstart import discover

ALL = 0xffffffff
DEST = {'store': 0, 'desk': 1, 'bench': 2}
CLASS = {'LABEL': 0, 'STORES': 1, 'RECOVER': 2}


def output_codes(mask, bits, width):
    base = temper(bits) >> (32 - width)
    span = {0}
    for bit in range(32):
        if not mask & (1 << bit):
            change = temper(1 << bit) >> (32 - width)
            span |= {x ^ change for x in tuple(span)}
            if len(span) == 1 << width:
                break
    return {base ^ code for code in span}


def sampler_accepts(state, row, gap, starts, labels, class_size):
    dest, next_class = labels[row][1], labels[row + 1][0]
    possible = {0}  # 0 = DEST pending, 1 = CLASS pending, 2 = complete
    for j in range(4, gap + 4):
        mask, bits = state.get(starts[row] + j, (0, 0))
        following = set()
        for phase in possible:
            if phase == 0:
                for code in output_codes(mask, bits, 2):
                    if code == 3:
                        following.add(0)
                    if code == DEST[dest]:
                        following.add(1)
            if phase == 1:
                for code in output_codes(mask, bits, 3):
                    if code >= class_size:
                        following.add(1)
                    if code == CLASS[next_class] or (
                        class_size == 4 and code == 3 and next_class == 'LABEL'
                    ):
                        following.add(2)
        if j < gap + 3:
            following.discard(2)
        possible = following
        if not possible:
            return False
    return 2 in possible


def position_bounds(within, boundary, floors):
    edges = []
    def equal(a, b, delta):
        edges.extend(((a, b, delta), (b, a, -delta)))
    for (a, j), (b, k), (c, l) in within:
        equal(a, b, 397 + j - k)
        equal(a, c, 624 + j - l)
    for a, bit, (b, k), (c, l) in boundary:
        equal(a, b, 396 - k)
        equal(a, c, 623 - l)
    for row in range(132):
        edges.append((row + 1, row, -4 - floors.get(row, 0)))
    def shortest(a, b):
        distances = [math.inf] * 133
        distances[a] = 0
        for _ in range(133):
            changed = False
            for x, y, weight in edges:
                if distances[x] + weight < distances[y]:
                    distances[y] = distances[x] + weight
                    changed = True
            if not changed:
                break
        assert not changed
        return distances[b]
    return -shortest(129, 0), shortest(0, 129)


def main(source):
    values = rows(source)
    assert len(values) == 133 and not values[129]
    with ZipFile(source) as archive:
        lines = [line for line in archive.read(
            'evidence/print/spool-reconstruction.log').decode().splitlines()
            if line.startswith('2026-')]
    assert len(lines) == 133
    labels = [(re.search(r'CLASS=([A-Z]+)', line).group(1),
               re.search(r'DEST=([a-z]+)', line).group(1))
              for line in lines]
    clusters = groups(source, values)
    states = {root: close_group(entries, values)[0] for root, entries in clusters.items()}
    root_of, starts = {}, {}
    for root, entries in clusters.items():
        for row, start in entries:
            root_of[row], starts[row] = root, start

    def joined(row, gap):
        a, b = root_of[row], root_of[row + 1]
        if a == b:
            return states[a] if starts[row + 1] - starts[row] == gap + 4 else None
        shift = starts[row] + gap + 4 - starts[row + 1]
        state = dict(states[a])
        for index, (mask, bits) in states[b].items():
            shifted = index + shift
            oldmask, oldbits = state.get(shifted, (0, 0))
            if (oldbits ^ bits) & oldmask & mask:
                return None
            state[shifted] = (oldmask | mask, oldbits | bits)
        try:
            return extend(state)
        except ValueError:
            return None

    within, boundary = discover(source)
    assert len(within) == 25 and len(boundary) == 17
    print('selected_row129_withheld', True)
    for class_size in (3, 4):
        allowed = {
            row: [gap for gap in range(65)
                  if (state := joined(row, gap)) is not None
                  and sampler_accepts(state, row, gap, starts, labels, class_size)]
            for row in range(127)
        }
        assert all(allowed.values())
        floors = {row: min(gaps) for row, gaps in allowed.items()}
        assert floors[12] == 5
        assert allowed[80] == [2]
        assert allowed[99] == (list(range(3, 65)) if class_size == 3 else [2])
        window = position_bounds(within, boundary, floors)
        assert window == (945, 955)
        print('CLASS_sampler_n', class_size)
        print('transitions_with_gap_gt2', sum(n > 2 for n in floors.values()))
        print('transitions_with_gap_ge4', sum(n >= 4 for n in floors.values()))
        print('row12_min_gap', floors[12])
        print('row80_gaps', allowed[80])
        print('row99_gaps', allowed[99][:5], 'count', len(allowed[99]))
        print('s129_minus_s0', window)
    print('K04_K08_UNRESOLVED')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: python k04_metadata_automaton.py original-export.zip')
    main(Path(sys.argv[1]))
