"""Exhaust all first-cycle phases for 32-/64-bit CPython MT seeds.
Run: python agents/agent38/k04_firstcycle_shortseed_fullphase.py ORIGINAL.zip
The printer's disputed row129 and every acceptance value remain withheld.
"""
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "agent1"))
sys.path.insert(0, str(ROOT / "agent23"))
from k04_python_seed_fragments import extract_pairs, fragments, verify_seed
from k04_mt_rowstart import untemper

def synthetic_controls():
    for n in (1, 2):
        seed = 0xB4DC31B9 if n == 1 else 0xB4DC31B9928371AF
        phase = 336
        rng = random.Random(seed)
        out = [untemper(rng.getrandbits(32)) for _ in range(624)]
        pairs = [(out[phase+j], out[phase+j+227]) for j in range(5)]
        recovered = fragments(pairs, phase, n)
        assert recovered is not None and len(recovered) == n
        recovered_seed = sum(recovered[j] << (32*j) for j in range(n))
        assert recovered_seed == seed
        assert verify_seed(recovered_seed, phase, pairs)

def main(source):
    synthetic_controls()
    row3, _, _, _ = extract_pairs(source)
    assert len(row3) == 5
    complete = {1: 0, 2: 0}
    matches = []
    for n in (1, 2):
        for phase in range(393):
            reconstructed = fragments(row3, phase, n)
            if reconstructed is None or len(reconstructed) != n:
                continue
            complete[n] += 1
            candidate = sum(reconstructed[j] << (32*j) for j in range(n))
            if verify_seed(candidate, phase, row3):
                matches.append((n, phase, candidate))
    assert complete == {1: 0, 2: 393}
    assert not matches
    print("synthetic_late_phase_controls_PASS", True)
    print("first_cycle_phase_range", "0..392")
    print("complete_candidates_32bit", complete[1])
    print("complete_candidates_64bit", complete[2])
    print("original_source_matching_candidates", matches)
    print("longer_seeds_and_cycle_crossing_UNTESTED", True)
    print("K04_K08_UNRESOLVED", True)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python k04_firstcycle_shortseed_fullphase.py ORIGINAL.zip")
    main(Path(sys.argv[1]))
