"""Conditional source-only K04 row9 DEST/row10 CLASS prediction from AX8/9.

Run: python k04_gap6_ax89_metadata.py original-case.zip
Imports same-directory k04_row9_ax_seed_gates.py; never inspects row129,
acceptance, K04 mask or K08.
"""
import json
import random
import sys
import zipfile
import k04_row9_ax_seed_gates as m

def prediction(words,low,p,ax8,ax9):
    k0=m.plus(*m.LATE[:3],p+1)
    k1=m.plus(*m.LATE[1:],p+2)
    outcome=[]
    for bit in (0,0x80000000):
        s2=low|bit
        s3=m.nextplus(words[1],s2,k0,p-171)
        s4=m.nextplus(s2,s3,k1,p-170)
        h8=ax8^(m.temper(m.twist(s2,s3))>>16)
        h9=ax9^(m.temper(m.twist(s3,s4))>>16)
        outcome.append((p,bit,h8,h9,h8>>14,h9>>13))
    return outcome

def synthetic():
    hits=0
    for n in (43,86,172):
        rng=random.Random(sum(((0x17BAD111+j*17027)&m.U)<<(32*j) for j in range(n)))
        init=rng.getstate()[1][:624]
        x=[m.untemper(rng.getrandbits(32)) for _ in range(850)]
        for p in (402,430,555,621):
            early=(init[p-174],init[p-173]);low=init[p-172]&0x7fffffff
            a8=m.temper(x[p-399])>>16;a9=m.temper(x[p-398])>>16
            k0=m.plus(*init[p-1:p+2],p+1);k1=m.plus(*init[p:p+3],p+2)
            s2=init[p-172];s3=m.nextplus(early[1],s2,k0,p-171)
            s4=m.nextplus(s2,s3,k1,p-170)
            assert (s3,s4)==(init[p-171],init[p-170])
            h8=a8^(m.temper(m.twist(s2,s3))>>16)
            h9=a9^(m.temper(m.twist(s3,s4))>>16)
            assert (h8,h9)==(m.temper(x[p-172])>>16,m.temper(x[p-171])>>16)
            hits+=1
    return hits

def main(path):
    assert synthetic()==12
    anc,row9,ax8=m.original(path)
    with zipfile.ZipFile(path) as z:
        transfers=z.read('evidence/transfers/transfer-audit.jsonl').decode().splitlines()
    cp=sorted((v['seq'],v['attempt'],v['checkpoint']) for ln in transfers
              if (v:=json.loads(ln))['kind']=='CHUNK' and v['transfer']=='AX-7778')
    assert cp[9]==(4,2,'A234')
    ax9=int.from_bytes(bytes.fromhex(cp[9][2]),'little')
    early,low=m.early(anc,row9,6)
    print('synthetic_positives',12,'source_ax8_ax9',f'{ax8:04X}',f'{ax9:04X}')
    for n in (43,86,172):
        dest_matches=[];class_matches=[];joint=[]
        for p in range(402,622):
            for x in prediction(early,low,p,ax8,ax9):
                if x[4]==0:dest_matches.append(x)
                if x[5]==1:class_matches.append(x)
                if x[4]==0 and x[5]==1:joint.append(x)
        print('n',n,'dest0',len(dest_matches),'class1',len(class_matches),
              'joint',len(joint),'joint_phases',[x[0] for x in joint])

if __name__=='__main__':
    if len(sys.argv)!=2:raise SystemExit('usage: python k04_gap6_ax89_metadata.py case.zip')
    main(sys.argv[1])
