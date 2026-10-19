"""Extend source-only H17 printer MT inverse seeds to 224/256-bit integers.

Usage: python agents/agent8/k04_seed_stitch.py original-case.zip
Requires agents 1, 23, 31 source-only reproducer modules on repository main.
Withholds selected row129. Never loads a REC8 commitment or mask.
"""
import collections
import random
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'agent1'))
from k04_python_seed_fragments import (ALL, INITIAL, compatible, extract_pairs,
                                       fragments, initial_words, seed_word,
                                       verify_seed)
sys.path.insert(0, str(ROOT / 'agent31'))
from k04_mt_recursive_peel import close_group, groups, rows, temper
sys.path.insert(0, str(ROOT / 'agent23'))
from k04_mt_rowstart import untemper

MODULUS = 1 << 32
INV_1664 = pow(1664525, -1, MODULUS)
INV_1566 = pow(1566083941, -1, MODULUS)


def multiplier(value, factor):
    return ((value ^ (value >> 30)) * factor) & ALL


def multiplier_inverse(value, inverse):
    word = (value * inverse) & ALL
    return word ^ (word >> 30)


def next_state(a, b, key, index, count):
    key_index = (index - 1) % count
    first = (b + index - 1) ^ multiplier(a, 1566083941)
    second = (INITIAL[index] ^ multiplier(first, 1664525)) + key + key_index
    return ((second & ALL) ^ multiplier(b, 1566083941)) - index & ALL


def previous_state(b, c, key, index, count):
    key_index = (index - 1) % count
    second = (c + index) ^ multiplier(b, 1566083941)
    first = multiplier_inverse(INITIAL[index] ^ ((second - key - key_index) & ALL), INV_1664)
    return multiplier_inverse(first ^ ((b + index - 1) & ALL), INV_1566)


def bridge(keys, left_phase, right_phase, left_pairs, right_pairs, count):
    """Recover one or two consecutive missing key-array words by two-way inversion.

    Returns a reconstructed key dictionary, or None if this bounded bridge
    cannot recover/verify an interval. None is not a model-wide refutation.
    """
    a_start, b_start = left_phase + 228, right_phase + 228
    a_words, b_words = initial_words(left_pairs), initial_words(right_pairs)
    a_end = a_start + len(a_words) - 1
    b_end = b_start + len(b_words) - 1
    if b_start <= a_end:
        return None
    left = {a_start + j: word for j, word in enumerate(a_words)}
    right = {b_start + j: word for j, word in enumerate(b_words)}
    missing = [i for i in range(a_end + 1, b_end + 1)
               if (i - 1) % count not in keys]
    if len(missing) > 2 or (len(missing) == 2 and missing[1] != missing[0] + 1):
        return None
    first = missing[0] if missing else b_end + 1
    last = missing[-1] if missing else b_end
    for i in range(a_end + 1, first):
        left[i] = next_state(left[i-2], left[i-1], keys[(i-1) % count], i, count)
        if i in right and left[i] != right[i]:
            return None
    if not missing:
        return dict(keys) if all(left.get(i) == v for i, v in right.items()) else None
    for i in range(b_end, last, -1):
        ki = (i - 1) % count
        if ki not in keys or i not in right or i-1 not in right:
            return None
        value = previous_state(right[i-1], right[i], keys[ki], i, count)
        if i-2 in right and right[i-2] != value:
            return None
        right[i-2] = value
    if any(i not in right for i in missing):
        return None
    if first-1 in right and first-1 in left and left[first-1] != right[first-1]:
        return None
    reconstructed = dict(keys)
    for i in missing:
        ki = (i - 1) % count
        value = (seed_word([left[i-2], left[i-1], right[i]], i) - ki) & ALL
        if ki in reconstructed and reconstructed[ki] != value:
            return None
        reconstructed[ki] = value
        left[i] = next_state(left[i-2], left[i-1], value, i, count)
        if left[i] != right[i]:
            return None
    for i in range(last + 1, b_end + 1):
        ki = (i - 1) % count
        if ki not in reconstructed:
            return None
        left[i] = next_state(left[i-2], left[i-1], reconstructed[ki], i, count)
        if i in right and left[i] != right[i]:
            return None
    return reconstructed


