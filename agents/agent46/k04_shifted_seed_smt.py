"""K04 shifted MT stream: solve third 96-bit Python seed word with bit-vector algebra.

Five 227-apart output pairs near source printer row3 recover two of
three seeded key-array words. The new CRC-good TRP2 row7/38 group supplies
two more initialized-state boundary words. Solve their deterministic
init_by_array bridge for the remaining unknown key instead of 2^32 guessing.

Requires z3-solver; does not access row129, REC8 commitments, or mask.
Docs: z3prover.github.io/api/html/namespacez3py.html (BitVec,LShR,Solver).
"""
from pathlib import Path
import random
import sys
import time

from z3 import BitVec,BitVecVal,LShR,Solver,sat,unsat,unknown

AGENTS=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(AGENTS/"agent1"),str(AGENTS/"agent23"),str(AGENTS/"agent31"),
             str(Path(__file__).resolve().parent)]
from k04_python_seed_fragments import (ALL,INITIAL,compatible,extract_pairs,
                                       fragments,initial_words,verify_seed)
from k04_mt_rowstart import untemper
from k04_cross_carrier_seed_windows import indexed_groups
from k04_mt_recursive_peel import close_group

def row7_pairs(source):
    words,clusters=indexed_groups(source,True)
    entries=next(entries for entries in clusters.values()
                 if any(r==7 for r,_ in entries))
    start=dict(entries)[7]+1
    state,_=close_group(entries,words)
    assert all(state[start+j][0]==ALL and state[start+j+227][0]==ALL
               for j in range(3))
    return [(state[start+j][1],state[start+j+227][1]) for j in range(3)]

def symbolic_step(a,b,key,index,count):
    if isinstance(a,int):a=BitVecVal(a,32)
    if isinstance(b,int):b=BitVecVal(b,32)
    first=(b+(index-1)) ^ ((a ^ LShR(a,30))*1566083941)
    second=(BitVecVal(INITIAL[index],32)
            ^((first ^ LShR(first,30))*1664525))
    second=second+key+((index-1)%count)
    return (second ^ ((b ^ LShR(b,30))*1566083941))-index

def recover_pair(a,g,pa,pg,timeout_ms=5000):
    """Return (status, seed-dictionary, elapsed) for an exact phase pair."""
    initial=initial_words(a)
    terminal=initial_words(g)
    assert len(initial)==4 and len(terminal)==2
    known=fragments(a,pa,3)
    assert known is not None and len(known)==2
    missing=next(i for i in range(3) if i not in known)
    unknown_key=BitVec("K_missing",32)
    sequence={pa+228+i:word for i,word in enumerate(initial)}
    solver=Solver()
    solver.set(timeout=timeout_ms)
    started=time.monotonic()
    for i in range(pa+232,pg+230):
        keyindex=(i-1)%3
        key=(BitVecVal(known[keyindex],32)
             if keyindex in known else unknown_key)
        sequence[i]=symbolic_step(sequence[i-2],sequence[i-1],key,i,3)
        if i in (pg+228,pg+229):
            solver.add(sequence[i]==terminal[i-(pg+228)])
    outcome=solver.check()
    elapsed=round(time.monotonic()-started,3)
    if outcome==sat:
        word=solver.model().eval(unknown_key).as_long()
        key=dict(known)
        key[missing]=word
        return "SAT",key,elapsed
    if outcome==unsat:return "UNSAT",None,elapsed
    return "TIMEOUT_OR_UNKNOWN",None,elapsed

def synthetic():
    n=3
    seed=sum(((0x31415926+0x123fed*i)&ALL)<<(i*32) for i in range(n))
    rng=random.Random(seed)
    state=[untemper(rng.getrandbits(32)) for _ in range(624)]
    pa,pg=320,346
    a=[(state[pa+j],state[pa+j+227]) for j in range(5)]
    g=[(state[pg+j],state[pg+j+227]) for j in range(3)]
    result,keys,elapsed=recover_pair(a,g,pa,pg,timeout_ms=20000)
    print("SYNTHETIC_SOLVE",result,"seconds",elapsed,flush=True)
    if result=="SAT":
        actual=sum(keys[i]<<(i*32) for i in range(n))
        assert actual==seed and verify_seed(actual,[(pa,a),(pg,g)])
        print("SYNTHETIC_96BIT_RECONSTRUCTION_PASS",pa,pg,flush=True)
    return result=="SAT"

def main(source):
    a=extract_pairs(source)[0]
    g=row7_pairs(source)
    attempts=0
    statuses={"SAT":0,"UNSAT":0,"TIMEOUT_OR_UNKNOWN":0}
    print("ORIGINAL_SOURCE_MODEL","one_early_first_cycle",
          "prefix_bound_row3_start_at_least_309",flush=True)
    started=time.monotonic()
    for pa in (309,316,324,332,340,348,356,368):
        if pa>368:continue
        for gap in (26,30,34,38):
            pg=pa+gap
            if pg>394:continue
            attempts+=1
            status,keys,elapsed=recover_pair(a,g,pa,pg,timeout_ms=1800)
            statuses[status]+=1
            print("SOURCE_PHASE_TEST",pa,pg,status,"seconds",elapsed,flush=True)
            if status=="SAT":
                seed=sum(keys[j]<<(32*j) for j in range(3))
                # An independent, strictly retained source prediction.
                if verify_seed(seed,[(pa,a),(pg,g)]):
                    print("SOURCE_KEY_MATCH",pa,pg,format(seed,"024X"),flush=True)
    print("selected_row129_withheld",True,
          "source_phase_pairs_tested",attempts,
          "elapsed_seconds",round(time.monotonic()-started,2))
    print("SOURCE_SMT_RESULTS",statuses)
    print("UNTESTED_PHASES",True)
    print("K04_K08_UNRESOLVED",flush=True)

if __name__=="__main__":
    if len(sys.argv)!=2:raise SystemExit("python k04_shifted_seed_smt.py source.zip")
    synthetic()
    main(Path(sys.argv[1]))
