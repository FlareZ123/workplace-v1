"""Invert first-cycle CPython MT19937 integer seed fragments from H17 spool.
Run: python agents/agent1/k04_python_seed_fragments.py original-case.zip
Selected row129 and all REC8 commitments are excluded. Requires existing
Agent 31/23 source-pinned, fixed-point inverse MT recurrence utilities.
"""
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "agent31"))
from k04_mt_recursive_peel import rows, groups, close_group, temper

ALL = 0xFFFFFFFF


def inverse_twist(value):
    parity = value >> 31
    word = (((value ^ (0x9908B0DF if parity else 0)) << 1) | parity) & ALL
    return word & 0x80000000, word & 0x7FFFFFFF


def initial_words(pairs):
    halves = [inverse_twist(a ^ b) for a, b in pairs]
    return [halves[i][1] | halves[i + 1][0] for i in range(len(halves) - 1)]


def initialization_constants():
    result = [19650218]
    for i in range(1, 624):
        result.append((1812433253 * (result[-1] ^ (result[-1] >> 30)) + i) & ALL)
    return result


INITIAL = initialization_constants()


def seed_word(state, index):
    a, b, c = state
    jprevious = ((b + index - 1) ^ ((a ^ (a >> 30)) * 1566083941)) & ALL
    jcurrent = ((c + index) ^ ((b ^ (b >> 30)) * 1566083941)) & ALL
    return (jcurrent - (INITIAL[index] ^ ((jprevious ^ (jprevious >> 30)) * 1664525))) & ALL


def fragments(pairs, first_position, num_words):
    reconstructed = initial_words(pairs)
    key = {}
    for j in range(2, len(reconstructed)):
        index = first_position + 228 + j
        if index >= 624:
            return None
        key_index = (index - 1) % num_words
        value = (seed_word(reconstructed[j - 2:j + 1], index) - key_index) & ALL
        if key_index in key and key[key_index] != value:
            return None
        key[key_index] = value
    return key


def compatible(left, right):
    if left is None or right is None:
        return None
    if any(i in left and left[i] != v for i, v in right.items()):
        return None
    return {**left, **right}


def verify_seed(seed, samples):
    count = max(first + len(pairs) + 227 for first, pairs in samples)
    rng = random.Random(seed)
    state = [rng.getrandbits(32) for _ in range(count)]
    return all(state[first + j] == temper(a) and
               state[first + j + 227] == temper(b)
               for first, pairs in samples for j, (a, b) in enumerate(pairs))


def run_scan(sets, num_words):
    # 42 unwithheld MT witnesses establish s3-s0=15..69, s10=50..104,
    # s13=74..128 and s14=82..136, plus ordered row-difference bounds.
    # The first pair starts one draw before rows 3,13,14 and at row10.
    a, c, b, d = sets
    af = {p: fragments(a, p, num_words) for p in range(14, 69)}
    cf = {p: fragments(c, p, num_words) for p in range(50, 105)}
    bf = {p: fragments(b, p, num_words) for p in range(73, 128)}
    df = {p: fragments(d, p, num_words) for p in range(81, 136)}
    counts = dict(ab=0, abc=0, abcd=0, complete=0, accepted=0)
    candidates = []
    for pa, fa in af.items():
        for pb, fb in bf.items():
            if not 59 <= pb - pa <= 113:
                continue
            ab = compatible(fa, fb)
            if ab is None:
                continue
            counts["ab"] += 1
            if num_words <= 4:
                if len(ab) == num_words:
                    counts["complete"] += 1
                    seed = sum(ab[i] << (32 * i) for i in range(num_words))
                    if verify_seed(seed, [(pa, a), (pb, b)]):
                        counts["accepted"] += 1
                        candidates.append((pa, pb, seed))
                continue
            for pc, fc in cf.items():
                if not (35 <= pc - pa - 1 <= 89 and
                        24 <= pb + 1 - pc <= 78):
                    continue
                abc = compatible(ab, fc)
                if abc is None:
                    continue
                counts["abc"] += 1
                for pd, fd in df.items():
                    if not 8 <= pd - pb <= 62:
                        continue
                    combined = compatible(abc, fd)
                    if combined is None:
                        continue
                    counts["abcd"] += 1
                    if len(combined) != num_words:
                        continue
                    counts["complete"] += 1
                    seed = sum(combined[i] << (32 * i) for i in range(num_words))
                    if verify_seed(seed, [(pa, a), (pb, b), (pc, c), (pd, d)]):
                        counts["accepted"] += 1
                        candidates.append((pa, pc, pb, pd, seed))
    return counts, candidates


