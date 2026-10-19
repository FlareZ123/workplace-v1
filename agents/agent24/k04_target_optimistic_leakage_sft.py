"""K04 source-only optimistic metadata leakage rank (conditional graph placements).

Run with the original case ZIP. Requires SciPy. The original K04 selected row129,
acceptance commitments, route mask and K08 materials are excluded. Graph-only
placements may contradict retained source bits; NONE authenticates coupon bytes.
"""
import random
import sys
from pathlib import Path

from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import coo_matrix

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "agent37"))
from k04_global_inverse_chronology_sft import source, conflicts

MAG = 0x9908B0DF
ALL = 0xFFFFFFFF


def stream_terms(n):
    out = [[1 << (32*p+b) for b in range(32)] for p in range(624)]
    for p in range(624, n):
        a, b, c = out[p-624], out[p-623], out[p-227]
        out.append([c[k] ^ (a[31] if k == 30 else b[k+1] if k < 30 else 0)
                    ^ (b[0] if MAG >> k & 1 else 0) for k in range(32)])
    return out[:n]


def tempered(bits):
    for sign, shift, mask in ((-1,11,ALL),(1,7,0x9D2C5680),
                              (1,15,0xEFC60000),(-1,18,ALL)):
        nxt = list(bits)
        for k in range(32):
            j = k-shift if sign == 1 else k+shift
            if 0 <= j < 32 and mask >> k & 1:
                nxt[k] ^= bits[j]
        bits = nxt
    return bits


def target_rank(starts, extra_bits):
    """Even optimistically revealing top extra_bits of EVERY missing non-target draw."""
    terms = stream_terms(starts[-1]+4)
    basis = {}
    def reduce(v):
        while v:
            p = v.bit_length()-1
            existing = basis.get(p)
            if existing is None:
                return v
            v ^= existing
        return 0
    def add(v):
        v = reduce(v)
        if v:
            basis[v.bit_length()-1] = v
    used = set()
    for r, start in enumerate(starts):
        if r == 129:
            continue
        for p in range(start,start+4):
            assert p not in used
            used.add(p)
            for v in terms[p]:
                add(v)
    source_rank = len(basis)
    for p in range(len(terms)):
        if p in used or starts[129] <= p < starts[129]+4:
            continue
        if extra_bits:
            for v in tempered(terms[p])[-extra_bits:]:
                add(v)
    augmented_rank = len(basis)
    independent = {}
    fixed = 0
    for p in range(starts[129],starts[129]+4):
        for v in tempered(terms[p]):
            v = reduce(v)
            if not v:
                fixed += 1
                continue
            while v:
                pivot = v.bit_length()-1
                old = independent.get(pivot)
                if old is None:
                    independent[pivot] = v
                    break
                v ^= old
    return source_rank, augmented_rank, len(independent), fixed


def graph_model(within, boundary, index):
    eq = [({r+1:1,r:-1,133+r:-1},4) for r in range(132)]
    for (r,j),(m,k),(e,l) in within:
        eq += [({m:1,r:-1},397+j-k),({e:1,r:-1},624+j-l)]
    for r,bit,(m,k),(e,l) in boundary:
        eq += [({m:1,r:-1},396-k),({e:1,r:-1},623-l)]
    for r,m,d in ((9,40,229),(9,63,398),(9,124,852)):
        eq.append(({m:1,r:-1},d))
    rr=[];cc=[];vv=[];fixed=[]
    for i,(coeff,value) in enumerate(eq):
        fixed.append(value)
        for j,v in coeff.items():
            rr.append(i);cc.append(j);vv.append(v)
    matrix = coo_matrix((vv,(rr,cc)),shape=(len(eq),265)).tocsc()
    lower=[0]*265; upper=[974]*265
    lower[0]=upper[0]=0
    lower[129]=upper[129]=index
    for r in range(127):
        lower[133+r]=2
        upper[133+r]=973-index
    for r in range(127,132):
        upper[133+r]=973-index
    return Bounds(lower,upper),LinearConstraint(matrix,fixed,fixed)


def main(case_zip):
    words,within,boundary=source(case_zip)
    assert len(within)==25 and len(boundary)==17 and not words[129]
    assert target_rank([6*r for r in range(133)],0)[2:] == (32,96)
    print("Synthetic h6: 32 unknown, 96 fixed original-format payload bits, PASS")
    for target in (947,950,955):
        bounds,constraint=graph_model(within,boundary,target)
        rng=random.Random(20261019+target)
        histogram={};smallest=10**9;seen=set()
        for i in range(100):
            cost=[0]*265
            for j in range(133,265):
                cost[j]=rng.uniform(-1,1)
            answer=milp(cost,integrality=[1]*265,bounds=bounds,
                        constraints=constraint,options={'time_limit':3})
            assert answer.x is not None, (target,i,answer.message)
            starts=[round(v) for v in answer.x[:133]]
            assert starts[129]==target
            assert (starts[40]-starts[9],starts[63]-starts[9],starts[124]-starts[9])==(229,398,852)
            seen.add(tuple(starts))
            _,_,rank,fixed=target_rank(starts,16)
            histogram[rank]=histogram.get(rank,0)+1
            smallest=min(smallest,len(conflicts(words,starts)))
            if target==950 and i==0:
                for bits in (0,2,3,16,20,24,28,30,31,32):
                    print("target950 example top-bit oracle",bits,"->",target_rank(starts,bits))
        print("selected index",target,"unique model-only geometries",len(seen),
              "oracle16 target rank histogram",histogram,
              "minimum original recurrence contradictions",smallest)
        assert len(seen)==100 and histogram=={128:100} and smallest>0
    print("ZERO original coupon bits recovered; zero K08 caption words.")


if __name__ == "__main__":
    main(sys.argv[1])
