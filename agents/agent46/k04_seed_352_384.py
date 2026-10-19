"""New H17 K04 source-window attack: 352/384-bit CPython integer seeds.

Requires the existing 42 printer-only witness and dual-window seed-inversion
modules. Withholds spool row129 and all acceptance commitments. Source-only
held-out word34/3 is checked by Agent8's main() before any hypothesis advances.

Usage: python agents/agent46/k04_seed_352_384.py original-source.zip
"""
from pathlib import Path
import sys
import random

HERE = Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent / "agent8"))
from k04_seed_dual_stitch import main
from k04_seed_stitch import bridge
sys.path.insert(0,str(HERE.parent / "agent1"))
from k04_python_seed_fragments import compatible, fragments, ALL
sys.path.insert(0,str(HERE.parent / "agent23"))
from k04_mt_rowstart import untemper

def synthetic_control(count):
    """Find a phase tuple where the two-bridge 352/384-bit grammar is identifiable."""
    seed = sum(((0x34123412 + 0x345211*j) & ALL) << (32*j) for j in range(count))
    rng = random.Random(seed)
    state = [untemper(rng.getrandbits(32)) for _ in range(624)]
    def fake(phase,length):
        return [(state[phase+j],state[phase+j+227]) for j in range(length)]
    pa=14
    a=fake(pa,5)
    ka=fragments(a,pa,count)
    for pc in range(50,67):
        c=fake(pc,4)
        kac=compatible(ka,fragments(c,pc,count))
        if kac is None: continue
        for pb in range(73,100):
            if not 59 <= pb-pa <= 113: continue
            b=fake(pb,5)
            kacb=compatible(kac,fragments(b,pb,count))
            if kacb is None: continue
            for pd in range(pb+8,min(pb+19,136)):
                d=fake(pd,4)
                keys=compatible(kacb,fragments(d,pd,count))
                if keys is None: continue
                for p11 in range(pc+4,min(pc+19,pb-6)):
                    e=fake(p11,3)
                    first=bridge(keys,pc,p11,c,e,count)
                    if first is None: continue
                    final=bridge(first,pb,pd,b,d,count)
                    if final is not None and len(final)==count:
                        rebuilt=sum(final[j] << (32*j) for j in range(count))
                        assert rebuilt==seed
                        print("SYNTHETIC_PASS",count*32, (pa,pc,p11,pb,pd),flush=True)
                        return True
    print("SYNTHETIC_NO_FULL_COVERAGE",count*32,"two-bridge tested-phase family",flush=True)
    return False

if __name__=="__main__":
    if len(sys.argv)!=2:raise SystemExit("Usage: python k04_seed_352_384.py source.zip")
    source=Path(sys.argv[1])
    for count in (11,12):
        covered=synthetic_control(count)
        print("TESTING_ORIGINAL",count*32,"synthetic_calibration",covered,flush=True)
        main(source,count)
