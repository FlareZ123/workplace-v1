"""K04: source-conditioned sixth initialized-state window for 352/384-bit seeds.

The new input is the row28/59/80/111 run (-1..+2, 227 apart) enabled by
the two RC-17 Rev B PURGE/VERIFY source-control fingerprints. It contributes
one independently constrained 32-bit seed word to Agent8's two-bridge method.

Only first-cycle CPython random.Random(numeric-seed) hypotheses are tested.
Selected ACK row129, K04/K08 commitments and route mask are never loaded.
"""
import collections
import random
import sys
import time
from pathlib import Path

AGENTS=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(AGENTS/"agent1"),str(AGENTS/"agent8"),str(AGENTS/"agent23"),
              str(AGENTS/"agent31"),str(Path(__file__).resolve().parent)]
from k04_python_seed_fragments import compatible,extract_pairs,fragments,ALL
from k04_seed_stitch import bridge,pair_group
from k04_mt_rowstart import untemper
from k04_mt_recursive_peel import close_group,rows,temper
from k04_cross_carrier_seed_windows import indexed_groups

def row28_pairs(source):
    words,clusters=indexed_groups(source,True)
    entries=next(e for e in clusters.values() if any(row==28 for row,_ in e))
    start=dict(entries)[28]-1
    state,_=close_group(entries,words)
    assert all(state[start+j][0]==ALL and state[start+j+227][0]==ALL
               for j in range(4))
    return [(state[start+j][1],state[start+j+227][1]) for j in range(4)]

def sources(source):
    a,c,b,d=extract_pairs(source)
    e=pair_group(source,11,3)
    f=row28_pairs(source)
    return a,c,e,b,d,f

def synthetic(count):
    seed=sum(((0x34123412+0x345211*j)&ALL)<<(32*j) for j in range(count))
    rng=random.Random(seed)
    state=[untemper(rng.getrandbits(32)) for _ in range(624)]
    def fake(p,n):
        return [(state[p+j],state[p+j+227]) for j in range(n)]
    pa=14
    a=fake(pa,5)
    # Phase model is constrained by regular-row minimum 6-draw transitions.
    for pc in range(57,87):
        c=fake(pc,4)
        for pb in range(max(73,pc+25), min(128,pc+75)):
            b=fake(pb,5)
            for pd in range(pb+8,min(pb+19,136)):
                d=fake(pd,4)
                keys={}
                for p,pairs in ((pa,a),(pc,c),(pb,b),(pd,d)):
                    keys=compatible(keys,fragments(pairs,p,count))
                    if keys is None:break
                if keys is None:continue
                for p11 in range(pc+4,min(pc+19,pb-6)):
                    e=fake(p11,3)
                    first=bridge(keys,pc,p11,c,e,count)
                    if first is None:continue
                    second=bridge(first,pb,pd,b,d,count)
                    if second is None or len(second)!=count-1:continue
                    missing=next(i for i in range(count) if i not in second)
                    # Row28 must follow row14 by at least fourteen ordinary rows.
                    for p28 in range(pd+84,394):
                        if (p28+229)%count!=missing:continue
                        f=fake(p28,4)
                        merged=compatible(second,fragments(f,p28,count))
                        if merged and len(merged)==count:
                            assert sum(merged[j]<<(32*j) for j in range(count))==seed
                            print("SYNTHETIC_THIRD_WINDOW_PASS",count*32,
                                  (pa,pc,p11,pb,pd,p28),flush=True)
                            return True
    print("SYNTHETIC_THIRD_WINDOW_NOT_COVERED",count*32,flush=True)
    return False

def main(source,count):
    a,c,e,b,d,f=sources(source)
    observed=rows(source)
    assert not observed[129]
    heldout=temper(observed[34][3])
    phase_sets=((a,range(14,69)),(c,range(50,105)),
                (b,range(73,128)),(d,range(81,136)))
    lookups=[{p:fragments(pairs,p,count) for p in phases}
             for pairs,phases in phase_sets]
    later={p:fragments(f,p,count) for p in range(180,394)}
    stats=collections.Counter()
    started=time.monotonic()
    for pa,ka in lookups[0].items():
        for pb,kb in lookups[2].items():
            if not 59<=pb-pa<=113:continue
            ab=compatible(ka,kb)
            if ab is None:continue
            for pc,kc in lookups[1].items():
                if not (35<=pc-pa-1<=89 and 24<=pb+1-pc<=78):continue
                abc=compatible(ab,kc)
                if abc is None:continue
                for pd,kd in lookups[3].items():
                    if not 8<=pd-pb<=18:continue
                    keys=compatible(abc,kd)
                    if keys is None:continue
                    stats["four_group_phase_compatible"]+=1
                    for p11 in range(pc+4,min(pc+19,pb-6)):
                        first=bridge(keys,pc,p11,c,e,count)
                        if first is None:continue
                        stats["first_bridge"]+=1
                        second=bridge(first,pb,pd,b,d,count)
                        if second is None:continue
                        stats["second_bridge"]+=1
                        stats[f"key_words_after_two_{len(second)}"]+=1
                        if len(second)<count-1:continue
                        missing=[j for j in range(count) if j not in second]
                        if len(missing)>1:continue
                        for p28 in range(max(pd+84,180),394):
                            if missing and (p28+229)%count!=missing[0]:continue
                            merged=compatible(second,later[p28])
                            if merged is None or len(merged)!=count:continue
                            stats["complete_seed_assignments"]+=1
                            seed=sum(merged[j]<<(32*j) for j in range(count))
                            predicted=random.Random(seed).getrandbits(32*(pa+233))>>(32*(pa+232))
                            if predicted==heldout:
                                stats["heldout_matches"]+=1
                                print("HELDOUT_MATCH",count,pa,pc,p11,pb,pd,p28,seed,flush=True)
    print("selected_row129_withheld",True,
          "integer_seed_bits",32*count,
          "elapsed_seconds",round(time.monotonic()-started,2),flush=True)
    print("SOURCE_STATS",dict(stats),flush=True)
    print("K04_K08_UNRESOLVED",flush=True)

if __name__=="__main__":
    if len(sys.argv)!=2:raise SystemExit("python k04_seed_six_window.py source.zip")
    for count in (11,12):
        print("CALIBRATE",32*count,flush=True)
        calibrated=synthetic(count)
        print("SOURCE_RUN",32*count,"synthetic_control",calibrated,flush=True)
        main(Path(sys.argv[1]),count)
