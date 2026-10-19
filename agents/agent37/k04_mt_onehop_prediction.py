"""K04 source-only MT single-twist reachability; original row129 excluded."""
from pathlib import Path
from collections import defaultdict
import hashlib, re, struct, sys, zipfile
N=133
SOURCE="evidence/print/spool-reconstruction.log"
DIGEST="7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
def ur(y,n):
 x=y
 for _ in range(6):x=y^(x>>n)
 return x&0xffffffff
def ul(y,n,m):
 x=y
 for _ in range(6):x=y^((x<<n)&m)
 return x&0xffffffff
def ut(y):return ur(ul(ul(ur(y,18),15,0xefc60000),7,0x9d2c5680),11)
def tw(a,b):
 y=(a&0x80000000)|(b&0x7fffffff)
 return(y>>1)^(0x9908b0df if y&1 else 0)
def read(root):
 if root.is_file():
  with zipfile.ZipFile(root) as z:raw=z.read(SOURCE)
 else:raw=(root/SOURCE).read_bytes()
 assert hashlib.sha256(raw).hexdigest()==DIGEST
 rows=[bytes.fromhex(re.search(r"PAYLOAD=([A-F0-9]{32})",ln).group(1))
       for ln in raw.decode().splitlines() if ln.startswith("2026-")]
 assert len(rows)==N
 ws=[list(map(ut,struct.unpack("<4I",row))) for row in rows]
 ws[129]=[]
 return ws
def witnesses(ws):
 lookup=defaultdict(list)
 for r,row in enumerate(ws):
  for j,v in enumerate(row):lookup[v].append((r,j))
 out=[]
 for a,row in enumerate(ws):
  if len(row)<4:continue
  for i in range(3):
   t=tw(row[i],row[i+1])
   for b in range(a+1,N):
    for j,v in enumerate(ws[b]):
     for c,k in lookup.get(v^t,()):
      if c>b:out.append(((a,i),(b,j),(c,k)))
 return out
def closure(hits,ws,cross):
 inf=10**8
 d=[[inf]*N for _ in range(N)]
 for r in range(N):d[r][r]=0
 def eq(a,b,w):
  d[a][b]=min(d[a][b],w);d[b][a]=min(d[b][a],-w)
 for (a,i),(b,j),(c,k) in hits:
  eq(a,b,397+i-j);eq(a,c,624+i-k)
 if cross:
  for a,b,c,j,k in [(33,86,116,2,3),(40,94,125,2,0),(43,97,130,2,3)]:
   assert ws[c][k]==ws[b][j]^tw(ws[a][3],ws[a+1][0])
   eq(a,a+1,4);eq(a,b,400-j);eq(a,c,627-k)
 for r in range(1,N):d[r][r-1]=min(d[r][r-1],-4)
 for t in range(N):
  for a in range(N):
   da=d[a];at=da[t];dt=d[t]
   for b in range(N):
    if at+dt[b]<da[b]:da[b]=at+dt[b]
 assert all(d[i][i]==0 for i in range(N))
 return d
def possible(ws,d):
 count=[0]*4
 rows=set()
 for a in range(129):
  for b in range(a+1,129):
   for i in range(3):
    for k in range(4):
     v=624+i-k
     if v>d[a][129] or -v>d[129][a]:continue
     for j in range(4):
      w=397+i-j
      if w>d[a][b] or -w>d[b][a]:continue
      if v-w>d[b][129] or w-v>d[129][b]:continue
      count[k]+=1
      rows.add((a,b))
 return count,rows
def main(root):
 ws=read(root);hits=witnesses(ws);assert len(hits)==25
 base=possible(ws,closure(hits,ws,False))
 cross=possible(ws,closure(hits,ws,True))
 assert base==([12,12,12,12],{(43,96)})
 assert cross==([0,0,0,0],set())
 print("spool_sha256",DIGEST,"source_hits",len(hits),"row129_withheld",True)
 print("within_only_candidate_triples_per_target_word",base[0],"antecedent_pairs",base[1])
 print("cross_compatible_candidate_triples_per_target_word",cross[0])
 print("original_K04_hash_NOT_used")
if __name__=="__main__":main(Path(sys.argv[1]))
