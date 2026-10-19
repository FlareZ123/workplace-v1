"""Source-only GF(2) target-leverage test for hypothetical printer metadata samplers.
Run from repository root; optional first argument is an original spool file path.
No selected row129 payload, mask, acceptance data or verifier is used.
"""
import hashlib
import random
import re
import struct
import sys
from pathlib import Path

SOURCE = Path(sys.argv[1] if len(sys.argv)>1 else 'resources/evidence/print/spool-reconstruction.log')
EXPECTED_SHA = '7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083'
MT_A = 0x9908B0DF
LO, HI = -229, 720
GROUP_43 = {12:-229,43:0,66:167,96:393,128:623}
GROUP_44 = {13:-227,44:0,67:168,97:394,130:620,131:624}
ORDINARY = {12,43,66,96,13,44,67,97}

def untemper(y):
    y ^= y>>18
    y ^= (y<<15)&0xEFC60000
    for _ in range(7): y ^= (y<<7)&0x9D2C5680
    for _ in range(3): y ^= y>>11
    return y&0xFFFFFFFF

def xright(bits,n):
    return [bits[k]^(bits[k+n] if k+n<32 else 0) for k in range(32)]

def xleft(bits,n,mask):
    return [bits[k]^(bits[k-n] if k>=n and (mask>>k)&1 else 0) for k in range(32)]

def tempered(bits):
    return xright(xleft(xleft(xright(bits,11),7,0x9D2C5680),15,0xEFC60000),18)

def rank(vectors):
    pivots={}
    for v in vectors:
        while v:
            k=v.bit_length()-1
            if k not in pivots:
                pivots[k]=v
                break
            v ^= pivots[k]
    return len(pivots)

def consistent(observations):
    pivots={}
    for v,b in observations:
        while v:
            k=v.bit_length()-1
            if k not in pivots:
                pivots[k]=(v,b)
                break
            old,old_bit=pivots[k]
            v ^= old
            b ^= old_bit
        else:
            if b:return False
    return True

def symbolic_words():
    states=[]
    for t in range(LO,HI+1):
        if t<LO+624:
            i=t-LO
            states.append([1<<(32*i+j) for j in range(32)])
        else:
            a=states[t-624-LO]
            b=states[t-623-LO]
            c=states[t-227-LO]
            states.append([c[j]^(b[j+1] if j<30 else a[31] if j==30 else 0)
                           ^(b[0] if MT_A>>j&1 else 0) for j in range(32)])
    return states

raw_bytes=SOURCE.read_bytes()
assert hashlib.sha256(raw_bytes).hexdigest()==EXPECTED_SHA
payloads=re.findall(rb'PAYLOAD=([0-9A-F]{32})',raw_bytes)
assert len(payloads)==133
spool={i:[untemper(v) for v in struct.unpack('<4I',bytes.fromhex(b.decode()))]
       for i,b in enumerate(payloads) if i!=129}
state=symbolic_words()
def word(t):return state[t-LO]

# Compare symbolic expressions to a separate seeded CPython MT stream.
rng=random.Random(434343)
samples=[untemper(rng.getrandbits(32)) for _ in range(HI-LO+1)]
basis=sum(1<<(32*i+j) for i,v in enumerate(samples[:624]) for j in range(32) if v>>j&1)
for t in (LO+624,LO+627,LO+800):
    predicted=sum(((linear&basis).bit_count()&1)<<j for j,linear in enumerate(word(t)))
    assert predicted==samples[t-LO],(t,predicted,samples[t-LO])
print('Independent synthetic MT recurrence controls PASS')

# Two source-linked row groups: shift d is model-conditional. The extra output
# immediately before and after each ordinary row is hypothetical CLASS/DEST.
# Treating entire 32-bit metadata words as observed gives an optimistic upper bound.
for d,p in ((11,627),(21,633),(43,655),(65,677)):
    starts={**GROUP_43,**{i:s+d for i,s in GROUP_44.items()}}
    source=[bit for i,s in starts.items() for j in range(4) for bit in word(s+j)]
    observations=[(bit,(spool[i][j]>>k)&1) for i,s in starts.items()
                  for j in range(4) for k,bit in enumerate(word(s+j))]
    assert consistent(observations), f'Contradictory source alignment at d={d}'
    top=[];full=[]
    for i,s in starts.items():
        if i not in ORDINARY:continue
        before,after=word(s-1),word(s+4)
        a,b=tempered(before),tempered(after)
        top += [a[k] for k in (29,30,31)]+[b[k] for k in (30,31)]
        full += before+after
    target=[bit for j in range(4) for bit in word(p+j)]
    r0=rank(source)
    rtop=rank(source+top)
    rfull=rank(source+full)
    t0=rank(source+target)-r0
    ttop=rank(source+top+target)-rtop
    tfull=rank(source+full+target)-rfull
    print(f'd={d:2} p={p:3}: source={r0}; with 40 sampler bits={rtop};'
          f' with 512 full metadata bits={rfull}; target freedom={t0}/{ttop}/{tfull}')
    assert (r0,rtop,rfull,t0,ttop,tfull)==(1123,1151,1442,128,128,128)
print('PASS: sampled bits and even full metadata words add zero coupon information in tested placements')
