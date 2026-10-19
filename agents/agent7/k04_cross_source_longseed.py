"""Source-conditioned long-seed MT19937 inversion for H-17 K04.
Run: python agents/agent7/k04_cross_source_longseed.py original-case.zip

Uses original spool, TRP2 and RC-17 source bytes; withholds spool row129
and reads neither K04/K08 commitments nor the recovery masks.
All conclusions assume one first-cycle CPython MT output stream, a
six-draw minimum for ordinary printer rows, and recorder/RC-17 ancestor
control words as exact 32-bit MT state words.
"""
from collections import Counter
from functools import lru_cache
from itertools import product
from pathlib import Path
import random
import sys

AGENTS = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(AGENTS / x) for x in ("agent7", "agent4", "agent8",
                                          "agent1", "agent6", "agent23")]
from k04_control_fullword_bridge import RelativePositions
from k04_cross_source_rc17_trp import source_hits
from k04_seed_stitch import bridge
from k04_python_seed_fragments import INITIAL, initial_words, seed_word
from k04_mt_rowstart import discover, untemper
from k04_mt_inverse_peel import groups
from k04_mt_ternary_class_gate import close_group, temper

MASK = 0xFFFFFFFF
ROWS = (3, 10, 13, 14, 28)
# Source-based pair group first positions relative to printer row0.
PREDECESSOR = {3: -1, 10: 0, 13: -1, 14: -1, 28: -1}
PAIR_COUNTS = {3: 5, 10: 4, 13: 5, 14: 4, 28: 4}
EXTRA_CONTROL = {10: "TRP[45]", 28: "RC17 RevB PURGE"}
LINKS = ((9, 40, 229), (7, 38, 230), (28, 59, 226))


def word_window(row, relative, count, states, positions, output_rows):
    root = positions.find(row)
    origin = positions.offset[row] + relative
    state = states[root]
    pairs = []
    for j in range(count):
        first = state[origin + j]
        second = state[origin + j + 227]
        assert first[0] == second[0] == MASK
        pairs.append((first[1], second[1]))
    return initial_words(pairs)


def exact_phase_constraints(source, positions):
    within, boundary = discover(source)
    assert (len(within), len(boundary)) == (25, 17)
    edges = []

    def equal(a, b, distance):
        edges.extend(((a, b, distance), (b, a, -distance)))

    for (a, j), (b, k), (c, l) in within:
        equal(a, b, 397 + j - k)
        equal(a, c, 624 + j - l)
    for a, bit, (b, k), (c, l) in boundary:
        equal(a, b, 396 - k)
        equal(a, c, 623 - l)
    for a, b, delta in LINKS:
        equal(a, b, delta)

    # Model-dependent class and destination sampler consume >=1 draw
    # each for ordinary printer row. Tail regime remains >=4 words.
    for row in range(132):
        edges.append((row + 1, row, -6 if row < 127 else -4))

    @lru_cache(None)
    def shortest(start, end):
        distances = [10**7] * 133
        distances[start] = 0
        for _ in range(133):
            changed = False
            for a, b, distance in edges:
                if distances[a] + distance < distances[b]:
                    distances[b] = distances[a] + distance
                    changed = True
            if not changed:
                break
        assert not any(distances[a] + distance < distances[b]
                       for a, b, distance in edges)
        return distances[end]

    starts = {}
    for row in ROWS:
        d = PREDECESSOR[row]
        low = -shortest(row, 0) + d
        high = shortest(0, row) + d
        starts[row] = range(low, high + 1)
    constraints = {(a, b): (-shortest(b, a) + PREDECESSOR[b] - PREDECESSOR[a],
                             shortest(a, b) + PREDECESSOR[b] - PREDECESSOR[a])
                   for a in (*ROWS, 11) for b in (*ROWS, 11) if a != b
                   if a != 11 and b != 11}
    # Pair phase row11 has zero predecessor, unlike row13's -1.
    mid_bound = (shortest, )
    return starts, constraints, shortest


def reconstruct(source):
    output_rows, hits = source_hits(source)
    assert not output_rows[129] and len(hits) == 9
    positions = RelativePositions(133)
    for root, entries in groups(source, output_rows).items():
        for row, position in entries:
            positions.equal(root, row, position)
    for a, b, delta in LINKS:
        positions.equal(a, b, delta)

    states = {}
    hidden = 0
    for root, entries in positions.clusters().items():
        state, increment = close_group(entries, output_rows)
        states[root] = state
        hidden += increment
    assert hidden == 77

    windows = {}
    sources = {name: data for name, data, crc, a, j, b, k in hits}
    for row in ROWS:
        words = word_window(row, PREDECESSOR[row], PAIR_COUNTS[row],
                            states, positions, output_rows)
        if row in EXTRA_CONTROL:
            prefix = EXTRA_CONTROL[row]
            match = [data for name, data in sources.items() if name.startswith(prefix)]
            assert len(match) == 1
            words.append(untemper(int.from_bytes(bytes.fromhex(match[0]), "little")))
        windows[row] = words
    windows[11] = word_window(11, 0, 3, states, positions, output_rows)
    assert [len(windows[r]) for r in ROWS] == [4, 4, 4, 3, 4]
    starts, bounds, shortest = exact_phase_constraints(source, positions)
    print("state_windows", {r: [f"{v:08X}" for v in windows[r]]
                            for r in ROWS})
    print("relative_pair_start_ranges", {r: [min(starts[r]), max(starts[r])]
                                         for r in ROWS})
    print("model_conditional_full_hidden_words", hidden + 4)
    return output_rows, windows, starts, shortest


