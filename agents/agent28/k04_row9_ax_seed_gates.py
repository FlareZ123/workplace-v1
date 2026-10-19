"""H17 K04 source-only conditional row9/AX initialized-state residue gates.

Run: python k04_row9_ax_seed_gates.py original-export.zip
Do not open printer row129, mask, original REC8 acceptance or K08 material.
Two independent branch assumptions: row9->10 gap 6 or gap 5; both
assume aligned AX-7778 positions 5..8 and CPython first output cycle.
"""
import hashlib
import json
import random
import re
import struct
import sys
import zipfile

U=0xffffffff
P_SHA='7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083'
T_SHA='32970ad4431a9d610cc12dcca2813f39dd8fd2e396f9e748dc94b5932cb69adf'
LATE=(0x6CE0E225,0xF4E8FCB2,0xC517EB25,0x7D3AAF35)
INITIAL=[19650218]
for i in range(1,624):
    INITIAL.append((1812433253*(INITIAL[-1]^(INITIAL[-1]>>30))+i)&U)

def untemper(y):
    x=y
    for shift,mask,left in ((18,U,False),(15,0xefc60000,True),(7,0x9d2c5680,True),(11,U,False)):
        a=x
        for _ in range(6):
            x=a^(((x<<shift)&mask) if left else (x>>shift))
        x&=U
    return x

def temper(y):
    y^=y>>11
    y^=(y<<7)&0x9d2c5680
    y^=(y<<15)&0xefc60000
    return (y^(y>>18))&U

def invpair(a,b):
    v=a^b
    return (((v^(0x9908B0DF if v>>31 else 0))<<1)|(v>>31))&U

def twist(a,b):
    v=(a&0x80000000)|(b&0x7fffffff)
    return ((v>>1)^(0x9908B0DF if v&1 else 0))&U

def ancestor(row33,row63,high16):
    mixed=[invpair(row33[i],row63[i+1]) for i in range(3)]
    results=[]
    for v,h in zip(mixed,high16):
        valid=[(v&0x7fffffff)|bit for bit in (0,0x80000000)
               if temper((v&0x7fffffff)|bit)>>16==h]
        assert len(valid)==1,(v,h,valid)
        results.append(valid[0])
    return results

def early(anc,row9,gap):
    off=gap-5
    m=[invpair(anc[i],row9[off+i]) for i in range(3)]
    return ((m[0]&0x7fffffff)|(m[1]&0x80000000),
            (m[1]&0x7fffffff)|(m[2]&0x80000000)),m[2]&0x7fffffff

def plus(a,b,c,i):
    previous=((b+i-1)^((a^(a>>30))*1566083941))&U
    current=((c+i)^((b^(b>>30))*1566083941))&U
    return (current-(INITIAL[i]^((previous^(previous>>30))*1664525)))&U

def nextplus(a,b,keyplus,i):
    previous=((b+i-1)^((a^(a>>30))*1566083941))&U
    intermediate=INITIAL[i]^((previous^(previous>>30))*1664525&U)
    current=(intermediate+keyplus)&U
    return ((current^((b^(b>>30))*1566083941))-i)&U

def last_checkpoint(ear,low,row9word3,keyplus,p):
    return [(bit,temper(row9word3^twist(low|bit,
            nextplus(ear[1],low|bit,keyplus,p-171)))>>16)
            for bit in (0,0x80000000)]

def test_synthetic():
    count=0
    for gap,lengths in ((6,(29,58,87,173,174)),(5,(43,86,172,173))):
        for n in lengths:
            seed=sum(((0x17BAD111+j*17027)&U)<<(32*j) for j in range(n))
            rng=random.Random(seed)
            state=rng.getstate()[1][:624]
            outputs=[untemper(rng.getrandbits(32)) for _ in range(850)]
            for p in (402,430,555,621):
                ax=[temper(x)>>16 for x in outputs[p-402:p-399]]
                anc=ancestor(outputs[p-6:p-2],outputs[p+220:p+224],ax)
                assert anc==outputs[p-402:p-399]
                r9=outputs[p-170-gap:p-166-gap]
                words,low=early(anc,r9,gap)
                assert words==state[p-174:p-172]
                assert low==(state[p-172]&0x7fffffff)
                if gap==6:
                    delta=173 if 173%n==0 else 174
                    expected=(plus(*state[p-1:p+2],p+1) if delta==173
                              else plus(*state[p:p+3],p+2))
                    assert expected in {plus(*words,low|bit,p-172)
                                        for bit in (0,0x80000000)}
                else:
                    delta=172 if 172%n==0 else 173
                    keyplus=(plus(*state[p-1:p+2],p+1) if delta==172
                             else plus(*state[p:p+3],p+2))
                    predicted=last_checkpoint(words,low,r9[3],keyplus,p)
                    expected=temper(outputs[p-399])>>16
                    assert expected in [h for _,h in predicted]
                count+=1
    return count

def original(path):
    with zipfile.ZipFile(path) as z:
        spool=z.read('evidence/print/spool-reconstruction.log')
        transfers=z.read('evidence/transfers/transfer-audit.jsonl')
    assert hashlib.sha256(spool).hexdigest()==P_SHA
    assert hashlib.sha256(transfers).hexdigest()==T_SHA
    rows=[ln for ln in spool.decode().splitlines() if ln.startswith('2026-')]
    assert len(rows)==133
    def row(i):
        h=re.search(r'PAYLOAD=([0-9A-F]{32})',rows[i]).group(1)
        return [untemper(w) for w in struct.unpack('<4I',bytes.fromhex(h))]
    ax=sorted((v['seq'],v['attempt'],v['checkpoint']) for ln in transfers.decode().splitlines()
              if (v:=json.loads(ln))['kind']=='CHUNK' and v['transfer']=='AX-7778')
    assert [ax[i] for i in (5,6,7,8)]==[(2,2,'1CB5'),(3,1,'AEDE'),(3,2,'C98C'),(4,1,'7CA7')]
    cps=[int.from_bytes(bytes.fromhex(ax[i][2]),'little') for i in (5,6,7,8)]
    anc=ancestor(row(33),row(63),cps[:3])
    assert anc==[0x51DA82D0,0x174C046A,0x6447255B]
    return anc,row(9),cps[3]

def main(path):
    print('CPython_positives',test_synthetic())
    anc,r9,ax8=original(path)
    print('AX_ancestors',*[f'{x:08X}' for x in anc])
    for gap,lengths in ((6,(29,58,87,173,174)),(5,(43,86,172,173))):
        words,low=early(anc,r9,gap)
        print('conditional_gap',gap,'S[p-174:p-172]',*[f'{x:08X}' for x in words],
              'S[p-172]_low31',f'{low:08X}')
        for n in lengths:
            delta=(173 if 173%n==0 else 174) if gap==6 else (172 if 172%n==0 else 173)
            hits=[]
            for p in range(402,622):
                late=(plus(*LATE[:3],p+1) if (gap==6 and delta==173 or gap==5 and delta==172)
                      else plus(*LATE[1:],p+2))
                if gap==6:
                    for bit in (0,0x80000000):
                        if plus(*words,low|bit,p-172)==late:
                            hits.append((p,bit))
                else:
                    for bit,h in last_checkpoint(words,low,r9[3],late,p):
                        if h==ax8:
                            hits.append((p,bit))
            print('n',n,'period',delta,'matches',hits,'comparisons',440)
            assert not hits
    print('row129_mask_acceptance_K08_unread',True)

if __name__=='__main__':
    if len(sys.argv)!=2:raise SystemExit('usage: python k04_row9_ax_seed_gates.py case.zip')
    main(sys.argv[1])
