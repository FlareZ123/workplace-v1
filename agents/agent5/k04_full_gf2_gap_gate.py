"""Source-only K04 MT19937 full-GF(2) gap gate.

Run from repository root:
    python agents/agent5/k04_full_gf2_gap_gate.py original-members.zip

The selected printer row129, K04 mask, commitments, and K08 nonce are never read.
Input SHA, the 42 original witnesses and all inferred state words are pinned by
upstream source-only parsers. This script adds a complete *linear* MT19937
consistency test for alternative offsets of neighboring witness groups.
"""
import random
import sys
from pathlib import Path

AGENTS = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(AGENTS / 'agent23'), str(AGENTS / 'agent31')]
from k04_mt_inverse_peel import groups, rows
from k04_mt_recursive_peel import close_group
from k04_mt_rowstart import discover, untemper

A = 0x9908B0DF


def symbolic(max_index):
    """Linear output bit expressions in 624 consecutive untempered MT words."""
    states = [[1 << (32 * i + b) for b in range(32)] for i in range(624)]
    for n in range(624, max_index + 1):
        older, successor, middle = states[n - 624], states[n - 623], states[n - 227]
        word = []
        for bit in range(32):
            vector = middle[bit]
            if bit < 31:
                vector ^= older[31] if bit == 30 else successor[bit + 1]
            if (A >> bit) & 1:
                vector ^= successor[0]
            word.append(vector)
        states.append(word)
    return states


def add_equation(expression, value, basis):
    while expression:
        pivot = expression.bit_length() - 1
        previous = basis.get(pivot)
        if previous is None:
            basis[pivot] = (expression, value)
            return True
        expression ^= previous[0]
        value ^= previous[1]
    return value == 0


def add_observations(observations, shift, origin, symbolic_states, basis):
    """None for consistent; otherwise first disproved (relative index, bit)."""
    for index, (mask, value) in observations.items():
        expressions = symbolic_states[index + shift - origin]
        while mask:
            low = mask & -mask
            bit = low.bit_length() - 1
            if not add_equation(expressions[bit], (value >> bit) & 1, basis):
                return index, bit
            mask ^= low
    return None


def original_overlap_compatible(a, b, shift):
    for index, (mask, bits) in a.items():
        other = b.get(index - shift)
        if other is not None and ((bits ^ other[1]) & mask & other[0]):
            return False
    return True


def source_floor(row, cluster_id, row_offset, states, use_full_gf2, max_gap=64):
    if row in (128, 129):
        return 0  # Deliberately withhold selected ACK and its direct transitions.
    left = cluster_id[row]
    right = cluster_id[row + 1]
    if left == right:
        return row_offset[row + 1] - row_offset[row] - 4
    a, b = states[left], states[right]
    base_shift = row_offset[row] + 4 - row_offset[row + 1]
    if use_full_gf2:
        origin = min(min(a), min(b) + base_shift)
        end = max(max(a), max(b) + base_shift + max_gap) - origin
        expressions = symbolic(end)
        basis = {}
        assert add_observations(a, 0, origin, expressions, basis) is None
    for skipped in range(max_gap + 1):
        shift = base_shift + skipped
        if use_full_gf2:
            test = basis.copy()
            possible = add_observations(b, shift, origin, expressions, test) is None
        else:
            possible = original_overlap_compatible(a, b, shift)
        if possible:
            return skipped
    # Preserve the earlier conservative convention if none passes the bound.
    return 0


def interval(within, boundary, floors):
    edges = []
    def equal(a, b, distance):
        edges.extend(((a, b, distance), (b, a, -distance)))
    for (a, j), (b, k), (c, l) in within:
        equal(a, b, 397 + j - k)
        equal(a, c, 624 + j - l)
    for a, bit, (b, k), (c, l) in boundary:
        equal(a, b, 396 - k)
        equal(a, c, 623 - l)
    edges.extend((r + 1, r, -4 - floors[r]) for r in range(132))

    def shortest(a, b):
        dist = [float('inf')] * 133
        dist[a] = 0
        for _ in range(132):
            improved = False
            for start, stop, weight in edges:
                if dist[start] + weight < dist[stop]:
                    dist[stop] = dist[start] + weight
                    improved = True
            if not improved:
                break
        assert not any(dist[a] + w < dist[b] for a, b, w in edges)
        return dist[b]

    return -shortest(129, 0), shortest(0, 129)


def control():
    """Independent CPython MT output proves the linear expression bit order."""
    for seed in (1, 0xDEADBEEF, 0xAB39EF012345ABCDEF):
        stream = random.Random(seed)
        words = [untemper(stream.getrandbits(32)) for _ in range(1000)]
        independent = symbolic(999)
        input_bits = sum(word << (32 * i) for i, word in enumerate(words[:624]))
        for index in (624, 625, 627, 792, 999):
            expected = sum(
                ((vector & input_bits).bit_count() & 1) << bit
                for bit, vector in enumerate(independent[index])
            )
            assert expected == words[index], (seed, index)
    print('SYNTHETIC_MT_LINEAR_MODEL_PASS', True)


def main(source):
    control()
    values = rows(source)
    assert len(values) == 133 and not values[129]
    within, boundary = discover(source)
    assert (len(within), len(boundary)) == (25, 17)
    components = groups(source, values)
    cluster_id, row_offset, states = {}, {}, {}
    for root, entries in components.items():
        state, _ = close_group(entries, values)
        states[root] = state
        for row, offset in entries:
            cluster_id[row] = root
            row_offset[row] = offset

    earlier = [source_floor(r, cluster_id, row_offset, states, False) for r in range(132)]
    stronger = [source_floor(r, cluster_id, row_offset, states, True) for r in range(132)]
    changes = [(r, earlier[r], stronger[r]) for r in range(132) if stronger[r] > earlier[r]]
    weaker = [(r, earlier[r], stronger[r]) for r in range(132) if stronger[r] < earlier[r]]
    assert not weaker, weaker
    assert sum(g > 0 for g in earlier) == 46
    assert changes == [
        (10, 2, 3), (30, 1, 2), (41, 1, 2), (53, 2, 3),
        (63, 0, 1), (64, 2, 3), (82, 2, 3), (94, 3, 4),
        (113, 2, 3), (125, 0, 1), (126, 1, 2),
    ], changes
    old_window = interval(within, boundary, earlier)
    new_window = interval(within, boundary, stronger)
    assert old_window == (922, 971) and new_window == (924, 971)
    print('SOURCE_TARGET_ROW129_WITHHELD', True)
    print('SOURCE_POSITION_GAP_TESTS', '0..64')
    print('NEW_GF2_STRICT_GAP_FLOORS', changes)
    print('OLD_SOURCE_START_WINDOW', old_window)
    print('NEW_SOURCE_START_WINDOW', new_window)
    print('EXACT_K04_WORDS', 'UNDETERMINED')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: python agents/agent5/k04_full_gf2_gap_gate.py original-members.zip')
    main(Path(sys.argv[1]))
