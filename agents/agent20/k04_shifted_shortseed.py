"""Shifted-origin short-seed inversion of original H17 printer MT state.

Use: python agents/agent20/k04_shifted_shortseed.py original-case.zip
Source row129, K04 mask and commitments are never loaded.
Hypothesis: shared recorder+printer MT stream, source phase of original row3
first 227-separated pair in 321..392 (the only first-cycle source window).
Tests CPython random.Random(int) 32-/64-bit initialization, with synthetic
positive recovery at both the boundary and the latest allowed phase.
"""
import random
import sys
from pathlib import Path

if len(sys.argv) != 2:
    raise SystemExit("usage: python k04_shifted_shortseed.py original-case.zip")
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "agent1"))
sys.path.insert(0, str(ROOT / "agent23"))
from k04_python_seed_fragments import extract_pairs, fragments, verify_seed
from k04_mt_rowstart import untemper


def synthetic(seed, phase):
    r = random.Random(seed)
    source = [untemper(r.getrandbits(32)) for _ in range(phase + 232)]
    return [(source[phase + i], source[phase + i + 227]) for i in range(5)]


for count, seed, phase in [(1, 0xB2CCDD98, 321), (2, 0x123456789ABCDEF0, 392)]:
    pairs = synthetic(seed, phase)
    recovered = fragments(pairs, phase, count)
    assert recovered is not None and len(recovered) == count
    assert sum(recovered[i] << (32 * i) for i in range(count)) == seed
    assert verify_seed(seed, [(phase, pairs)])
    print("synthetic_phase", phase, "seed_bits", count * 32, "PASS")

original_row3 = extract_pairs(Path(sys.argv[1]))[0]
assert original_row3[0] == (0x482F6361, 0xA757A2AC)

for count in (1, 2):
    fragment_survivors = 0
    source_matches = []
    for phase in range(321, 393):
        recovered = fragments(original_row3, phase, count)
        if recovered is None or len(recovered) != count:
            continue
        fragment_survivors += 1
        seed = sum(recovered[i] << (32 * i) for i in range(count))
        if verify_seed(seed, [(phase, original_row3)]):
            source_matches.append((phase, seed))
    print("model", "CPython_firstcycle_integer", "seed_bits", count * 32,
          "phases_tested", 72, "algebraic_fragment_survivors", fragment_survivors,
          "complete_source_seed_matches", source_matches)

print("selected_row129_withheld", True)
print("no_K04_or_K08_verification_attempted", True)
