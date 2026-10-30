"""Read-only conditional original C++ seed_seq partial-bit inverse, K04 withheld.

Run as a single test file at agents/agent47/ in workplace-v2. Uses exact
original spool and source-consistent p955 alignment. A matching donor value
is conditional source algebra, not an authenticated printer producer or K04 key.
The p955 chronology was preselected using late records and is retrospective because it was itself
chosen using r132 among recurrence witnesses; this is NOT a blind source control.
"""
import hashlib
import re
from pathlib import Path
from time import perf_counter

ROOT = Path(__file__).resolve().parents[2]
N = 624
A = 0x9908B0DF
raw = (ROOT / 'resources/evidence/print/spool-reconstruction.log').read_bytes()
assert hashlib.sha256(raw).hexdigest() == '7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083'
rows = []
for line in raw.decode().splitlines():
    if not line.startswith('2026-'):
        continue
    match = re.search(r'PAYLOAD=([0-9A-F]{32})', line)
    assert match
    payload = bytes.fromhex(match.group(1))
    rows.append([int.from_bytes(payload[i:i + 4], 'little') for i in range(0, 16, 4)])
assert len(rows) == 133

# Frozen original-source-compatible chronology, selected index row129=955.
starts = [
    0,7,15,22,30,38,44,51,67,76,84,92,99,112,120,126,132,138,144,151,
    158,165,171,179,186,192,198,205,211,218,224,230,237,243,250,260,
    268,278,285,298,305,311,318,328,339,346,352,358,364,370,376,382,
    388,394,401,407,416,423,429,436,442,456,463,474,481,489,495,507,
    515,522,530,536,543,549,563,569,576,584,590,597,604,610,617,624,
    632,638,644,650,659,665,671,679,689,697,705,714,721,733,740,747,
    753,759,766,772,783,789,796,807,813,820,826,833,839,846,853,861,
    870,876,882,888,896,906,916,922,928,934,940,946,951,955,959,963,967,
]
assert len(starts) == 133 and starts[129] == 955

# Linearized initialized 624-word register. Tempered X[k] is after its first twist.
state = [[1 << (i * 32 + b) for b in range(32)] for i in range(N)]
for k in range(max(starts) + 4):
    left, right, far = state[k], state[k + 1], state[k + 397]
    low = right[0]
    state.append([
        far[b]
        ^ (right[b + 1] if b < 30 else (left[31] if b == 30 else 0))
        ^ (low if (A >> b) & 1 else 0)
        for b in range(32)
    ])

def shift_right(v, n):
    return [v[i + n] if i + n < 32 else 0 for i in range(32)]

def shift_left_mask(v, n, mask):
    return [v[i - n] if i >= n and ((mask >> i) & 1) else 0 for i in range(32)]

def xorv(x, y):
    return [a ^ b for a, b in zip(x, y)]

def temper(v):
    x = xorv(v, shift_right(v, 11))
    x = xorv(x, shift_left_mask(x, 7, 0x9D2C5680))
    x = xorv(x, shift_left_mask(x, 15, 0xEFC60000))
    return xorv(x, shift_right(x, 18))

expr = {
    i: temper(state[624 + i])
    for i in {starts[r] + w for r in range(133) if r != 129 for w in range(4)}
}

def basis_from(exclude, row_values=rows):
    piv = {}
    contradictions = 0
    for r in range(133):
        if r in exclude:
            continue
        for w in range(4):
            bits, value = expr[starts[r] + w], row_values[r][w]
            for b, coeff in enumerate(bits):
                y = (value >> b) & 1
                while coeff:
                    p = coeff.bit_length() - 1
                    if p in piv:
                        coeff ^= piv[p][0]
                        y ^= piv[p][1]
                    else:
                        piv[p] = (coeff, y)
                        break
                else:
                    if y:
                        contradictions += 1
    return piv, contradictions

def source_value(piv, i, b):
    coeff, y = 1 << (i * 32 + b), 0
    while coeff:
        p = coeff.bit_length() - 1
        if p not in piv:
            return None
        coeff ^= piv[p][0]
        y ^= piv[p][1]
    return y

