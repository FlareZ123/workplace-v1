"""Selected-ACK-withheld TRP2/RC17 mixed-role MT recurrence source check."""
import re,struct,zlib,random
from pathlib import Path
from collections import defaultdict
E=Path(__file__).resolve().parents[2]/"resources"/"evidence"
def ut(y):
 x=y
 for _ in range(5):x=y^(x>>18)
 y=x
 for _ in range(5):x=y^((x<<15)&0xefc60000)
 y=x
 for _ in range(5):x=y^((x<<7)&0x9d2c5680)
 y=x
 for _ in range(5):x=y^(x>>11)
 return x&0xffffffff
def tw(a,b):
 return (((a&0x80000000)|(b&0x7fffffff))>>1)^(0x9908b0df if b&1 else 0)
r=random.Random(1729);w=[ut(r.getrandbits(32)) for _ in range(625)]
assert w[624]==w[397]^tw(w[0],w[1])
lines=[x for x in (E/"print/spool-reconstruction.log").read_text().splitlines() if "JOB=" in x]
assert len(lines)==133
rows=[]
for i,s in enumerate(lines):
 if i==129:rows.append(None);continue
 b=bytes.fromhex(re.search("PAYLOAD=([0-9A-F]{32})",s).group(1))
 rows.append([ut(int.from_bytes(b[4*j:4*j+4],"little")) for j in range(4)])
printer=[(i,j,x) for i,row in enumerate(rows) if row is not None for j,x in enumerate(row)]
assert len(printer)==528
raw=(E/"recorder/trip-recorder.raw").read_bytes()
assert raw[:8]==b"TRP2DUMP" and struct.unpack_from("<HHI",raw,8)==(2,24,88)
source={}
for i in range(88):
 b=raw[16+24*i:16+24*(i+1)]
 if zlib.crc32(b[:20])&0xffffffff==int.from_bytes(b[20:24],"little"):
  source["TRP2_"+str(i)]=ut(int.from_bytes(b[12:16],"little"))
assert len(source)==84
for s in (E/"procedures/RC-17-scans.txt").read_text().split("\f"):
 if "DOCUMENT RC-17" not in s:continue
 label=re.search("DOCUMENT RC-17 / REV ([^\n]+)",s).group(1)
 b=bytes.fromhex(re.search("Footer control strip: ([0-9A-F]{8})",s).group(1))
 source["RC17_"+label]=ut(int.from_bytes(b,"little"))
assert len(source)==96
lookup=defaultdict(list)
for label,v in source.items():lookup[v].append(label)
hits=[]
for i,row in enumerate(rows):
 if row is None:continue
 for j in range(3):
  t=tw(row[j],row[j+1])
  for a,b,v in printer:
   if a!=i:
    for label in lookup.get(t^v,()):hits.append((i,j,a,b,label))
print("synthetic_positive=PASS; sources=96; intact_printer=528; adjacent=396; full32_matches=",len(hits))
for x in hits:print(x)
