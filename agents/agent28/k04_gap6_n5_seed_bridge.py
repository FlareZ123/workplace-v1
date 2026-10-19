"""Two-window exact 160-bit CPython seed algebraic reconstruction.
No selected printer row129, K04 mask, REC8 acceptance, or K08.
"""
import random
import re
import struct
import sys
import zipfile
import hashlib
import k04_row9_ax_seed_gates as m
from k04_gap6_ax4_reverse import previous

D,E,F=(0x0A9DE247,0xFBBBB07E,0x2A07F662)

def fit_phase(p,A,B,C,D,E,F,k0,k1):
    out=[]
    for bit_c in (0,0x80000000):
        c=C|bit_c
        k_early=m.plus(A,B,c,p-172)
        old_m1=previous(D,E,k_early,p-167)
        old_m2=previous(old_m1,D,k1,p-168)
        old_m3=previous(old_m2,old_m1,k0,p-169)
        for bit_f in (0,0x80000000):
            f=F|bit_f
            k_old=m.plus(D,E,f,p-166)
            pred=m.nextplus(B,c,k_old,p-171)
            if pred!=old_m3:continue
            k_missing=m.plus(c,old_m3,old_m2,p-170)
            items=((p%5,k0),((p+1)%5,k1),((p+2)%5,k_early),((p+3)%5,k_old),((p+4)%5,k_missing))
            keys=[0]*5
            for i,k in items:keys[i]=(k-i)&m.U
            seed=sum(v<<(32*i) for i,v in enumerate(keys))
            out.append((seed,bit_c,bit_f,old_m1,old_m2,old_m3))
    return out

def positives():
    for seedbase in (0x12341234,0xABCDABCD):
        seed=sum((((seedbase+0x112233*i)&m.U)<<(32*i)) for i in range(5))
        st=random.Random(seed).getstate()[1][:624]
        for p in (407,430,555,621):
            cands=fit_phase(p,st[p-174],st[p-173],st[p-172]&0x7fffffff,
                st[p-168],st[p-167],st[p-166]&0x7fffffff,
                m.plus(*st[p-1:p+2],p+1),m.plus(*st[p:p+3],p+2))
            assert any(v[0]==seed for v in cands),(seed,p,cands)
    return 8

def main(path):
    print('seeded_160bit_positives',positives())
    a,r9,ax=m.original(path)
    (A,B),C=m.early(a,r9,6)
    with zipfile.ZipFile(path) as z:
        spool=z.read('evidence/print/spool-reconstruction.log')
    assert hashlib.sha256(spool).hexdigest()==m.P_SHA
    rows=[ln for ln in spool.decode().splitlines() if ln.startswith('2026-')]
    raw=bytes.fromhex(re.search(r'PAYLOAD=([0-9A-F]{32})',rows[41]).group(1))
    row41=struct.unpack('<4I',raw)
    found=[];hits=[]
    for p in range(402,622):
        k0=m.plus(*m.LATE[:3],p+1)
        k1=m.plus(*m.LATE[1:],p+2)
        for info in fit_phase(p,A,B,C,D,E,F,k0,k1):
            found.append((p,info[:3]))
            seed=info[0]
            gen=random.Random(seed)
            for _ in range(p+57):gen.getrandbits(32)
            pred=tuple(gen.getrandbits(32) for _ in range(4))
            if pred==row41:hits.append((p,info[:3]))
    print('source_conditional_seed_completions',len(found))
    print('source_completions_detail',found[:20]);print('independent_row41_holdout_matches',hits)

if __name__=='__main__':main(sys.argv[1])
