"""K04 original-source early MT first-cycle seed-period and n5 edge SFT.

Usage: python k04_early_170_period_gate.py original-case.zip
Imports only the sibling source-pinned read-only MT helper. Uses printer rows
3,10,34,41,64 and never touches selected row129 or REC8 commitments.
"""
import random
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import k04_p566_heldout31 as h

LOW=h.LO;TOP=h.TOP;MASK=h.MASK
LENGTHS=(1,2,5,10,17,34,85,170)

def initialized_key(a,b,c,index,n):
    first=((b+index-1)^h.mix(a,1566083941))&MASK
    second=((c+index)^h.mix(b,1566083941))&MASK
    return (second-(h.INIT[index]^h.mix(first,1664525))-((index-1)%n))&MASK

def wrap_s1(s622,s623,key0,key3):
    t1=((h.INIT[1]^h.mix(h.INIT[0],1664525))+key0)&MASK
    p623=((s623+623)^h.mix(s622,1566083941))&MASK
    p1=((t1^h.mix(p623,1664525))+key3+3)&MASK
    return ((p1^h.mix(s623,1566083941))-1)&MASK

def early_witness(first,midfirst,second,midsecond):
    a=h.pair(first,second)
    b=h.pair(midfirst,midsecond)
    return a,b

def source_phase(p, row10,row41,row34,row64,late,late_next,n=5):
    mid=h.pair(row10,row41)
    mixed=[h.untwist(a,b) for a,b in zip(row34,row64)]
    if 170<=p<=393:
        after=h.pair(row34,row64)
        k1=initialized_key(*mid,p+60,n)
        k2=initialized_key(*after,p+230,n)
        return {'survives':k1==k2,'early_key':k1,'late_key':k2}
    if p==394:
        assert n==5
        s622=(mixed[0]&LOW)|(mixed[1]&TOP)
        s623=(mixed[1]&LOW)|(mixed[2]&TOP)
        x0=(mixed[2]&LOW)|(mixed[3]&TOP)
        key0=initialized_key(late[1],late[2],late[3],396,5)
        key3=initialized_key(*mid,454,5)
        s1=wrap_s1(s622,s623,key0,key3)
        possibilities=[h.untwist(late_next|msb,x0)&LOW
                       for msb in (0,TOP)
                       if h.untwist(late_next|msb,x0)&TOP]
        return {'survives':(s1&LOW) in possibilities,
                'key0':key0,'key3':key3,'s1':s1,
                's1_low_options':possibilities,
                's622':s622,'s623':s623,'x0':x0}
    if p==395:
        x0=(mixed[1]&LOW)|(mixed[2]&TOP)
        inv=h.untwist(late[3],x0)
        return {'survives':bool(inv&TOP),'x0':x0,
                's397':late[3],'inverse_first_twist':inv}
    raise ValueError('unsupported phase')

def seeded_controls():
    tested={n:0 for n in LENGTHS}
    for n in LENGTHS:
        phases=range(170,394) if n==5 else (170,228,229,290,392,393)
        for p in phases:
            trials=8 if n==5 else 3
            for trial in range(trials):
                words=[((0x9E3779B9*(trial+1)+0x1B123BB5*(j+1))&MASK) for j in range(n)]
                seed=sum(w<<(32*j) for j,w in enumerate(words))
                rng=random.Random(seed)
                state=list(rng.getstate()[1][:624]);out=[h.untemper(rng.getrandbits(32)) for _ in range(627)]
                left=out[p-170:p-166];right=out[p+57:p+61]
                first=out[p:p+4];second=out[p+227:p+231]
                result=source_phase(p,left,right,first,second,(),0,n)
                assert result['survives'],(n,p,trial,result)
                assert result['early_key']==words[(p+59)%n]
                tested[n]+=1
    print('PYTHON_SEEDED_KEY_PERIOD_CONTROLS_PASS',tested)
    boundary={394:0,395:0}
    for trial in range(120):
        n=5;words=[((0xA45131B9*(trial+1)+0x1B123BB5*(j+1))&MASK) for j in range(n)]
        seed=sum(w<<(32*j) for j,w in enumerate(words))
        rng=random.Random(seed)
        state=list(rng.getstate()[1][:624]);out=[h.untemper(rng.getrandbits(32)) for _ in range(627)]
        for p in (394,395):
            late=h.pair(out[p-229:p-224],out[p-2:p+3])
            extra=h.untwist(out[p-225],out[p+2])&LOW
            assert late==state[p-1:p+3] and extra==state[p+3]&LOW
            result=source_phase(p,out[p-170:p-166],out[p+57:p+61],out[p:p+4],out[p+227:p+231],late,extra)
            assert result['survives'],(p,trial,result)
            if p==394:
                assert result['s622']==state[622] and result['s623']==state[623]
                assert result['s1']==state[1] and result['x0']==out[0]
            if p==395:
                assert result['inverse_first_twist']&LOW == state[1]&LOW
                assert result['x0']==out[0]
            boundary[p]+=1
    print('PYTHON_SEEDED_EDGE_CONTROLS_PASS',boundary)

def original(path):
    r=h.load_source(path)
    late=h.LATE
    extra=h.untwist(r[3][3],r[34][2])&LOW
    assert extra==0x31FD69FC
    first=h.pair(r[10],r[41]);second=h.pair(r[34],r[64])
    assert first==[0x348ADB23,0x324EF3E1,0x353CCDFC]
    assert second==[0xBFD3ACA1,0xEF2DD8BC,0x611914B2]
    for n in LENGTHS:
        survivors=[p for p in range(170,394) if source_phase(p,r[10],r[41],r[34],r[64],late,extra,n)['survives']]
        assert not survivors, (n,survivors)
        print('ORIGINAL_N',n,'PERIOD170_PHASES_170_393',224,'MATCHES',len(survivors))
    for p in (394,395):
        result=source_phase(p,r[10],r[41],r[34],r[64],late,extra)
        assert not result['survives'],(p,result)
        print('ORIGINAL_EDGE_EXCLUDED',p,{k:([f'{w:08X}' for w in v] if isinstance(v,list) else (f'{v:08X}' if isinstance(v,int) and k!='survives' else v)) for k,v in result.items()})
    print('N5_CONDITIONAL_FIRST_CYCLE_ALL_PHASES_170_621_CLOSED_WITH_AGENT18_P396_621')
    print('ORIGINAL_REC8_AND_SELECTED_K04_NOT_READ')

if __name__=='__main__':
    if len(sys.argv)!=2:raise SystemExit('usage: python k04_early_170_period_gate.py original.zip')
    seeded_controls()
    original(sys.argv[1])
