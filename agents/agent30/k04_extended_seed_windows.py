"""Source-only K04 conditional 96/128-bit first-cycle seed exclusion.

Run: python agents/agent30/k04_extended_seed_windows.py original-case.zip

Extends original row3 MT pairing to six consecutive 227-separated pairs,
using the independently predicted conditional row33->34 metadata bridge.
Withholds selected spool row129, original REC8 verifier, mask and commitments.
"""
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "agent31"))
from k04_mt_recursive_peel import rows, groups, close_group
sys.path.insert(0, str(ROOT / "agent1"))
from k04_python_seed_fragments import fragments, compatible, verify_seed
sys.path.insert(0, str(ROOT / "agent23"))
from k04_mt_rowstart import untemper

ALL = 0xFFFFFFFF


def source_pair_runs(source):
    values = rows(source)
    assert not values[129]
    clusters = list(groups(source, values).values())
    left = next(c for c in clusters if any(row == 33 for row, _ in c))
    right = next(c for c in clusters if any(row == 34 for row, _ in c))
    p33, p34 = dict(left)[33], dict(right)[34]
    shift = p33 + 6 - p34
    state, _ = close_group(left + [(r, p + shift) for r, p in right], values)

    start = p33 - 224
    first = []
    for j in range(6):
        assert state[start+j][0] == state[start+j+227][0] == ALL
        first.append((state[start+j][1], state[start+j+227][1]))
    assert first[1] == (0x482F6361, 0xA757A2AC)

    ten = next(c for c in clusters if any(row == 10 for row, _ in c))
    p10 = dict(ten)[10]
    old, _ = close_group(ten, values)
    second = []
    for j in range(4):
        assert old[p10+j][0] == old[p10+j+227][0] == ALL
        second.append((old[p10+j][1], old[p10+j+227][1]))
    return first, second


def synthetic_controls():
    for words in (3, 4):
        for p in (0, 125, 305, 350):
            q = p + 35
            seed = sum(((0xA1B2C3D4 + j * 0x13F123) & ALL) << (32*j)
                       for j in range(words))
            rng = random.Random(seed)
            state = [untemper(rng.getrandbits(32)) for _ in range(q+231)]
            first = [(state[p+j], state[p+j+227]) for j in range(6)]
            second = [(state[q+j], state[q+j+227]) for j in range(4)]
            a = fragments(first, p, words)
            b = fragments(second, q, words)
            recovered = compatible(a, b)
            assert recovered is not None and len(recovered) == words
            assert seed == sum(recovered[j] << (32*j) for j in range(words))
    print("synthetic_CPpython_random_96_128_seed_controls_PASS", 8)


def main(source):
    first, second = source_pair_runs(source)
    synthetic_controls()

    # Six source pairs have five reconstructed initialized-state words,
    # which algebraically determine all three words of a 96-bit seed.
    count96 = 0
    for p in range(392):
        key = fragments(first, p, 3)
        assert key is not None and len(key) == 3
        seed = sum(key[j] << (32*j) for j in range(3))
        count96 += int(verify_seed(seed, [(p, first)]))
    assert count96 == 0

    # First six-pair window: p+232 <= 623. Row10 four-pair window:
    # q+230 <= 623. Source-only 42-witness constraints give 35<=q-p<=90.
    complete128 = matching128 = 0
    for p in range(392):
        a = fragments(first, p, 4)
        for q in range(p + 35, min(p + 91, 394)):
            b = fragments(second, q, 4)
            key = compatible(a, b)
            if key is None or len(key) != 4:
                continue
            complete128 += 1
            seed = sum(key[j] << (32*j) for j in range(4))
            matching128 += int(verify_seed(seed, [(p, first), (q, second)]))
    assert (complete128, matching128) == (4662, 0)

    print("selected_row129_withheld", True)
    print("96bit_all_first_cycle_row3_phases", 392, "exact_source_matches", count96)
    print("128bit_completed_two_window_phase_assignments", complete128,
          "exact_source_matches", matching128)
    print("later_cycle_and_other_seed_classes_NOT_EXCLUDED")
    print("original_K04_K08_UNRESOLVED")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python k04_extended_seed_windows.py original-case.zip")
    main(Path(sys.argv[1]))
