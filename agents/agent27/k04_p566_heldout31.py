"""K04 p566 CPython n5 held-out inverse-twist attack (source-only SFT).

Usage: python k04_p566_heldout31.py <original-case.zip>
Standard library only. Does not read selected row129, K04 mask/commitment,
K08 caption/nonce, or the REC8 verifier. Historical stream phase is conditional.
"""
import hashlib
import random
import re
import struct
import sys
import zipfile

MASK=0xFFFFFFFF;TOP=0x80000000;LO=0x7FFFFFFF;N=5
SPOOL_HASH='7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083'
TRANSFER_HASH='32970ad4431a9d610cc12dcca2813f39dd8fd2e396f9e748dc94b5932cb69adf'
LATE=(0x6CE0E225,0xF4E8FCB2,0xC517EB25,0x7D3AAF35)
INIT=[19650218]
for i in range(1,624):INIT.append((1812433253*(INIT[-1]^(INIT[-1]>>30))+i)&MASK)

def mix(v,k):return ((v^(v>>30))*k)&MASK
def unmix(v,k):
 w=(v*pow(k,-1,1<<32))&MASK
 return w^(w>>30)
def untwist(a,b):
 z=a^b;bit=z>>31
 return (((z^(0x9908B0DF if bit else 0))<<1)|bit)&MASK
def twist(a,b):
 v=(a&TOP)|(b&LO)
 return (v>>1)^(0x9908B0DF if v&1 else 0)
def untemper(v):
 for shift,mask,left in ((18,MASK,False),(15,0xEFC60000,True),(7,0x9D2C5680,True),(11,MASK,False)):
  base=v
  for _ in range(6):v=base^(((v<<shift)&mask) if left else v>>shift)
  v&=MASK
 return v

def pair(left,right):
 values=[untwist(a,b) for a,b in zip(left,right)]
 return [(values[i]&LO)|(values[i+1]&TOP) for i in range(len(values)-1)]
def partial_key(index,a,b,c_lo,n):
 k=(index-1)%n
 first=((b+index-1)^mix(a,1566083941))&MASK
 base=INIT[index]^mix(first,1664525)
 return (((((c_lo+index)&LO)^(mix(b,1566083941)&LO))-base-k)&LO)
def prior(a,b,key,index,n):
 k=(index-1)%n
 second=(b+index)^mix(a,1566083941)
 first=unmix(INIT[index]^((second-key-k)&MASK),1664525)
 return unmix(first^((a+index-1)&MASK),1566083941)
def key_word(a,b,c,index,n):
 first=((b+index-1)^mix(a,1566083941))&MASK
 second=((c+index)^mix(b,1566083941))&MASK
 return (second-(INIT[index]^mix(first,1664525))-((index-1)%n))&MASK
def next_state(a,b,key,index,n):
 k=(index-1)%n
 first=((b+index-1)^mix(a,1566083941))&MASK
 second=((INIT[index]^mix(first,1664525))+key+k)&MASK
 return ((second^mix(b,1566083941))-index)&MASK

def infer(early,late,partial_early,partial_late,first,second):
 """Derive seed-conditioned predictions from original source-bearing runs."""
 mixed=[untwist(a,b) for a,b in zip(first,second)]
 x0=(mixed[1]&TOP)|(mixed[0]&LO)
 x1=(mixed[2]&TOP)|(mixed[1]&LO)
 x2=(mixed[3]&TOP)|(mixed[2]&LO)
 heldout_x3_lo=mixed[3]&LO
 key3_lo=partial_key(569,late[2],late[3],partial_late,N)
 phase_branches=[]
 for bit in (0,TOP):
  key3=key3_lo|bit
  s397=prior(early[0],early[1],key3,399,N)
  q0=untwist(s397,x0)
  if not q0&TOP:continue  # CPython initialized S0=0x80000000.
  q1=untwist(early[0],x1)
  q2=untwist(early[1],x2)
  s1=(q1&TOP)|(q0&LO)
  s2=(q2&TOP)|(q1&LO)
  s3_lo=q2&LO
  assert key_word(s397,*early,399,N)==key3
  for s3_top in (0,TOP):
   s3=s3_lo|s3_top
   s4=next_state(s2,s3,key3,4,N)
   x3_pred=(partial_early^twist(s3,s4))&LO
   phase_branches.append(dict(seed_key3=key3,s397=s397,s1=s1,s2=s2,
     s3=s3,s4=s4,x3_pred=x3_pred,x3_heldout=heldout_x3_lo,
     matched=x3_pred==heldout_x3_lo))
 return mixed,(x0,x1,x2,heldout_x3_lo),phase_branches