def positive_controls():
    phases_by_size = {
        9: {3: 20, 10: 76, 13: 105, 14: 116, 28: 207},
        10: {3: 20, 10: 74, 13: 102, 14: 110, 28: 208},
        11: {3: 20, 10: 77, 13: 105, 14: 118, 28: 211},
    }
    for count, phases in phases_by_size.items():
        keys = [(0x1234AFFB + 0x86A119 * j) & MASK for j in range(count)]
        seed = sum(value << (32*j) for j, value in enumerate(keys))
        rng = random.Random(seed)
        initialized = rng.getstate()[1][:624]
        emitted = [untemper(rng.getrandbits(32)) for _ in range(624)]
        window = {}
        found = {}
        for row in ROWS:
            p = phases[row]
            n = PAIR_COUNTS[row]
            pairs = [(emitted[p+j], emitted[p+j+227]) for j in range(n)]
            recovered = initial_words(pairs)
            if row in EXTRA_CONTROL:
                recovered.append(initialized[p+231])
            assert recovered == list(initialized[p+228:p+228+len(recovered)])
            window[row] = recovered
            for j in range(2, len(recovered)):
                i = p + 228 + j
                k = (i-1) % count
                value = (seed_word(recovered[j-2:j+1], i) - k) & MASK
                assert keys[k] == value
                found[k] = value
        if len(found) < count:
            bridged = bridge(found, phases[13], phases[14],
                             window[13], window[14], count)
            assert bridged is not None
            found = bridged
        assert found == dict(enumerate(keys)), (count, found)
        print("synthetic_seed_recovered_bits", count * 32)


def scan(source):
    output_rows, windows, starts, shortest = reconstruct(source)
    assert output_rows[129] == []
    heldout = temper(output_rows[34][3])
    def pair_shift(row):
        return PREDECESSOR[row]

    constraints = {}
    for a in ROWS:
        for b in ROWS:
            if a < b:
                offset = pair_shift(b) - pair_shift(a)
                constraints[a,b] = (-shortest(b,a)+offset,
                                     shortest(a,b)+offset)

    feasible = []
    for phases in product(*(starts[row] for row in ROWS)):
        pos = dict(zip(ROWS, phases))
        if all(lo <= pos[b]-pos[a] <= hi
               for (a,b), (lo,hi) in constraints.items()):
            feasible.append(phases)
    assert len(feasible) == 2799
    print("relative_phase_tuples", len(feasible))

    @lru_cache(None)
    def fragments(row, phase, count):
        arr = windows[row]
        key = {}
        for j in range(2, len(arr)):
            i = phase+228+j
            k = (i-1) % count
            value = (seed_word(arr[j-2:j+1], i)-k) & MASK
            if k in key and key[k] != value:
                return None
            key[k] = value
        return key

    def heldout_match(keys, count, first_pair_phase):
        seed = sum(keys[k] << (32*k) for k in range(count))
        index = first_pair_phase + 232
        # CPython getrandbits(32*n) consumes n words and places the
        # last output in the highest 32 bits.
        predicted = random.Random(seed).getrandbits(32 * (index+1)) >> (32*index)
        return predicted == heldout

    total = {}
    for count in (9, 10, 11):
        stats = Counter()
        found = []
        for shift in range(186):
            for original in feasible:
                phases = {r: p+shift for r,p in zip(ROWS, original)}
                if phases[28]+231 >= 624:
                    continue
                stats["first_cycle_phase_assignments"] += 1
                pieces = {}
                for row in ROWS:
                    part = fragments(row, phases[row], count)
                    if part is None or any(k in pieces and pieces[k] != value
                                           for k, value in part.items()):
                        break
                    pieces.update(part)
                else:
                    stats["fragment_compatible"] += 1
                    candidates = []
                    if len(pieces) == count:
                        candidates.append(("direct", pieces))
                    elif count > 9:
                        stats["bridge_13_14_attempts"] += 1
                        extended = bridge(pieces, phases[13], phases[14],
                                          windows[13], windows[14], count)
                        if extended is not None and len(extended) == count:
                            candidates.append(("bridge_13_14", extended))
                        for p11 in range(max(82+shift, phases[10]+6),
                                         min(93+shift, phases[13]-6)):
                            gap10 = p11 - phases[10]
                            gap13 = phases[13] - p11
                            if not (-shortest(11,10) <= gap10 <= shortest(10,11)
                                    and -shortest(13,11)-1 <= gap13 <= shortest(11,13)-1):
                                continue
                            stats["bridge_10_11_attempts"] += 1
                            extended = bridge(pieces, phases[10], p11,
                                              windows[10], windows[11], count)
                            if extended is not None and len(extended) == count:
                                candidates.append(("bridge_10_11", extended))
                    for kind, candidate in candidates:
                        stats["completed_seed_"+kind] += 1
                        stats["completed_total"] += 1
                        if heldout_match(candidate, count, phases[3]):
                            found.append((shift, original, kind, candidate))
                        else:
                            stats["heldout_reject"] += 1
        assert stats["first_cycle_phase_assignments"] == 513553
        assert not found, "Source-consistent seed found: investigate before publication"
        print("seed_array_words", count, "statistics", dict(stats),
              "heldout_matches", len(found))
        total[count] = stats
    assert total[9]["completed_total"] == 2022
    assert total[10]["completed_total"] == 0
    assert total[11]["completed_total"] == 8935
    print("K04_K08_UNRESOLVED", True)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python k04_cross_source_longseed.py original-case.zip")
    positive_controls()
    scan(Path(sys.argv[1]))
