"""Original source AX position4 held-out gate via two-step CPython seed inversion.
Standalone companion to k04_row9_ax_seed_gates.py. No K04 row129 or digest.
"""
import json
import random
import sys
import zipfile
import k04_row9_ax_seed_gates as m
U=m.U
I1664=pow(1664525,-1,1<<32)
I1566=pow(1566083941,-1,1<<32)

def undo_mult(x,inv):
    v=(x*inv)&U
    return (v^(v>>30))&U

def previous(b,c,keyplus,i):
    current=((c+i)^((b^(b>>30))*1566083941))&U
    former=undo_mult(m.INITIAL[i]^((current-keyplus)&U),I1664)
    return undo_mult(former^((b+i-1)&U),I1566)

def predicted(words,p,k0,k1,row9word0):
    older1=previous(words[0],words[1],k1,p-173)  # S[p-175]
    older2=previous(older1,words[0],k0,p-174)    # S[p-176]
    anc=row9word0^m.twist(older2,older1) # X[p-403]
    return older2,older1,m.temper(anc)>>16

def synthetic():
    tested=0
    for n in (5,7,25,35,175):
        seed=sum(((0x17BAD111+j*17027)&U)<<(32*j) for j in range(n))
        rng=random.Random(seed)
        state=rng.getstate()[1][:624]
        x=[m.untemper(rng.getrandbits(32)) for _ in range(850)]
        for p in (407,430,555,621):
            words=(state[p-174],state[p-173])
            k0=m.plus(*state[p-1:p+2],p+1)
            k1=m.plus(*state[p:p+3],p+2)
            older2,older1,high=predicted(words,p,k0,k1,x[p-176])
            assert (older2,older1)==(state[p-176],state[p-175]),(n,p)
            assert high==(m.temper(x[p-403])>>16),(n,p)
            tested+=1
    return tested

def main(path):
    print('synthetic_positives',synthetic())
    anc,row9,ax8=m.original(path)
    words,low=m.early(anc,row9,6)
    with zipfile.ZipFile(path) as z:lines=z.read('evidence/transfers/transfer-audit.jsonl').decode().splitlines()
    cp=sorted((v['seq'],v['attempt'],v['checkpoint']) for ln in lines
              if (v:=json.loads(ln))['kind']=='CHUNK' and v['transfer']=='AX-7778')
    assert cp[4]==(2,1,'368D')
    h4=int.from_bytes(bytes.fromhex(cp[4][2]),'little')
    print('ax4_heldout_high16',f'{h4:04X}','gap6_init_words',*[f'{x:08X}' for x in words])
    for n in (5,7,25,35,175):
        hits=[];nearest=16
        for p in range(403,622):
            k0=m.plus(*m.LATE[:3],p+1)
            k1=m.plus(*m.LATE[1:],p+2)
            a,b,h=predicted(words,p,k0,k1,row9[0])
            nearest=min(nearest,(h^h4).bit_count())
            if h==h4:hits.append((p,a,b))
        print('n',n,'AX4_original_matches',hits,'nearest_hamming',nearest)

if __name__=='__main__':main(sys.argv[1])