def load_source(path):
 with zipfile.ZipFile(path) as z:
  spool=z.read('evidence/print/spool-reconstruction.log')
  transfer=z.read('evidence/transfers/transfer-audit.jsonl')
 assert hashlib.sha256(spool).hexdigest()==SPOOL_HASH
 assert hashlib.sha256(transfer).hexdigest()==TRANSFER_HASH
 lines=[line for line in spool.decode().splitlines() if line.startswith('2026-')]
 assert len(lines)==133
 rows={}
 for i in (3,10,34,41,64):
  payload=re.search(r'PAYLOAD=([0-9A-F]{32})',lines[i]).group(1)
  rows[i]=[untemper(v) for v in struct.unpack('<4I',bytes.fromhex(payload))]
 return rows

def initialized_state(seed):
 words=[]
 while seed:
  words.append(seed&MASK);seed>>=32
 if not words:words=[0]
 s=INIT.copy();i=1;j=0
 for _ in range(max(624,len(words))):
  s[i]=((s[i]^mix(s[i-1],1664525))+words[j]+j)&MASK
  i+=1;j=(j+1)%len(words)
  if i==624:s[0],i=s[623],1
 for _ in range(623):
  s[i]=((s[i]^mix(s[i-1],1566083941))-i)&MASK
  i+=1
  if i==624:s[0],i=s[623],1
 s[0]=TOP
 return s

def control():
 passes=0
 for i in range(120):
  seed=sum((((0xA1245687+j*0x51317)^((i+1)*0x5A31F2F7+j*0x79CABC))&MASK)<<(32*j) for j in range(N))
  s=initialized_state(seed)
  rng=random.Random(seed)
  assert list(rng.getstate()[1][:624])==s
  x=[untemper(rng.getrandbits(32)) for _ in range(797)]
  p=566
  pre=pair(x[p:p+4],x[p+227:p+231])
  early=pair(pre,x[p-169:p-166])
  late=pair(x[p-229:p-224],x[p-2:p+3])
  tail=untwist(x[p-225],x[p+2])&LO
  source_early_low=untwist(pre[2],x[p-167])&LO
  assert early==s[398:400] and late==s[565:569] and tail==(s[569]&LO) and source_early_low==(s[400]&LO)
  mixed,observed,branches=infer(early,late,source_early_low,tail,x[p-170:p-166],x[p+57:p+61])
  expected_key=(seed>>(32*3))&MASK
  exact=[b for b in branches if b['matched']]
  assert any(b['seed_key3']==expected_key and all(b[key]==state for key,state in (('s397',s[397]),('s1',s[1]),('s2',s[2]),('s3',s[3]),('s4',s[4]))) for b in exact),(i,exact)
  passes+=1
 print('ACTUAL_RANDOM_160BIT_SEED_CONTROL_PASS',passes)

def original(path):
 rows=load_source(path)
 pre=pair(rows[34],rows[64]); assert pre==[0xBFD3ACA1,0xEF2DD8BC,0x611914B2]
 early=pair(pre,rows[10][1:4]);assert early==[0x0A9DE247,0xFBBBB07E]
 tail=untwist(rows[3][3],rows[34][2])&LO;assert tail==0x31FD69FC
 partial_early=untwist(pre[2],rows[10][3])&LO
 assert partial_early==0x2A07F662
 mixed,observed,branches=infer(early,LATE,partial_early,tail,rows[10],rows[41])
 assert mixed==[0x348ADB23,0x324EF3E1,0x353CCDFC,0x16DF5138]
 print('ORIGINAL_REASSEMBLED_X0_X1_X2_X3_LOW',*[f'{v:08X}' for v in observed])
 print('ORIGINAL_S400_LOW31',f'{partial_early:08X}')
 for b in branches:
  print('ORIGINAL_BRANCH', ' '.join(f'{k}={v:08X}' if isinstance(v,int) and k!='matched' else f'{k}={v}' for k,v in b.items()))
 assert len(branches)==2 and not any(b['matched'] for b in branches)
 print('SOURCE_ONLY_P566_N5_EXCLUDED no_original_key_or_target_used')

if __name__=='__main__':
 if len(sys.argv)!=2:raise SystemExit('Usage: python k04_p566_heldout31.py original.zip')
 control()
 original(sys.argv[1])
