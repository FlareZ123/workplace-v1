"""Two-stage 288/320-bit CPython MT19937 numeric-seed bridge on original H17 spool.

Usage: python agents/agent8/k04_seed_dual_stitch.py original-case.zip
Reuses source-pinned 42 MT recurrence groups; omits source-selected row129
and never reads K04/K08 acceptance commitments or coupon mask.
"""
import collections
import random
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from k04_seed_stitch import (ALL, bridge, pair_group)
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "agent1"))
from k04_python_seed_fragments import compatible, extract_pairs, fragments
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "agent23"))
from k04_mt_rowstart import untemper
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "agent31"))
from k04_mt_recursive_peel import rows, temper


def synthetic_controls():
    cases = [
        (9, (14, 52, 58, 80, 91)),
        (10, (14, 51, 57, 76, 88)),
    ]
    for count, (pa, pc, p11, pb, pd) in cases:
        seed = sum(((0x34123412 + 0x345211 * j) & ALL) << (32*j)
                   for j in range(count))
        generator = random.Random(seed)
        state = [untemper(generator.getrandbits(32)) for _ in range(624)]
        def fake(phase, length):
            return [(state[phase+j], state[phase+j+227])
                    for j in range(length)]
        a, c, e, b, d = (fake(pa,5), fake(pc,4), fake(p11,3),
                         fake(pb,5), fake(pd,4))
        keys = {}
        for pairs, phase in ((a,pa),(c,pc),(b,pb),(d,pd)):
            keys = compatible(keys, fragments(pairs, phase, count))
            assert keys is not None
        first = bridge(keys, pc, p11, c, e, count)
        assert first is not None
        second = bridge(first, pb, pd, b, d, count)
        assert second is not None and len(second) == count
        reconstructed = sum(second[j] << (32*j) for j in range(count))
        assert reconstructed == seed
        print("synthetic_seed_recovery_PASS",count*32,(pa,pc,p11,pb,pd))


def main(source, count):
    a, c, b, d = extract_pairs(source)
    e = pair_group(source, 11, 3)
    source_values = rows(source)
    assert not source_values[129]
    heldout = temper(source_values[34][3])
    phase_sets = (
        (a,range(14,69)),(c,range(50,105)),
        (b,range(73,128)),(d,range(81,136))
    )
    lookups = [{p:fragments(pairs,p,count) for p in phases}
               for pairs,phases in phase_sets]
    stats = collections.Counter()
    started = time.monotonic()

    def check_seed(keys, pa):
        if len(keys) != count:
            return False
        seed = sum(keys[j] << (32*j) for j in range(count))
        phase = pa + 232  # row34 fourth payload word: outside all seed-window pairs
        predicted = random.Random(seed).getrandbits(32*(phase+1)) >> (32*phase)
        return predicted == heldout

    for pa,ka in lookups[0].items():
        for pb,kb in lookups[2].items():
            if not 59 <= pb-pa <= 113:
                continue
            ab = compatible(ka,kb)
            if ab is None:
                continue
            for pc,kc in lookups[1].items():
                if not (35 <= pc-pa-1 <= 89 and 24 <= pb+1-pc <= 78):
                    continue
                abc = compatible(ab,kc)
                if abc is None:
                    continue
                for pd,kd in lookups[3].items():
                    if not 8 <= pd-pb <= 18:
                        continue
                    keys = compatible(abc,kd)
                    if keys is None:
                        continue
                    stats["four_group_phase_compatible"] += 1
                    # Try 13->14 first once per source phase tuple.
                    reverse = bridge(keys,pb,pd,b,d,count)
                    for p11 in range(pc+4,min(pc+19,pb-6)):
                        stats["five_group_phase_tests"] += 1
                        first = bridge(keys,pc,p11,c,e,count)
                        if first is not None:
                            stats["row10_row11_bridge"] += 1
                            second = bridge(first,pb,pd,b,d,count)
                            if second is not None and len(second) == count:
                                stats["complete_forward_seed_assignments"] += 1
                                if check_seed(second,pa):
                                    stats["heldout_matches"] += 1
                                    print("HELDOUT_MATCH",count,pa,pc,p11,pb,pd,
                                          second,flush=True)
                        if reverse is not None:
                            last = bridge(reverse,pc,p11,c,e,count)
                            if last is not None and len(last) == count:
                                stats["complete_reverse_seed_assignments"] += 1
                                if check_seed(last,pa):
                                    stats["heldout_matches"] += 1
                                    print("REVERSE_HELDOUT_MATCH",count,pa,pc,p11,pb,pd,
                                          last,flush=True)
    print("selected_row129_withheld",True)
    print("integer_seed_bits",count*32)
    print("elapsed_seconds",round(time.monotonic()-started,2))
    print("counts",dict(stats))
    print("K04_K08_UNRESOLVED")


if __name__ == "__main__":
    if len(sys.argv)!=2:
        raise SystemExit("Usage: python agents/agent8/k04_seed_dual_stitch.py original-case.zip")
    synthetic_controls()
    main(Path(sys.argv[1]),9)
    main(Path(sys.argv[1]),10)
