"""Exact K04 target-observability test for hypothetical external MT words.

Usage: python agents/agent4/k04_future_donor_quotient_sft.py original-case.zip
Only intact original spool words and published index955 model are accessed;
selected row129 is withheld, and no acceptance or mask is consulted.
"""
import json
import random
import sys
from pathlib import Path
from agents.agent33.k04_global_target_projection import (
    source_rows, state_expressions, tempered_expressions, untemper, temper,
)

LIMIT = 1600

def add(basis, e):
    while e:
        p = e.bit_length()-1
        old = basis.get(p)
        if old is None:
            basis[p] = e
            return True
        e ^= old
    return False

def reduce(basis, e):
    while e:
        old = basis.get(e.bit_length()-1)
        if old is None:
            return e
        e ^= old
    return 0

def make_basis(rows, starts, terms):
    basis = {}
    for r, words in enumerate(rows):
        for j, val in enumerate(words):
            for e in terms[starts[r]+j]:
                add(basis, e)
    return basis

def add_donors(basis, terms, starts):
    b = basis.copy()
    for start in starts:
        for k in range(start, start+4):
            for e in terms[k]:
                add(b, e)
    return b

def quotient(basis, target):
    # Exact quotient: extend a COPY of source basis by every target vector.
    # Independent early-stopped target reductions can overcount this rank.
    b = basis.copy()
    before = len(b)
    for e in target:
        add(b, e)
    masks=[]
    for word in range(4):
        mask = 0
        for bit, e in enumerate(target[word*32:(word+1)*32]):
            if reduce(basis, e) == 0:
                mask |= 1 << bit
        masks.append(f'{mask:08X}')
    return len(b)-before, masks

def check_synthetic(starts, terms, target):
    rng=random.Random(20261019)
    truth=[untemper(rng.getrandbits(32)) for _ in range(LIMIT+4)]
    rows=[truth[s:s+4] if r!=129 else [] for r,s in enumerate(starts)]
    original=make_basis(rows,starts,terms)
    cases=[([],128),([728],127),([1182],97),([1410],66),([332,728],0)]
    for offsets, expected in cases:
        b=add_donors(original,terms,offsets)
        rank,masks=quotient(b,target)
        assert rank==expected, (offsets,rank)
        affine={}
        for r,row in enumerate(rows):
            for j,value in enumerate(row):
                for bit,e in enumerate(terms[starts[r]+j]):
                    add(affine,(e<<1)|((value>>bit)&1))
        for s in offsets:
            for j in range(s,s+4):
                for bit,e in enumerate(terms[j]):
                    add(affine,(e<<1)|((truth[j]>>bit)&1))
        for bit,e in enumerate(target):
            if (int(masks[bit//32],16)>>(bit%32))&1:
                got=reduce(affine,e<<1)
                want=(temper(truth[starts[129]+bit//32])>>(bit%32))&1
                assert got==want, (offsets,bit)
    print('Seeded withheld-target controls: 5/5 PASS')

def main():
    assert len(sys.argv)==2, 'usage: k04_future_donor_quotient_sft.py original-case.zip'
    # Counterexample to the published early-stop/separate-target rank logic.
    e3=1<<3
    e5=1<<5
    assert quotient({3:e3},[e5^e3,e5]+[0]*126)[0]==1
    root=Path(__file__).resolve().parents[2]
    starts=json.loads((root/'results/h17-k04-source-consistent-index955.json').read_text())['row_starts']
    assert len(starts)==133 and starts[129]==955
    terms=state_expressions(LIMIT+3)
    target=[e for j in range(4) for e in tempered_expressions(terms[starts[129]+j])]
    rows=source_rows(Path(sys.argv[1]))  # SHA256 pinned; disputed row129 set to [].
    assert len(rows[129])==0
    basis=make_basis(rows,starts,terms)
    assert len(basis)==15305, len(basis)
    # Validate all original data equations on the indexed MT stream.
    affine={}
    for r, words in enumerate(rows):
        for j,value in enumerate(words):
            for bit,e in enumerate(terms[starts[r]+j]):
                equation=(e<<1)|((value>>bit)&1)
                assert reduce(affine,equation)!=1, (r,j,bit)
                add(affine,equation)
    check_synthetic(starts,terms,target)
    assert quotient(basis,target)==(128,['00000000']*4)
    for offsets, expected in [([728],127),([1182],97),([1410],66),
                              ([1182,1410],66),([728,1410],65),([332,728],0)]:
        result=quotient(add_donors(basis,terms,offsets),target)
        assert result[0]==expected, (offsets,result)
        print('Counterfactual full32 donor starts',offsets,'K04 quotient',result)
    intact={starts[r]+j for r in range(133) if r!=129 for j in range(4)}
    singles=[]
    for t in range(LIMIT+1):
        if t in intact or starts[129]<=t<starts[129]+4:
            continue
        b=basis.copy()
        for e in terms[t]:
            add(b,e)
        # Avoid repeated 128 independent rank/mask queries during the scan.
        c=b.copy()
        before=len(c)
        for e in target:
            add(c,e)
        gain=128-(len(c)-before)
        if gain:
            singles.append((t,gain))
    assert singles==[(728,1),(1185,31),(1411,30),(1412,32)],singles
    windows=[]
    for t in range(LIMIT-2):
        if t<=starts[129]+3 and t+3>=starts[129]:
            continue
        c=add_donors(basis,terms,[t])
        before=len(c)
        for e in target:
            add(c,e)
        gain=128-(len(c)-before)
        if gain:
            windows.append((t,gain))
    assert windows==[(725,1),(726,1),(727,1),(728,1),
                    (1182,31),(1183,31),(1184,31),(1185,31),
                    (1408,30),(1409,62),(1410,62),(1411,62),(1412,32)],windows
    print('Original rank: 15305; actual K04 target quotient: 128 of 128')
    print('Counterfactual single-word leverage:',singles)
    print('Counterfactual four-word leverage:',windows)
    print('Historical target coupon bits recovered: zero')

if __name__=='__main__':
    main()
