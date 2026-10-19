"""K04 source-only AX row9 -> row10 CPython key-reuse heldout prediction.

Usage: python agents/agent26/k04_ax_row9_forward_bridge.py ORIGINAL_CASE_ZIP
Reads only SHA-pinned original printer spool and AX transfer. Selected row129,
K04/K08 commitments, route mask/nonce and verifier are not opened.
"""
import hashlib
import json
import random
import re
import struct
import sys
import zipfile
import k04_seven_residue_gate as core

M=core.M
TOP=0x80000000
TRANSFER='evidence/transfers/transfer-audit.jsonl'
TRANSFER_SHA='32970ad4431a9d610cc12dcca2813f39dd8fd2e396f9e748dc94b5932cb69adf'
LENGTHS=(1,3,9,19,57,171)


def temper(x):
    x^=x>>11
    x^=(x<<7)&0x9D2C5680
    x^=(x<<15)&0xEFC60000
    return (x^(x>>18))&M


def ax_ancestors(r33,r63,checkpoints):
    mixed=[core.inverse_pair(r33[j],r63[j+1]) for j in range(3)]
    result=[]
    for j,m in enumerate(mixed):
        low=m&0x7FFFFFFF
        candidates=[low|hi for hi in (0,TOP)
                    if temper(low|hi)>>16==checkpoints[j]]
        assert len(candidates)==1,(j,candidates)
        result.append(candidates[0])
    return result


def row9_fragment(ancestors,row9):
    mixed=[core.inverse_pair(ancestors[j],row9[j+1]) for j in range(3)]
    full=[(mixed[j]&0x7FFFFFFF)|(mixed[j+1]&TOP) for j in range(2)]
    return full,mixed[2]&0x7FFFFFFF


def step(a,b,index,key,residue):
    prior=((b+index-1)^core.mix(a,1566083941))&M
    first=core.BASE[index]^core.mix(prior,1664525)
    return (((first+key+residue)&M)^core.mix(b,1566083941))-index&M


def predictions(late,row9,phase,length):
    """Predict heldout S[p-168] through four known-residue updates."""
    assert 171%length==0
    prior,partial=row9
    l,tail=late
    known={}
    for offset in (0,1,2):
        i=phase+offset
        residue=(i-1)%length
        known[residue]=(core.seed_term(l[offset],l[offset+1],l[offset+2],i)-residue)&M
    i=phase+3
    residue=(i-1)%length
    partial_key=(core.seed_term(l[3],l[4],tail,i)-residue)&0x7FFFFFFF
    results=[]
    for state_high in (0,TOP):
        for key_high in (0,TOP):
            a,b=prior[1],partial|state_high
            for i in range(phase-171,phase-167):
                slot=(i-1)%length
                key=known.get(slot)
                if key is None:
                    assert slot==residue
                    key=partial_key|key_high
                a,b=b,step(a,b,i,key,slot)
            results.append(b)
    return results


def positive_controls():
    count=0
    for length in LENGTHS:
        for phase in (402,445,535,563,564,566,590,620):
            for trial in range(3):
                seed=sum((((0xA716E19A+j*0x9E3779B9+trial*0x31EA6)&M)<<(32*j))
                         for j in range(length))
                state=random.Random(seed).getstate()[1][:624]
                rng=random.Random(seed)
                x=[core.untemper(rng.getrandbits(32)) for _ in range(phase+684)]
                rows={row:x[phase+offset:phase+offset+4]
                      for row,offset in core.POSITIONS.items()}
                checkpoints=[temper(x[phase-402+j])>>16 for j in range(3)]
                ancestors=ax_ancestors(rows[33],rows[63],checkpoints)
                assert ancestors==x[phase-402:phase-399]
                fragment=row9_fragment(ancestors,x[phase-176:phase-172])
                assert fragment[0]==list(state[phase-174:phase-172])
                assert fragment[1]==(state[phase-172]&0x7FFFFFFF)
                _,late,_=core.infer(rows)
                assert state[phase-168] in predictions(late,fragment,phase,length)
                count+=1
    assert count==144
    print('ACTUAL_CPYTHON_SEEDED_POSITIVES_PASS',count)


def original(zip_path):
    rows=core.read_rows(zip_path)
    with zipfile.ZipFile(zip_path) as z:
        spool=z.read(core.SOURCE)
        audit=z.read(TRANSFER)
    assert hashlib.sha256(spool).hexdigest()==core.SOURCE_SHA
    assert hashlib.sha256(audit).hexdigest()==TRANSFER_SHA
    lines=[s for s in spool.decode().splitlines() if s.startswith('2026-')]
    assert len(lines)==133
    payload=bytes.fromhex(re.search(r'PAYLOAD=([0-9A-F]{32})',lines[9]).group(1))
    row9=[core.untemper(w) for w in struct.unpack('<4I',payload)]
    chunks=sorted(
        (obj for line in audit.decode().splitlines()
         if (obj:=json.loads(line)).get('kind')=='CHUNK' and obj.get('transfer')=='AX-7778'),
        key=lambda rec:(int(rec['seq']),int(rec['attempt'])))
    assert len(chunks)==16
    checkpoints=[int.from_bytes(bytes.fromhex(c['checkpoint']),'little') for c in chunks[5:8]]
    ancestors=ax_ancestors(rows[33],rows[63],checkpoints)
    assert ancestors==[0x51DA82D0,0x174C046A,0x6447255B]
    fragment=row9_fragment(ancestors,row9)
    assert fragment==([0x418BDA1E,0x2E02BC3D],0x38EBB043)
    early,late,_=core.infer(rows)
    assert early[0][0]==0x0A9DE247

    print('row9_seeded_fragment',*[f'{v:08X}' for v in fragment[0]],
          'next_low31',f'{fragment[1]:08X}')
    for length in (9,19,57,171):
        matches=[phase for phase in range(402,621)
                 if early[0][0] in predictions(late,fragment,phase,length)]
        assert not matches,(length,matches)
        print('key_array_words',length,'source_phases',219,'predictions_per_phase',4,
              'matching_heldout_S_pminus168',len(matches))
    print('SELECTED_ROW129_AND_COMMITMENTS_UNREAD',True)
    print('K04_K08_NOT_RECOVERED')


if __name__=='__main__':
    if len(sys.argv)!=2:
        raise SystemExit('usage: python k04_ax_row9_forward_bridge.py original-case.zip')
    positive_controls()
    original(sys.argv[1])
