"""Source-pinned K04 first-cycle 169/171 seed-period gate. Python 3 stdlib.
Usage: python k04_period169_171.py original.zip
Reads four intact spool rows; neither disputed row129 nor REC8 commitments.
"""
import hashlib
import random
import re
import struct
import sys
from zipfile import ZipFile

M=0xffffffff
TOP=0x80000000
LOW=0x7fffffff
A=0x9908b0df
SHA="7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
LENGTHS=(3,9,13,19,57,169,171)

def mix(x,c):
    return ((x^(x>>30))*c)&M

def unshift_right(v,n):
    x=v
    for _ in range(6): x=v^(x>>n)
    return x&M

def unshift_left(v,n,mask):
    x=v
    for _ in range(6): x=v^((x<<n)&mask)
    return x&M

def untemper(x):
    x=unshift_right(x,18)
    x=unshift_left(x,15,0xefc60000)
    x=unshift_left(x,7,0x9d2c5680)
    return unshift_right(x,11)

def inverse_mix(x,y):
    v=x^y
    bit=v>>31
    return (((v^(A if bit else 0))<<1)|bit)&M

def splice(first,second):
    parts=[inverse_mix(a,b) for a,b in zip(first,second)]
    full=[(parts[j]&LOW)|(parts[j+1]&TOP) for j in range(3)]
    return full,parts[3]&LOW

def initial_state():
    arr=[19650218]
    for i in range(1,624): arr.append((mix(arr[-1],1812433253)+i)&M)
    return arr

INIT=initial_state()

def key_term(a,b,c,i,n):
    x=((b+i-1)^mix(a,1566083941))&M
    y=((c+i)^mix(b,1566083941))&M
    return (y-(INIT[i]^mix(x,1664525))-((i-1)%n))&M

def tests(mid,late,p,n):
    mf,mp=mid
    lf,lp=late
    a={key_term(mf[1],mf[2],mp|bit,p+61,n) for bit in (0,TOP)}
    b={key_term(*lf,p+230,n)}
    out=[]
    if 169%n==0: out.append((169,bool(a&b)))
    if p<=392 and 171%n==0:
        c={key_term(*mf,p+60,n)}
        d={key_term(lf[1],lf[2],lp|bit,p+231,n) for bit in (0,TOP)}
        out.append((171,bool(c&d)))
    return out

def source(path):
    with ZipFile(path) as z: data=z.read("evidence/print/spool-reconstruction.log")
    assert hashlib.sha256(data).hexdigest()==SHA
    lines=[v for v in data.decode().splitlines() if v.startswith("2026-")]
    assert len(lines)==133
    rows={}
    for j in (10,34,41,64):
        h=re.search(r"PAYLOAD=([0-9A-F]{32})",lines[j]).group(1)
        rows[j]=[untemper(v) for v in struct.unpack("<4I",bytes.fromhex(h))]
    return splice(rows[10],rows[41]),splice(rows[34],rows[64])

def positive_controls():
    for n in LENGTHS:
        for p in (170,171,228,229,300,391,392,393):
            for trial in range(6):
                words=[(0x9e3779b9*(j+1)+0x168a9b17*(trial+1))&M for j in range(n)]
                seed=sum(v<<(32*j) for j,v in enumerate(words))
                rng=random.Random(seed)
                state=rng.getstate()[1][:624]
                output=[untemper(rng.getrandbits(32)) for _ in range(p+231)]
                mid=splice(output[p-170:p-166],output[p+57:p+61])
                late=splice(output[p:p+4],output[p+227:p+231])
                assert mid[0]==list(state[p+58:p+61]) and mid[1]==state[p+61]&LOW
                assert late[0]==list(state[p+228:p+231])
                if p<=392: assert late[1]==state[p+231]&LOW
                assert all(ok for _,ok in tests(mid,late,p,n)),(n,p,trial)
        print("SEEDED_POSITIVE_PASS",n,48)

def original(path):
    mid,late=source(path)
    assert mid==([0x348adb23,0x324ef3e1,0x353ccdfc],0x16df5138)
    assert late==([0xbfd3aca1,0xef2dd8bc,0x611914b2],0x3f44282b)
    for n in LENGTHS:
        hits={169:[],171:[]}
        for p in range(170,394):
            for distance,ok in tests(mid,late,p,n):
                if ok: hits[distance].append(p)
        for distance in (169,171):
            if distance%n==0:
                print("ORIGINAL_PERIOD",distance,"LENGTH",n,"PHASES",224 if distance==169 else 223,"SURVIVORS",len(hits[distance]))
                assert not hits[distance],(distance,n,hits[distance])
    print("SELECTED_K04_ACK_AND_REC8_NEVER_READ")

if __name__=="__main__":
    assert len(sys.argv)==2
    positive_controls()
    original(sys.argv[1])
