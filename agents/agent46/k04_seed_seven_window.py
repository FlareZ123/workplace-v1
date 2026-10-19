"""K04 seven-window 384-bit numeric-seed crack: recover final repeated key word.

The sixth source window is row28/59 RC17; the seventh is row7/38 TRP2.
Three distinct two-sided inverse-init_by_array bridges are attempted.
The original selected spool row129 and all acceptance commitments are omitted.
"""
import collections
import random
import sys
import time
from pathlib import Path

AGENTS=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(AGENTS/"agent1"),str(AGENTS/"agent8"),
             str(AGENTS/"agent23"),str(AGENTS/"agent31"),
             str(Path(__file__).resolve().parent)]
from k04_python_seed_fragments import compatible,extract_pairs,fragments,ALL
from k04_seed_stitch import bridge,pair_group
from k04_mt_rowstart import untemper
from k04_mt_recursive_peel import close_group,rows,temper
from k04_cross_carrier_seed_windows import indexed_groups

COUNT=12

def extra_pairs(source):
    words,clusters=indexed_groups(source,True)
    result={}
    for row,offset,length in ((7,1,3),(28,-1,4)):
        entries=next(e for e in clusters.values() if any(r==row for r,_ in e))
        start=dict(entries)[row]+offset
        state,_=close_group(entries,words)
        assert all(state[start+j][0]==ALL and state[start+j+227][0]==ALL
                   for j in range(length))
        result[row]=[(state[start+j][1],state[start+j+227][1]) for j in range(length)]
    return result[7],result[28]

def stages(a,c,e,b,d,g,f,pa,pc,p11,pb,pd,p7,p28):
    keys={}
    for phase,pairs in ((pa,a),(pc,c),(pb,b),(pd,d)):
        keys=compatible(keys,fragments(pairs,phase,COUNT))
        if keys is None:return None
    first=bridge(keys,pc,p11,c,e,COUNT)
    if first is None:return None
    second=bridge(first,pb,pd,b,d,COUNT)
    if second is None:return None
    sixth=compatible(second,fragments(f,p28,COUNT))
    if sixth is None:return None
    third=bridge(sixth,p7,pc,g,c,COUNT)
    return third if third is not None and len(third)==COUNT else None

def synthetic():
    seed=sum(((0x34123412+0x345211*j)&ALL)<<(32*j) for j in range(COUNT))
    rng=random.Random(seed)
    state=[untemper(rng.getrandbits(32)) for _ in range(624)]
    def fake(phase,length):
        return [(state[phase+j],state[phase+j+227]) for j in range(length)]
    pa=14;a=fake(pa,5)
    for pc in range(57,87):
        c=fake(pc,4)
        for pb in range(max(73,pc+25),min(128,pc+75)):
            b=fake(pb,5)
            for pd in range(pb+8,min(pb+19,136)):
                d=fake(pd,4)
                keys={}
                for phase,pairs in ((pa,a),(pc,c),(pb,b),(pd,d)):
                    keys=compatible(keys,fragments(pairs,phase,COUNT))
                    if keys is None:break
                if keys is None:continue
                for p11 in range(pc+4,min(pc+19,pb-6)):
                    e=fake(p11,3)
                    first=bridge(keys,pc,p11,c,e,COUNT)
                    if first is None:continue
                    second=bridge(first,pb,pd,b,d,COUNT)
                    if second is None or len(second)!=10:continue
                    missing=set(range(COUNT))-set(second)
                    for p28 in range(pd+84,394):
                        if (p28+229)%COUNT not in missing:continue
                        sixth=compatible(second,fragments(fake(p28,4),p28,COUNT))
                        if sixth is None or len(sixth)!=11:continue
                        for p7 in range(pa+26,pc-16):
                            recovered=bridge(sixth,p7,pc,fake(p7,3),c,COUNT)
                            if recovered is None or len(recovered)!=COUNT:continue
                            reconstructed=sum(recovered[j]<<(32*j) for j in range(COUNT))
                            assert reconstructed==seed
                            print("SYNTHETIC_SEVEN_WINDOW_PASS",
                                  (pa,pc,p7,p11,pb,pd,p28),flush=True)
                            return True
    print("SYNTHETIC_SEVEN_WINDOW_NOT_COVERED",flush=True)
    return False

def main(source):
    a,c,b,d=extract_pairs(source)
    e=pair_group(source,11,3)
    g,f=extra_pairs(source)
    original=rows(source)
    assert not original[129]
    heldout=temper(original[34][3])
    ranges=((a,range(14,69)),(c,range(50,105)),
            (b,range(73,128)),(d,range(81,136)))
    lookup=[{p:fragments(pair,p,COUNT) for p in phase} for pair,phase in ranges]
    last={p:fragments(f,p,COUNT) for p in range(180,394)}
    stats=collections.Counter()
    begun=time.monotonic()
    for pa,ka in lookup[0].items():
        for pb,kb in lookup[2].items():
            if not 59<=pb-pa<=113:continue
            ab=compatible(ka,kb)
            if ab is None:continue
            for pc,kc in lookup[1].items():
                if not(35<=pc-pa-1<=89 and 24<=pb+1-pc<=78):continue
                abc=compatible(ab,kc)
                if abc is None:continue
                # source-backed two-selector floor: row3->7->10
                if pc-pa<43:continue
                for pd,kd in lookup[3].items():
                    if not 8<=pd-pb<=18:continue
                    keys=compatible(abc,kd)
                    if keys is None:continue
                    for p11 in range(pc+4,min(pc+19,pb-6)):
                        first=bridge(keys,pc,p11,c,e,COUNT)
                        if first is None:continue
                        stats["first_bridge"]+=1
                        second=bridge(first,pb,pd,b,d,COUNT)
                        if second is None:continue
                        stats[f"after_two_{len(second)}"]+=1
                        if len(second)!=10:continue
                        missing=set(range(COUNT))-set(second)
                        for p28 in range(max(pd+84,180),394):
                            if (p28+229)%COUNT not in missing:continue
                            sixth=compatible(second,last[p28])
                            if sixth is None or len(sixth)!=11:continue
                            stats["sixth_window_11_of_12"]+=1
                            for p7 in range(pa+26,pc-16):
                                final=bridge(sixth,p7,pc,g,c,COUNT)
                                if final is None or len(final)!=COUNT:continue
                                stats["seven_window_complete"]+=1
                                seed=sum(final[j]<<(32*j) for j in range(COUNT))
                                predicted=random.Random(seed).getrandbits(32*(pa+233))>>(32*(pa+232))
                                if predicted==heldout:
                                    stats["heldout_matches"]+=1
                                    print("HELDOUT_MATCH",pa,pc,p7,p11,pb,pd,p28,seed,flush=True)
    print("selected_row129_withheld",True,"seed_bits",384,
          "elapsed_seconds",round(time.monotonic()-begun,2),flush=True)
    print("SEVEN_WINDOW_STATS",dict(stats),flush=True)
    print("K04_K08_UNRESOLVED",flush=True)

if __name__=="__main__":
    if len(sys.argv)!=2:raise SystemExit("python k04_seed_seven_window.py source.zip")
    print("SYNTHETIC_CALIBRATION",synthetic(),flush=True)
    main(Path(sys.argv[1]))
