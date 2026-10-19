"""Source-only, two-step MT19937 low31-equivalent quartet witness SFT.

Original selected printer row129 and all original acceptance commitments are withheld.
Requires the original local 43-member case ZIP; standard library only.
"""
import hashlib, json, random, struct, re, sys, zipfile
from collections import defaultdict

MASK=0xBFFFFFFF  # all 32 bits except bit 30 (31 exact linear bits)
A=0x9908B0DF
SPOOL="evidence/print/spool-reconstruction.log"
SHA="7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"

def untemper(y):
    for direction,n,mask in [(0,18,0xffffffff),(1,15,0xefc60000),(1,7,0x9d2c5680),(0,11,0xffffffff)]:
        x=y
        for _ in range(6):
            x=y^(((x<<n)&mask) if direction else (x>>n))
        y=x&0xffffffff
    return y

def phi(w):
    b=w&0x7fffffff
    return ((b>>1)^(A if b&1 else 0))&MASK

def case_rows(case_zip):
    with zipfile.ZipFile(case_zip) as z:
        raw=z.read(SPOOL)
    assert hashlib.sha256(raw).hexdigest()==SHA
    rows=[]
    for ln in raw.splitlines():
        m=re.search(rb"PAYLOAD=([0-9A-F]{32})",ln)
        if m:
            rows.append([untemper(w) for w in struct.unpack('<4I',bytes.fromhex(m.group(1).decode()))])
    assert len(rows)==133
    rows[129]=[]
    return rows

def recover_quartets(rows):
    words=[(r,j,w) for r,group in enumerate(rows) for j,w in enumerate(group)]
    firstpairs=defaultdict(list)
    for i,(ra,ja,wa) in enumerate(words):
        for rb,jb,wb in words[i+1:]:
            if ra<rb:
                firstpairs[phi(wa)^phi(wb)].append((ra,ja,rb,jb))
    matches=[]
    for i,(rc,jc,wc) in enumerate(words):
        for rd,jd,wd in words[i+1:]:
            if rc>=rd:
                continue
            for ra,ja,rb,jb in firstpairs.get((wc^wd)&MASK,()):
                if rb<rc:
                    matches.append((ra,ja,rb,jb,rc,jc,rd,jd))
    return matches

def synthetic_control():
    rng=random.Random(20261019)
    w=[untemper(rng.getrandbits(32)) for _ in range(1400)]
    for t in range(1,450):
        assert ((w[t+850]^w[t+396])&MASK)==(phi(w[t])^phi(w[t+227]))
    print("449 independent indexed synthetic two-twist comparisons PASS")

def main(case_zip):
    synthetic_control()
    matches=recover_quartets(case_rows(case_zip))
    assert len(matches)==15, matches
    predicted_new=[
       (4,3,35,0,58,0,118,1),
       (5,3,36,0,59,1,119,3),
       (9,2,40,0,63,0,124,0),
    ]
    for q in predicted_new:
        assert q in matches
    # A 31-bit next-position original witness independent of q3's selected words:
    assert (9,3,40,1,63,1,124,1) in matches
    print("Original ordered four-word 31-bit matches:",len(matches))
    print("Three new components of quartet-based index evidence:")
    for q in predicted_new:
        a,i,b,j,c,k,d,l=q
        print(q,'index differences',(227+i-j,396+i-k,850+i-l))
    print("Independent adjacent original match:",(9,3,40,1,63,1,124,1))
    print("Source-only; no disputed selected row or original commitments read")

if __name__=="__main__":
    main(sys.argv[1])
