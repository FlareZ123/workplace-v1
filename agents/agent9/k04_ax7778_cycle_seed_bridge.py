"""K04 AX-7778 two-cycle MT initialized-state inversion, source-only SFT.
Usage: python agents/agent9/k04_ax7778_cycle_seed_bridge.py EXTRACTED_CASE_DIR
Original selected row129, acceptance, verifier, K04 mask and K08 nonce excluded.
"""
import hashlib
import pathlib
import random
import re
import struct
import sys

P = pathlib.Path(sys.argv[1])
MASK = 0xffffffff
sha = {
 "evidence/print/spool-reconstruction.log": "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083",
 "evidence/transfers/transfer-audit.jsonl": "32970ad4431a9d610cc12dcca2813f39dd8fd2e396f9e748dc94b5932cb69adf",
}
for name, expected in sha.items():
 assert hashlib.sha256((P/name).read_bytes()).hexdigest() == expected

def untemper(value):
 x = value
 for shift, mask, left in ((18,MASK,False),(15,0xefc60000,True),
                           (7,0x9d2c5680,True),(11,MASK,False)):
  base = x
  for _ in range(6):
   x = base ^ (((x << shift) & mask) if left else x >> shift)
  x &= MASK
 return x

def temper(x):
 x ^= x >> 11
 x ^= (x << 7) & 0x9d2c5680
 x ^= (x << 15) & 0xefc60000
 return (x ^ (x >> 18)) & MASK

def inverse_twist_pair(a,b):
 z = a ^ b
 bit = z >> 31
 return (((z ^ (0x9908b0df if bit else 0)) << 1) | bit) & MASK

def seeded_window(a,b):
 mixed = [inverse_twist_pair(x,y) for x,y in zip(a,b)]
 return [(mixed[j]&0x7fffffff)|(mixed[j+1]&0x80000000)
         for j in range(len(mixed)-1)]

def twist(high,nextword):
 y=((high&1)<<31)|(nextword&0x7fffffff)
 return ((y>>1)^(0x9908b0df if y&1 else 0))&MASK

def seeded_initial_state(seed):
 key=[]
 while seed:
  key.append(seed&MASK)
  seed >>= 32
 if not key:key=[0]
 s=[19650218]
 for i in range(1,624):
  s.append((1812433253*(s[-1]^(s[-1]>>30))+i)&MASK)
 i,j=1,0
 for _ in range(max(624,len(key))):
  s[i]=((s[i]^((s[i-1]^(s[i-1]>>30))*1664525))+key[j]+j)&MASK
  i+=1;j=(j+1)%len(key)
  if i==624:s[0]=s[623];i=1
 for _ in range(623):
  s[i]=((s[i]^((s[i-1]^(s[i-1]>>30))*1566083941))-i)&MASK
  i+=1
  if i==624:s[0]=s[623];i=1
 s[0]=0x80000000
 return s

def two_windows(data):
 # Global source coordinates are relative to first output of printer row34.
 # row34->row64=227, row10 at -170, row3 at -228.
 # Inverse row34/64 reconstructs unknown first-cycle X[-396..-394].
 x=[inverse_twist_pair(data[j],data[j+227]) for j in range(4)]
 predecessor=[(x[j]&0x7fffffff)|(x[j+1]&0x80000000)
              for j in range(3)]
 old=seeded_window([data[i] for i in range(-229,-224)],
                   [data[i] for i in range(-2,3)])
 new=seeded_window(predecessor,[data[i] for i in (-169,-168,-167)])
 return predecessor,old,new

src=(P/"evidence/print/spool-reconstruction.log").read_text()
lines=[s for s in src.splitlines() if s.startswith("2026-")]
assert len(lines)==133
positions={3:-228,10:-170,33:-6,34:0,41:57,56:166,63:220,
           64:227,86:394,94:451,116:620,125:680}
state={}
def insert(i,mask,value):
 mask &= MASK;value &= mask
 oldmask,oldvalue=state.get(i,(0,0))
 assert not ((oldvalue^value)&oldmask&mask),("contradiction",i)
 if (oldmask|mask)==oldmask:return 0
 state[i]=(oldmask|mask,oldvalue|value)
 return 1
for row,start in positions.items():
 raw=bytes.fromhex(re.search(r"PAYLOAD=([0-9A-F]{32})",lines[row]).group(1))
 for j,word in enumerate(struct.unpack("<4I",raw)):
  insert(start+j,MASK,untemper(word))
for _ in range(20):
 change=0
 for i,(mask,v) in list(state.items()):
  other=state.get(i+227)
  if mask==MASK and other and other[0]==MASK:
   m=inverse_twist_pair(v,other[1])
   change+=insert(i-397,0x80000000,m&0x80000000)
   change+=insert(i-396,0x7fffffff,m&0x7fffffff)
 for i,(mask,v) in list(state.items()):
  next_word=state.get(i+1)
  if not next_word or not mask&0x80000000 or next_word[0]&0x7fffffff!=0x7fffffff:
   continue
  t=twist(v>>31,next_word[1])
  for left,right in ((i+397,i+624),(i+624,i+397)):
   a=state.get(left)
   if a and a[0]==MASK:
    change+=insert(right,MASK,a[1]^t)
 if not change:break
needed=list(range(-229,-224))+list(range(-2,4))+list(range(-169,-166))+list(range(227,231))
assert all(i in state and state[i][0]==MASK for i in needed)
data={i:value for i,(mask,value) in state.items() if mask==MASK}
pre,a,b=two_windows(data)
assert a==[0x6ce0e225,0xf4e8fcb2,0xc517eb25,0x7d3aaf35]
assert b==[0x0a9de247,0xfbbbb07e]
print("source_sha256",sha)
print("selected_row129_withheld",True)
print("ancestor_words",*[f"{v:08X}" for v in pre])
print("existing_S[p-1:p+3]",*[f"{v:08X}" for v in a])
print("NEW_S[p-168:p-166]",*[f"{v:08X}" for v in b])
# Five independent seeded CPython cases straddling first/second output cycles.
for p in (535,555,584,605,621):
 seed=int.from_bytes(bytes(range(48)),"little")
 rng=random.Random(seed)
 output=[untemper(rng.getrandbits(32)) for _ in range(p+232)]
 indices=list(range(p-229,p-224))+list(range(p-2,p+4))+list(range(p-170,p-166))+list(range(p+227,p+231))
 d={i-p:output[i] for i in indices}
 _,first,second=two_windows(d)
 actual=seeded_initial_state(seed)
 assert first==actual[p-1:p+3] and second==actual[p-168:p-166]
print("synthetic_cycle_boundary_controls_PASS",5)
print("K04_target_bits_determined",0)
