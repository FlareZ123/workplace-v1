"""Algebraic source-only test of standard MT19937 init_genrand (C/C++ 32-bit seed).

Usage: python agents/agent47/k04_initgenrand_gate.py ORIGINAL_CASE.zip
Selected row129 and all K04/K08 commitments are excluded.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "agent1"))
from k04_python_seed_fragments import extract_pairs, initial_words

MASK = 0xFFFFFFFF
TWIST_A = 0x9908B0DF
SEED_MULTIPLIER = 1812433253


def inferred_index(before, after):
    return (after - SEED_MULTIPLIER * (before ^ (before >> 30))) & MASK


def c_init_genrand(seed):
    result = [seed & MASK]
    for index in range(1, 624):
        result.append((SEED_MULTIPLIER * (result[-1] ^ (result[-1] >> 30)) + index) & MASK)
    return result


def twist_cycle(initial):
    # Standard 624-word in-place MT19937 twist, as in the reference C generator.
    state = initial[:]
    for k in range(624):
        y = (state[k] & 0x80000000) | (state[(k + 1) % 624] & 0x7FFFFFFF)
        state[k] = (state[(k + 397) % 624] ^ (y >> 1) ^
                    (TWIST_A if y & 1 else 0)) & MASK
    return state


def synthetic_controls():
    for seed in (1, 0x12345678, 0xFFFFFFFF):
        initial = c_init_genrand(seed)
        actual = twist_cycle(initial)
        for phase in (0, 30, 100, 395):
            pairs = [(actual[phase + j], actual[phase + 227 + j])
                     for j in range(5)]
            recovered = initial_words(pairs)
            assert recovered == initial[phase + 228: phase + 232]
            assert [inferred_index(a, b) for a, b in
                    zip(recovered, recovered[1:])] == list(range(phase + 229, phase + 232))
    print("reference_init_genrand_controls_PASS", 12)


def main(source):
    synthetic_controls()
    row3, row10, row13, row14 = extract_pairs(source)
    for row, pairs in ((3, row3), (10, row10), (13, row13), (14, row14)):
        recovered = initial_words(pairs)
        inferred = [inferred_index(a, b) for a, b in zip(recovered, recovered[1:])]
        print("source_row", row,
              "reconstructed_words", [f"{v:08X}" for v in recovered],
              "necessary_seeded_indices", inferred)
        assert inferred and all(not (1 <= v <= 623) for v in inferred)
    print("standard_first_cycle_32bit_init_genrand", "EXCLUDED")
    print("advanced_cycle_or_other_seeding", "UNTESTED")
    print("K04_K08", "UNRESOLVED")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python k04_initgenrand_gate.py ORIGINAL_CASE.zip")
    main(Path(sys.argv[1]))
