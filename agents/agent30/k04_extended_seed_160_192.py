"""K04: conditional six-pair row3 stream attack on 160/192-bit numeric seeds.

Run: python agents/agent30/k04_extended_seed_160_192.py original-case.zip

Uses source-only 42 MT witnesses and the row33->34 two-metadata-draw
bridge. Target row129, coupon mask and REC8 commitments are withheld.
"""
import collections
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "agent30"))
from k04_extended_seed_windows import source_pair_runs
sys.path.insert(0, str(ROOT / "agent8"))
from k04_seed_stitch import bridge, pair_group
sys.path.insert(0, str(ROOT / "agent1"))
from k04_python_seed_fragments import fragments, compatible
sys.path.insert(0, str(ROOT / "agent23"))
from k04_mt_rowstart import untemper
sys.path.insert(0, str(ROOT / "agent31"))
from k04_mt_recursive_peel import rows, temper

ALL = 0xFFFFFFFF


def synthetic_controls():
    for n in (5, 6):
        for p in (0, 125, 305):
            q = p + 35
            third = q + (7 if n == 5 else 6)
            seed = sum(((0x88776655 + j * 0x6124329) & ALL) << (32*j)
                       for j in range(n))
            rng = random.Random(seed)
            original = [untemper(rng.getrandbits(32))
                        for _ in range(third+230)]
            a = [(original[p+j], original[p+j+227]) for j in range(6)]
            b = [(original[q+j], original[q+j+227]) for j in range(4)]
            c = [(original[third+j], original[third+j+227])
                 for j in range(3)]
            keys = compatible(fragments(a,p,n), fragments(b,q,n))
            assert keys is not None
            recovered = bridge(keys,q,third,b,c,n)
            assert recovered is not None and len(recovered)==n
            assert seed == sum(recovered[j] << (32*j) for j in range(n))
    print("synthetic_160_192bit_CPpython_seed_recovery_PASS",6)


def main(source):
    synthetic_controls()
    first, second = source_pair_runs(source)
    third = pair_group(source,11,3)
    known = rows(source)
    assert not known[129]
    # Original row34 fourth output is outside the 6+4+3 paired windows.
    heldout = temper(known[34][3])

    for count in (5, 6):
        stats = collections.Counter()
        for p in range(392):
            a = fragments(first,p,count)
            for q in range(p+35,min(p+91,394)):
                b = fragments(second,q,count)
                keys = compatible(a,b)
                if keys is None or len(keys)!=4:
                    continue
                stats["source_phase_pair_compatible"] += 1
                for third_phase in range(q+4,min(q+19,395)):
                    stats["bridge_attempts"] += 1
                    completed = bridge(keys,q,third_phase,second,third,count)
                    if completed is None or len(completed)!=count:
                        continue
                    stats["complete_numeric_seeds"] += 1
                    seed = sum(completed[j] << (32*j)
                               for j in range(count))
                    predicted = random.Random(seed).getrandbits(32*(p+234)) >> (32*(p+233))
                    if predicted==heldout:
                        stats["source_heldout_matches"] += 1
                        print("HOLDOUT_MATCH",count,p,q,third_phase,seed,flush=True)
        expected = (
            {"source_phase_pair_compatible":7271,"bridge_attempts":105765}
            if count == 5 else
            {"source_phase_pair_compatible":9269,"bridge_attempts":134835,
             "complete_numeric_seeds":28004}
        )
        assert all(stats[k]==v for k,v in expected.items()),stats
        assert stats["source_heldout_matches"]==0,stats
        print("numeric_seed_words",count,"counts",dict(stats))
    print("selected_row129_withheld",True)
    print("later_cycle_and_other_seed_classes_UNTESTED")
    print("original_K04_K08_UNRESOLVED")


if __name__=="__main__":
    if len(sys.argv)!=2:
        raise SystemExit("usage: python k04_extended_seed_160_192.py original-case.zip")
    main(Path(sys.argv[1]))
