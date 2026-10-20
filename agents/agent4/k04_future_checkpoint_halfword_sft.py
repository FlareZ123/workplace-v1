"""Source-conditional K04 target leverage of future 16-bit transfer-style checkpoints.

Run from repository root with original 43-member H-17 ZIP path as argument.
All original selected row129 payload bytes and acceptance commitments are withheld.
"""
import json
import random
import sys
from pathlib import Path
from agents.agent33.k04_global_target_projection import (
    state_expressions, source_rows, tempered_expressions, untemper, temper,
)
from agents.agent4.k04_future_donor_quotient_sft import add, quotient, make_basis, reduce

LIMIT=1603

def observe_upper16(b,terms,positions):
    c=b.copy()
    for t in positions:
        for e in tempered_expressions(terms[t])[16:32]:
            add(c,e)
    return c

def verify_synthetic(starts,terms,target):
    rng=random.Random(20261020)
    truth=[untemper(rng.getrandbits(32)) for _ in range(LIMIT+1)]
    rows=[truth[s:s+4] if r!=129 else [] for r,s in enumerate(starts)]
    original=make_basis(rows,starts,terms)
    for positions,rank in [([],128),([1185],113),([1411],114),([1412],112),
                            ([1411,1412],98),([1410,1411,1412,1413],98)]:
        observed=observe_upper16(original,terms,positions)
        got,masks=quotient(observed,target)
        assert got==rank,(positions,got)
        affine={}
        for r,row in enumerate(rows):
            for j,w in enumerate(row):
                for bit,e in enumerate(terms[starts[r]+j]):
                    add(affine,(e<<1)|((w>>bit)&1))
        for pos in positions:
            for bit,e in enumerate(tempered_expressions(terms[pos])[16:],16):
                add(affine,(e<<1)|((temper(truth[pos])>>bit)&1))
        for bit,e in enumerate(target):
            if (int(masks[bit//32],16)>>(bit%32))&1:
                inferred=reduce(affine,e<<1)
                actual=(temper(truth[starts[129]+bit//32])>>(bit%32))&1
                assert inferred==actual,(positions,bit,inferred,actual)
    print('Six real seeded-MT masked-payload positive controls PASS')

def main():
    assert len(sys.argv)==2
    root=Path(__file__).resolve().parents[2]
    starts=json.loads((root/'results/h17-k04-source-consistent-index955.json').read_text())['row_starts']
    terms=state_expressions(LIMIT)
    target=[e for j in range(4) for e in tempered_expressions(terms[starts[129]+j])]
    original=make_basis(source_rows(Path(sys.argv[1])),starts,terms)
    assert len(original)==15305
    verify_synthetic(starts,terms,target)
    expected=[([1185],113,['00000000','00000000','00000000','BBF70000']),
              ([1411],114,['00000000','00000000','9BF30000','00000000']),
              ([1412],112,['00000000','00000000','00000000','FFFF0000']),
              ([1411,1412],98,['00000000','00000000','9BF30000','FFFF0000']),
              ([1410,1411,1412,1413],98,['00000000','00000000','9BF30000','FFFF0000'])]
    for positions,rank,masks in expected:
        got=quotient(observe_upper16(original,terms,positions),target)
        assert got==(rank,masks),(positions,got)
        print('Hypothetical future upper16 checkpoints',positions,'K04 target rank/masks',got)
    for size in [1,2,4,8,16]:
        gain=[]
        for start in range(975,1501-size):
            b=observe_upper16(original,terms,range(start,start+size))
            rank,_=quotient(b,target)
            if rank<128:
                gain.append((start,128-rank))
        assert max((k for s,k in gain),default=0)==(16 if size==1 else 30)
        print('Future high16 source-control window length',size,'positive count',len(gain),'max gain',max(k for s,k in gain))
    print('No original historical checkpoint-to-index linkage; actual K04 recovered bits = 0')

if __name__=='__main__':
    main()