def extract_pairs(source):
    values = rows(source)
    assert len(values) == 133 and not values[129]
    source_groups = groups(source, values)
    result = {}
    for row, relative_first, count in [(3, -1, 5), (10, 0, 4),
                                       (13, -1, 5), (14, -1, 4)]:
        entries = next(e for e in source_groups.values()
                       if any(r == row for r, _ in e))
        positions = dict(entries)
        start = positions[row] + relative_first
        state, _ = close_group(entries, values)
        assert all(state[start + j][0] == ALL and
                   state[start + j + 227][0] == ALL for j in range(count))
        result[row] = [(state[start + j][1], state[start + j + 227][1])
                       for j in range(count)]
    assert result[3][0] == (0x482F6361, 0xA757A2AC)
    assert result[13][0] == (0x8F878FB0, 0x0ACF4761)
    return result[3], result[10], result[13], result[14]


def synthetic_controls():
    cases = [
        (1, 0xA1234567, (32, 76, 104, 115)),
        (2, 0xAB123456ABCDEF12, (32, 76, 104, 115)),
        (3, 0x1ABACADCBABACDB123, (32, 76, 104, 115)),
        (4, 0xFEDCBA9876543210DEADBEEF12345678, (32, 78, 106, 115)),
        (5, int.from_bytes(bytes(range(20)), "little") | (1 << 159),
         (32, 76, 104, 115)),
        (6, int.from_bytes(bytes(range(24)), "little") | (1 << 191),
         (32, 78, 106, 115)),
    ]
    def untemper(y):
        x = y
        for shift, mask, left in [(18, ALL, False),
                                  (15, 0xEFC60000, True),
                                  (7, 0x9D2C5680, True),
                                  (11, ALL, False)]:
            initial = x
            for _ in range(6):
                x = initial ^ (((x << shift) & mask) if left else x >> shift)
            x &= ALL
        return x
    for n, seed, (pa, pc, pb, pd) in cases:
        rng = random.Random(seed)
        state = [untemper(rng.getrandbits(32)) for _ in range(624)]
        data = [[(state[p + j], state[p + j + 227]) for j in range(m)]
                for p, m in [(pa, 5), (pc, 4), (pb, 5), (pd, 4)]]
        merged = {}
        for (phase, pairs) in zip((pa, pc, pb, pd), data):
            merged = compatible(merged, fragments(pairs, phase, n))
            assert merged is not None
        if len(merged) == n:
            candidate = sum(merged[i] << (32 * i) for i in range(n))
            assert candidate == seed
            assert verify_seed(seed, list(zip((pa, pc, pb, pd), data)))
    print("synthetic_controls_PASS", len(cases))


def main(source):
    synthetic_controls()
    sets = extract_pairs(source)
    print("selected_row129_withheld", True)
    for n in range(1, 7):
        counts, candidates = run_scan(sets, n)
        print("integer_seed_32bit_chunks", n, "counts", counts,
              "matching_seeds", candidates[:10])
        assert not candidates
    print("six_short_integer_seed_classes_NO_MATCH")
    print("longer_or_later_cycle_seed_models_UNTESTED")
    print("K04_K08_UNRESOLVED")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python agents/agent1/k04_python_seed_fragments.py original-case.zip")
    main(Path(sys.argv[1]))
