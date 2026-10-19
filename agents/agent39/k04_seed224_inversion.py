"""K04 source-conditioned seven-word CPython integer-seed inversion.

Usage: python agents/agent39/k04_seed224_inversion.py original-case.zip
Selected printer row129 is omitted before inference; acceptance commitments,
K04 mask, and K08 inputs are never opened.

The tested family is a first-output-cycle CPython MT19937 seeded by an
unsigned 224-bit Python int, with row0 at stream position zero and at least
two nonpayload RNG draws between ordinary printer records. The three
independently discovered recorder/RC17 MT bridges are conditional equalities.
"""
import random
import sys
from pathlib import Path

agents = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(agents / "agent1"), str(agents / "agent31"),
               str(agents / "agent23")]

from k04_python_seed_fragments import fragments, compatible, verify_seed
from k04_mt_recursive_peel import rows, groups, close_group
from k04_mt_rowstart import discover, untemper

BRIDGES = ((9, 40, 229), (7, 38, 230), (28, 59, 226))
# Exact original source fields. The last four-pair run is newly available
# after joining printer groups 28 and 59 via the two RC-17 control strips.
SOURCE_RUNS = ((3, -1, 5), (13, -1, 5), (10, 0, 4),
               (14, -1, 4), (28, -1, 4))
SEED_WORDS = 7


def source_runs(path):
    original = rows(path)
    assert len(original) == 133 and not original[129]
    base = list(groups(path, original).values())

    def containing(row):
        return next(entries for entries in base
                    if any(r == row for r, _ in entries))

    left, right = containing(28), containing(59)
    assert left is not right
    shift = dict(left)[28] + 226 - dict(right)[59]
    merged = left + [(r, p + shift) for r, p in right]

    runs = {}
    for row, shift_from_start, n in SOURCE_RUNS:
        entries = merged if row == 28 else containing(row)
        state, _ = close_group(entries, original)
        start = dict(entries)[row] + shift_from_start
        assert all(state[start + j][0] == 0xFFFFFFFF and
                   state[start + j + 227][0] == 0xFFFFFFFF
                   for j in range(n))
        runs[row] = [(state[start + j][1], state[start + j + 227][1])
                     for j in range(n)]
    assert runs[3][0] == (0x482F6361, 0xA757A2AC)
    assert runs[13][0] == (0x8F878FB0, 0x0ACF4761)
    return runs


def phase_graph(path):
    within, boundary = discover(path)
    assert (len(within), len(boundary)) == (25, 17)
    edges = []

    def equal(a, b, distance):
        edges.extend(((a, b, distance), (b, a, -distance)))

    for (a, j), (b, k), (c, ell) in within:
        equal(a, b, 397 + j - k)
        equal(a, c, 624 + j - ell)
    for a, bit, (b, k), (c, ell) in boundary:
        equal(a, b, 396 - k)
        equal(a, c, 623 - ell)
    for a, b, distance in BRIDGES:
        equal(a, b, distance)
    for row in range(132):
        edges.append((row + 1, row, -(6 if row < 127 else 4)))

    def shortest(start):
        dist = [float("inf")] * 133
        dist[start] = 0
        for _ in range(132):
            changed = False
            for a, b, weight in edges:
                if dist[a] + weight < dist[b]:
                    dist[b] = dist[a] + weight
                    changed = True
            if not changed:
                break
        assert all(dist[a] + w >= dist[b] for a, b, w in edges)
        return dist

    required = [0] + [r for r, _, _ in SOURCE_RUNS]
    return {r: shortest(r) for r in required}


def synthetic_control():
    seed = int.from_bytes(bytes(range(28)), "little") | (1 << 223)
    phases = {3: 21, 13: 107, 10: 74, 14: 116, 28: 209}
    rng = random.Random(seed)
    words = [untemper(rng.getrandbits(32)) for _ in range(500)]
    combined = {}
    samples = []
    for row, shift, count in SOURCE_RUNS:
        start = phases[row] + shift
        pairs = [(words[start + j], words[start + j + 227])
                 for j in range(count)]
        fragment = fragments(pairs, start, SEED_WORDS)
        combined = compatible(combined, fragment)
        assert combined is not None
        samples.append((start, pairs))
    assert len(combined) == SEED_WORDS
    recovered = sum(combined[i] << (32 * i) for i in range(SEED_WORDS))
    assert recovered == seed and verify_seed(recovered, samples)
    print("synthetic_224bit_exact_recovery", "PASS")


def main(path):
    synthetic_control()
    runs = source_runs(path)
    distances = phase_graph(path)

    choices = []
    for row, shift, count in SOURCE_RUNS:
        lo, hi = -distances[row][0], distances[0][row]
        options = [(phase, fragments(runs[row], phase + shift, SEED_WORDS))
                   for phase in range(lo, hi + 1)]
        options = [(phase, f) for phase, f in options if f is not None]
        choices.append((row, options))
        print("row", row, "allowed_first_cycle_phase", (lo, hi),
              "fragment_options", len(options))

    counts = {"compatible_full_assignments": 0,
              "complete_seven_word_seeds": 0,
              "original_source_matches": 0}
    accepted = []

    def search(i, phases, fragments_so_far):
        if i == len(choices):
            counts["compatible_full_assignments"] += 1
            if len(fragments_so_far) != SEED_WORDS:
                return
            counts["complete_seven_word_seeds"] += 1
            seed = sum(fragments_so_far[j] << (32 * j)
                       for j in range(SEED_WORDS))
            samples = [(phases[row] + shift, runs[row])
                       for row, shift, count in SOURCE_RUNS]
            if verify_seed(seed, samples):
                counts["original_source_matches"] += 1
                accepted.append((dict(phases), seed))
            return
        row, options = choices[i]
        for phase, fragment in options:
            if any(not (-distances[other][row] <= phase - other_phase
                        <= distances[row][other])
                   for other, other_phase in phases.items()):
                continue
            merged = compatible(fragments_so_far, fragment)
            if merged is not None:
                search(i + 1, {**phases, row: phase}, merged)

    search(0, {}, {})
    assert counts == {"compatible_full_assignments": 18,
                      "complete_seven_word_seeds": 18,
                      "original_source_matches": 0}, counts
    assert accepted == []
    print("counts", counts)
    print("selected_row129_withheld", True)
    print("first_cycle_CP_uint224_with_model_constraints", "NO_MATCH")
    print("other_seed_types_and_K04_K08", "UNRESOLVED")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python agents/agent39/k04_seed224_inversion.py original-case.zip")
    main(Path(sys.argv[1]))