def pair_group(source, row, length):
    values = rows(source)
    entries = next(g for g in groups(source, values).values()
                   if any(r == row for r, _ in g))
    start = dict(entries)[row]
    state, _ = close_group(entries, values)
    assert all(state[start + j][0] == ALL and
               state[start + j + 227][0] == ALL for j in range(length))
    return [(state[start + j][1], state[start + j + 227][1])
            for j in range(length)]


def synthetic_controls():
    for count, phases in [(7, (14, 51, 74, 83)), (8, (14, 50, 75, 85))]:
        seed = sum(((0x12345112 + 0x77321 * j) & ALL) << (32*j)
                   for j in range(count))
        rng = random.Random(seed)
        state = [untemper(rng.getrandbits(32)) for _ in range(624)]
        samples = [[(state[p + j], state[p + j + 227]) for j in range(length)]
                   for p, length in zip(phases, (5, 4, 5, 4))]
        keys = {}
        for p, pairs in zip(phases, samples):
            keys = compatible(keys, fragments(pairs, p, count))
            assert keys is not None
        recovered = bridge(keys, phases[2], phases[3], samples[2], samples[3], count)
        assert recovered and len(recovered) == count
        assert seed == sum(recovered[j] << (32*j) for j in range(count))
        print('synthetic_recovered', count * 32, 'bits', 'PASS')


def scan(source, count):
    a, c, b, d = extract_pairs(source)
    row11 = pair_group(source, 11, 3)
    # Original row34 word3 at phase pa+232 was not used in seed fragments.
    # This source-only holdout is separate from all four pair-run inversions.
    holdout = temper(rows(source)[34][3])
    samples = [(a, range(14, 69)), (c, range(50, 105)),
               (b, range(73, 128)), (d, range(81, 136))]
    lookup = [{p: fragments(pairs, p, count) for p in phases}
              for pairs, phases in samples]
    stats = collections.Counter()
    started = time.monotonic()

    def check(candidate, first_phase):
        if len(candidate) != count:
            return False
        seed = sum(candidate[j] << (32*j) for j in range(count))
        # Predict genuinely held-out intact row34 final payload word.
        phase = first_phase + 232
        predicted = random.Random(seed).getrandbits(32*(phase+1)) >> (32*phase)
        if predicted != holdout:
            return False
        return verify_seed(seed, [(pa, a), (pc, c), (pb, b), (pd, d)])

    for pa, ka in lookup[0].items():
        for pb, kb in lookup[2].items():
            if not 59 <= pb - pa <= 113:
                continue
            ab = compatible(ka, kb)
            if ab is None:
                continue
            for pc, kc in lookup[1].items():
                if not (35 <= pc-pa-1 <= 89 and 24 <= pb+1-pc <= 78):
                    continue
                abc = compatible(ab, kc)
                if abc is None:
                    continue
                for pd, kd in lookup[3].items():
                    if not 8 <= pd-pb <= 62:
                        continue
                    keys = compatible(abc, kd)
                    if keys is None:
                        continue
                    stats['phase_compatible'] += 1
                    if pd-pb <= 18:
                        stats['bridge_13_14_attempts'] += 1
                        candidate = bridge(keys, pb, pd, b, d, count)
                        if candidate and len(candidate) == count:
                            stats['bridge_13_14_full_seeds'] += 1
                            assert not check(candidate, pa), 'first-cycle seed found'
                    # Original row11 first pair starts at the row11 stream index.
                    for p11 in range(pc + 4, min(pc + 19, pb - 6)):
                        stats['bridge_10_11_attempts'] += 1
                        candidate = bridge(keys, pc, p11, c, row11, count)
                        if candidate and len(candidate) == count:
                            stats['bridge_10_11_full_seeds'] += 1
                            assert not check(candidate, pa), 'first-cycle seed found'
    print('selected_row129_withheld', True)
    print('integer_seed_word_count', count, 'elapsed_seconds', round(time.monotonic()-started, 2))
    print('stats', dict(stats))
    print('complete_source_seed_matches', 0)
    print('K04_K08_UNRESOLVED')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('Usage: python agents/agent8/k04_seed_stitch.py original-case.zip')
    synthetic_controls()
    scan(Path(sys.argv[1]), 7)
    scan(Path(sys.argv[1]), 8)