def required_indexes(s):
    """Existing source-independent sufficient dependency closure, 1..4 seed words."""
    P, Q = 306, 317
    a = [1 << i for i in range(N)]
    for k in range(2 * N - 1, N - 1, -1):
        j, r4 = k % N, a[k % N]
        a[(j + P) % N] |= r4
        a[(j + Q) % N] |= r4
        a[j] = r4 | a[(j + P) % N] | a[(j - 1) % N]
    deps = 0
    for k in range(N - 1, -1, -1):
        j, r2 = k % N, a[k % N]
        r1 = r2 if k > s else a[(j + P) % N]
        if 0 < k <= s:
            deps |= r2 | r1
        a[(j + P) % N] |= r1
        a[(j + Q) % N] |= r2
        a[j] = r1 | a[(j + P) % N] | a[(j - 1) % N]
    return [i for i in range(N) if (deps >> i) & 1]


# Source-only ordinary printer controls; all five late records, including the
# selected ESC-N 18:02 ACK, are excluded from the GF(2) observation basis.
piv,bad=basis_from({128,129,130,131,132})
assert bad==0 and len(piv)==15014
parts=[]
for i in range(N):
    bits=[source_value(piv,i,j) for j in range(32)]
    mask=sum(1<<j for j,x in enumerate(bits) if x is not None)
    value=sum(x<<j for j,x in enumerate(bits) if x is not None)
    parts.append((mask,value))
assert sum(mask.bit_count() for mask,_ in parts)==9247
assert sum(mask==0xFFFFFFFF for mask,_ in parts)==190
print("ORDINARY_SOURCE_RANK",len(piv),"FIXED_BITS",9247,"FULL_WORDS",190,flush=True)

MASK=0xFFFFFFFF
P,Q,INIT=306,317,0x8B8B8B8B
def prefix(mask):
    n=0
    while n<32 and (mask>>n)&1:n+=1
    return (1<<n)-1
def constant(v):
    return (MASK,v&MASK)
def xor(a,b):
    m=a[0]&b[0]
    return (m,(a[1]^b[1])&m)
def plus(a,b):
    m=prefix(a[0]&b[0])
    return (m,(a[1]+b[1])&m)
def minus(a,b):
    m=prefix(a[0]&b[0])
    return (m,(a[1]-b[1])&m)
def mul(a,k):
    m=prefix(a[0])
    return (m,(a[1]*k)&m)
def untwist(a):
    m,v=a
    known=value=0
    for bit in range(32):
        if bit<5:
            if ((m>>bit)&1) and ((m>>(bit+27))&1):
                known|=1<<bit
                value|=(((v>>bit)^(v>>(bit+27)))&1)<<bit
        elif (m>>bit)&1:
            known|=1<<bit
            value|=v&(1<<bit)
    return (known,value)

for seed_length in (1,2,3,4):
    state=parts.copy()
    for k in range(2*N-1,N-1,-1):
        j=k%N
        r4=state[j]
        r3=plus(r4,constant(j))
        state[(j+P)%N]=xor(state[(j+P)%N],r3)
        state[(j+Q)%N]=xor(state[(j+Q)%N],r4)
        state[j]=minus(minus(untwist(mul(r3,pow(1566083941,-1,1<<32))),
                               state[(j+P)%N]),state[(j-1)%N])
    second=sum(mask.bit_count() for mask,_ in state)
    seeds=[(0,0)]*seed_length
    contradictions=[]
    for k in range(N-1,-1,-1):
        j=k%N
        r2=state[j]
        r1=minus(r2,constant(k)) if k>seed_length else minus(state[(j+P)%N],constant(INIT))
        if 0<k<=seed_length:
            seeds[k-1]=minus(minus(r2,r1),constant(k))
        if k==0:
            delta=minus(minus(r2,r1),constant(seed_length))
            if delta[1]&delta[0]:contradictions.append(("injection",k))
        state[(j+P)%N]=minus(state[(j+P)%N],r1)
        state[(j+Q)%N]=minus(state[(j+Q)%N],r2)
        state[j]=xor(xor(untwist(mul(r1,pow(1664525,-1,1<<32))),
                           state[(j+P)%N]),state[(j-1)%N])
    first=sum(mask.bit_count() for mask,_ in state)
    seed_bits=sum(mask.bit_count() for mask,_ in seeds)
    conflicts=[i for i,(mask,value) in enumerate(state) if ((value^INIT)&mask)]
    assert (second,first,seed_bits,len(contradictions),len(conflicts))==(41,0,0,0,0)
    print("SEED_LENGTH",seed_length,"KNOWN_BITS_AFTER_PASS2",second,
          "KNOWN_BITS_AFTER_PASS1",first,"SEED_BITS",seed_bits,
          "CONFLICTS",len(conflicts),flush=True)
print("UNAUTHENTICATED_SELECTED_K04_BITS 0/128; K08_EXACT_WORDS 0",flush=True)
