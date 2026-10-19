"""Exact GF(2) joint K04 two-sampler and tail identifiability witness.
Usage: python agents/agent50/k04_joint_target_ambiguity.py original-case.zip
Original selected printer row129, mask, routing and acceptance withheld.
"""
from pathlib import Path
import hashlib
import sys

AGENTS = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(AGENTS / 'agent23'), str(AGENTS / 'agent31')]
from k04_mt_recursive_peel import rows, groups, temper

if len(sys.argv) != 2:
    raise SystemExit('usage: python agents/agent50/k04_joint_target_ambiguity.py original-case.zip')
values = rows(Path(sys.argv[1]))
assert len(values) == 133 and not values[129]
clusters = groups(Path(sys.argv[1]), values)

ALL = 0xffffffff
A = 0x9908b0df
START = -229

def symbolic(last):
    state = {START+i:[1<<(32*i+b) for b in range(32)] for i in range(624)}
    for position in range(START+624,last+1):
        t = position-624
        mid,left,right = state[t+397],state[t],state[t+1]
        state[position] = [
            mid[b] ^ (right[b+1] if b<30 else (left[31] if b==30 else 0)) ^
            (right[0] if (A>>b)&1 else 0) for b in range(32)
        ]
    return state

def eliminate(equations, prior=None):
    basis = {} if prior is None else dict(prior)
    dependent = 0
    for vector, rhs in equations:
        while vector:
            pivot = vector.bit_length()-1
            if pivot not in basis:
                basis[pivot] = (vector,rhs)
                break
            known,answer = basis[pivot]
            vector ^= known
            rhs ^= answer
        else:
            assert not rhs, 'inconsistent MT source or sampled metadata'
            dependent += 1
    return basis,dependent

def reduce(vector,basis):
    rhs = 0
    while vector:
        pivot = vector.bit_length()-1
        if pivot not in basis:
            return vector,rhs
        known,answer = basis[pivot]
        vector ^= known
        rhs ^= answer
    return 0,rhs

def rank(vectors):
    pivots = {}
    for vector in vectors:
        while vector:
            pivot = vector.bit_length()-1
            if pivot not in pivots:
                pivots[pivot] = vector
                break
            vector ^= pivots[pivot]
    return len(pivots)

def output_bits(word,width):
    result=[]
    for b in range(32-width,32):
        value=0
        for bit in range(32):
            if (temper(1<<bit)>>b)&1:
                value ^= word[bit]
        result.append(value)
    return result

def code_equations(symbolic_words, position, width, code):
    return [(vector,(code>>i)&1) for i,vector in
            enumerate(output_bits(symbolic_words[position],width))]

# Printer witness groups: s44=s43+11 and s97=s96+12. In this
# feasible RECOVER-tail branch s129=s128+4=s43+627; tail has no extra draws.
G = 11
left = next(g for g in clusters.values() if any(r==43 and p==0 for r,p in g))
right = next(g for g in clusters.values() if any(r==44 and p==0 for r,p in g))
assert (len(left),len(right)) == (5,6)
source_rows = left + [(r,p+G) for r,p in right]
expressions = symbolic(692)
observed = [
    (expressions[p+j][bit],(v>>bit)&1)
    for r,p in source_rows for j,v in enumerate(values[r]) for bit in range(32)
]
base,dependent = eliminate(observed)
assert (len(base),dependent) == (1123,285)
print('source_only_rank',len(base),'source_dependent',dependent)

# A *single explicit* accepted/rejected draw path valid for both n=3 and n=4
# CLASS hypotheses, with no extra draws beyond DEST followed by CLASS:
#   43 DEST bench p4=2, 44 CLASS STORES p5..9 rejects, p10=1;
#   96 DEST store p397=0, 97 CLASS LABEL p398..403 rejects, p404=0.
# 3-bit codes >=4 are rejected by both models; 2-bit code3 rejects DEST.
paths = {
    4:(2,2),5:(3,4),6:(3,4),7:(3,4),8:(3,4),9:(3,7),10:(3,1),
    397:(2,0),398:(3,5),399:(3,6),400:(3,4),401:(3,4),
    402:(3,4),403:(3,4),404:(3,0)
}
equations = [
    eq for pos,(width,code) in paths.items()
    for eq in code_equations(expressions,pos,width,code)
]
joint,dep = eliminate(equations,base)
assert len(joint)-len(base)==29 and dep==14
target = [reduce(v,joint)[0] for pos in range(627,631)
          for v in output_bits(expressions[pos],32)]
assert all(target) and rank(target)==128
print('joint_sampler_equations',len(equations),
      'joint_added_rank',len(joint)-len(base),
      'target_rank',rank(target),
      'fixed_target_bits',sum(x==0 for x in target))

# Two fully reconstructed MT *trajectories*: both reproduce all 44 source
# words in eleven untouched printer rows and fifteen specified sampler
# outputs, yet they produce opposite 128-bit selected-row values.
for target_word in (0,ALL):
    target_constraints = [
        (vector,(target_word>>bit)&1)
        for pos in range(627,631)
        for bit,vector in enumerate(output_bits(expressions[pos],32))
    ]
    complete,dependent = eliminate(target_constraints,joint)
    assert len(complete)==len(joint)+128
    solution=0
    for pivot in sorted(complete):
        vector,rhs=complete[pivot]
        lower=vector^(1<<pivot)
        solution |= (rhs^((lower&solution).bit_count()&1))<<pivot
    stream={START+i:(solution>>(32*i))&ALL for i in range(624)}
    for pos in range(START+624,693):
        t=pos-624
        y=(stream[t]&0x80000000)|(stream[t+1]&0x7fffffff)
        stream[pos]=stream[t+397]^(y>>1)^(A if y&1 else 0)
    for r,p in source_rows:
        for j,expected in enumerate(values[r]):
            assert stream[p+j]==expected
    for pos,(width,expected) in paths.items():
        assert temper(stream[pos])>>(32-width)==expected
    assert all(temper(stream[p])==target_word for p in range(627,631))
    statebytes=b''.join(stream[START+i].to_bytes(4,'little') for i in range(624))
    print('counterexample_target_word',f'{target_word:08X}',
          'synthetic_state_sha256',hashlib.sha256(statebytes).hexdigest(),
          'original_rows_reproduced',len(source_rows),
          'specified_sampler_words_reproduced',len(paths))
print('shared_models_n3_n4_both_feasible',True)
print('selected_row129_and_acceptance_withheld',True)
print('K04_K08_UNRESOLVED')
