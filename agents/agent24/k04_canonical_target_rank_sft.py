"""Fix early-exit GF2 quotient overcount by direct source+target matrix rank.

Run: python agents/agent24/k04_canonical_target_rank_sft.py original.zip [fixture.json ...]
Requires original unchanged 43-member source export; withholds selected row129,
K04 coupon/mask, acceptance commitments, and all K08 data.
"""
import json
import random
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from agents.agent33.k04_global_target_projection import (
    source_rows, state_expressions, tempered_expressions, temper, untemper
)


def insert(basis,v):
    while v:
        pivot=v.bit_length()-1
        old=basis.get(pivot)
        if old is None:
            basis[pivot]=v
            return
        v ^= old


def canonical(basis,v,pivot_mask):
    # Crucial: eliminate ALL occupied pivots, including pivots below a
    # currently unoccupied higher bit. The old function stopped early.
    while v & pivot_mask:
        p=(v & pivot_mask).bit_length()-1
        v ^= basis[p]
    return v


def analyze(rows,starts):
    assert len(rows)==len(starts)==133 and not rows[129]
    assert starts[0]==0 and all(starts[i+1]>=starts[i]+4 for i in range(132))
    terms=state_expressions(starts[-1]+3)
    source={}
    augmented={}
    for r,words in enumerate(rows):
        if r==129: continue
        for j,value in enumerate(words):
            for bit,expr in enumerate(terms[starts[r]+j]):
                insert(source,expr)
                v=(expr<<1)|((value>>bit)&1)
                while v:
                    pivot=v.bit_length()-1
                    old=augmented.get(pivot)
                    if old is None:break
                    v ^= old
                if v==1:
                    raise ValueError("Original source contradiction at row %d" % r)
                if v:
                    augmented[v.bit_length()-1]=v
    source_rank=len(source)
    combined=source.copy()
    mask=sum(1<<p for p in augmented if p>0)
    fixed={}
    for j in range(4):
        for b,expr in enumerate(tempered_expressions(terms[starts[129]+j])):
            insert(combined,expr)
            v=canonical(augmented,expr<<1,mask)
            if v in (0,1):fixed[32*j+b]=v
    return {"source_rank":source_rank,
            "target_quotient_rank":len(combined)-source_rank,
            "fixed_target_bits":fixed}


def synthetic():
    for gap,expected_rank,expected_fixed in (
        (4,128,0),(5,64,58),(6,32,96),(7,96,32),
        (8,97,28),(9,65,58),(10,126,0)
    ):
        starts=[gap*r for r in range(133)]
        rng=random.Random(20261019)
        stream=[untemper(rng.getrandbits(32)) for _ in range(starts[-1]+4)]
        rows=[stream[s:s+4] for s in starts]
        withheld=[temper(x) for x in rows[129]]
        rows[129]=[]
        result=analyze(rows,starts)
        assert result["target_quotient_rank"]==expected_rank
        assert len(result["fixed_target_bits"])==expected_fixed
        assert all((withheld[k//32]>>(k%32))&1==v
                   for k,v in result["fixed_target_bits"].items())
        print("synthetic h",gap,"exact quotient",expected_rank,
              "fixed",expected_fixed,flush=True)
    # Independent pure-GF2 minimal counterexample:
    # source basis [0b0110], selected expressions [0b1000, 0b1110].
    # Their difference 0b0110 is source-known, so exact quotient=1.
    basis={}
    insert(basis,0b0110)
    joined=basis.copy()
    insert(joined,0b1000)
    insert(joined,0b1110)
    assert len(joined)-len(basis)==1
    assert canonical(basis,0b1110,sum(1<<p for p in basis))==0b1000
    print("minimal counterexample and seven withheld-output controls PASS")


def main():
    synthetic()
    if len(sys.argv)==1:return
    rows=source_rows(Path(sys.argv[1]))
    for file in sys.argv[2:]:
        starts=json.loads(Path(file).read_text(encoding="utf-8"))["row_starts"]
        result=analyze(rows,starts)
        print("original consistent fixture",file,"index",starts[129],
              "source_rank",result["source_rank"],
              "EXACT quotient rank",result["target_quotient_rank"],
              "fixed target bits",result["fixed_target_bits"],flush=True)


if __name__=="__main__":
    main()
