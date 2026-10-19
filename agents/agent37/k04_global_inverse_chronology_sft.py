"""Reproduce selected K04 index-945 exclusion from intact original printer words.
Original H-17 ZIP input; requires SciPy. Selected row129, route, and hashes are unused.
"""
import hashlib, math, random, re, struct, sys, zipfile
from collections import defaultdict
from scipy.optimize import milp, Bounds, LinearConstraint
from scipy.sparse import coo_matrix

SPOOL='evidence/print/spool-reconstruction.log'
SHA='7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083'
LO=0x7fffffff; HI=0x80000000; A=0x9908b0df

def ur(y,n):
 x=y
 for _ in range(6):x=y^(x>>n)
 return x&0xffffffff

def ul(y,n,m):
 x=y
 for _ in range(6):x=y^((x<<n)&m)
 return x&0xffffffff

def ut(y):return ur(ul(ul(ur(y,18),15,0xefc60000),7,0x9d2c5680),11)
def twist(a,b):
 x=(a&HI)|(b&LO)
 return ((x>>1)^(A if x&1 else 0))&0xffffffff
def inverse(y):
 bit=y>>31
 return (((y^(A if bit else 0))<<1)|bit)&0xffffffff

def source(path):
 with zipfile.ZipFile(path) as z:raw=z.read(SPOOL)
 assert hashlib.sha256(raw).hexdigest()==SHA
 lines=[x for x in raw.decode().splitlines() if x.startswith('2026-')]
 assert len(lines)==133
 words=[list(map(ut,struct.unpack('<4I',bytes.fromhex(re.search(r'PAYLOAD=([A-F0-9]{32})',x).group(1))))) for x in lines]
 words[129]=[]
 lookup=defaultdict(list)
 for r,ws in enumerate(words):
  for j,w in enumerate(ws):lookup[w].append((r,j))
 within=[];boundary=[]
 for a,ws in enumerate(words):
  for i in range(len(ws)-1):
   delta=twist(ws[i],ws[i+1])
   for b in range(a+1,133):
    for j,w in enumerate(words[b]):
     for c,k in lookup.get(delta^w,()):
      if c>b:within.append(((a,i),(b,j),(c,k)))
  if ws:
   for bit in (0,1):
    delta=twist(bit<<31,ws[0])
    for b in range(a+1,133):
     for j,w in enumerate(words[b]):
      for c,k in lookup.get(delta^w,()):
       if c>b:boundary.append((a,bit,(b,j),(c,k)))
 assert (len(within),len(boundary))==(25,17)
 return words,within,boundary

def setup(within,boundary):
 eq=[];fixed=[]
 for r in range(132):eq.append(({r+1:1,r:-1,133+r:-1},4))
 for (a,i),(b,j),(c,k) in within:
  fixed.extend(((a,b,397+i-j),(a,c,624+i-k)))
 for a,bit,(b,j),(c,k) in boundary:
  fixed.extend(((a,b,396-j),(a,c,623-k)))
 for a,b,d in fixed:eq.append(({b:1,a:-1},d))
 dist=[[float('inf')]*133 for _ in range(133)]
 for i in range(133):dist[i][i]=0
 for a,b,d in fixed:
  dist[a][b]=min(dist[a][b],d);dist[b][a]=min(dist[b][a],-d)
 for r in range(132):dist[r+1][r]=min(dist[r+1][r],-(6 if r<127 else 4))
 dist[0][129]=945;dist[129][0]=-945
 for k in range(133):
  for i in range(133):
   if dist[i][k]==float('inf'):continue
   for j in range(133):
    z=dist[i][k]+dist[k][j]
    if z<dist[i][j]:dist[i][j]=z
 assert min(dist[i][i] for i in range(133))==0
 assert max(dist[0])==967
 assert max(dist[i][i+1]-4 for i in range(132))==28
 return eq

def conflicts(rows,starts):
 at={starts[r]+j:(r,j,w) for r,ws in enumerate(rows) for j,w in enumerate(ws)}
 bad=set()
 for t,(a,i,x) in at.items():
  for step,mask in ((396,LO),(397,HI)):
   b=at.get(t+step);c=at.get(t+step+227)
   if b is None or c is None:continue
   br,j,y=b;cr,k,z=c
   if (x^inverse(y^z))&mask:bad.add((a,i,br,j,cr,k,step,step+227))
 return bad

def model(eq,cuts):
 n=265+4*len(cuts);lb=[0]*n;ub=[1500]*n
 lb[0]=ub[0]=0;lb[129]=ub[129]=945
 for r in range(127):lb[133+r]=2;ub[133+r]=64
 lb[263]=ub[263]=0
 for j in range(265,n):ub[j]=1
 rows=[];cols=[];vals=[];lower=[];upper=[]
 def add(co,l,h):
  i=len(lower);lower.append(l);upper.append(h)
  for j,v in co.items():rows.append(i);cols.append(j);vals.append(v)
 for co,z in eq:add(co,z,z)
 for ix,(a,i,b,j,c,k,d1,d2) in enumerate(sorted(cuts)):
  q=265+4*ix;f=d1+i-j;g=d2+i-k;M=3000
  add({b:1,a:-1,q:M},-math.inf,M+f-1)
  add({b:-1,a:1,q+1:M},-math.inf,M-f-1)
  add({c:1,a:-1,q+2:M},-math.inf,M+g-1)
  add({c:-1,a:1,q+3:M},-math.inf,M-g-1)
  add({q:1,q+1:1,q+2:1,q+3:1},1,math.inf)
 mat=coo_matrix((vals,(rows,cols)),shape=(len(lower),n)).tocsc()
 return milp(c=[0]*n,integrality=[1]*n,bounds=Bounds(lb,ub),constraints=LinearConstraint(mat,lower,upper),options={'time_limit':15})

def main(path):
 rng=random.Random(13579);synthetic=[ut(rng.getrandbits(32)) for _ in range(2000)]
 for t in range(1,1350):
  for step,mask in ((396,LO),(397,HI)):
   assert not (synthetic[t]^inverse(synthetic[t+step]^synthetic[t+step+227]))&mask
 words,within,boundary=source(path);eq=setup(within,boundary);cuts=set()
 print('Original spool SHA256',SHA,'original witness counts',len(within),len(boundary),'synthetic controls',2698)
 print('Test s129-s0=945 with each regular gap>=2; exact graph caps all gaps at 28')
 for iteration in range(40):
  r=model(eq,cuts)
  if r.x is None:
   assert r.status==2,r.message
   print('EXCLUDED K04 index 945; infeasible after',len(cuts),'source low31/MSB cuts in',iteration,'rounds')
   return
  starts=[round(v) for v in r.x[:133]]
  new=conflicts(words,starts)-cuts
  assert new, 'a globally consistent index assignment needs further full recurrence inspection'
  cuts.update(new)
 raise RuntimeError('Search did not complete')

if __name__=='__main__':main(sys.argv[1])
