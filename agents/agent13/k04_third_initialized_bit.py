"""Original-source-only SFT: K04 31-bit third CPython seed-state fragment.
Usage: python k04_third_initialized_bit.py original-case.zip
Never reads selected row129, masked K04, nonce, acceptance, verifier, or known keys.
"""
import hashlib
import json
import random
import re
import struct
import sys
import zipfile

MASK = 0xffffffff
SPOOL = 'evidence/print/spool-reconstruction.log'
AUDIT = 'evidence/transfers/transfer-audit.jsonl'
PINS = {SPOOL:'7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083',
        AUDIT:'32970ad4431a9d610cc12dcca2813f39dd8fd2e396f9e748dc94b5932cb69adf'}

def untemper(y):
    for s,m,left in ((18,MASK,False),(15,0xefc60000,True),(7,0x9d2c5680,True),(11,MASK,False)):
        original=y
        for _ in range(6):
            y=original^(((y<<s)&m) if left else y>>s)
        y &= MASK
    return y

def temper(y):
    y ^= y>>11
    y ^= (y<<7)&0x9d2c5680
    y ^= (y<<15)&0xefc60000
    return (y^(y>>18))&MASK

def inverse_mixed(a,b):
    delta=a^b
    parity=delta>>31
    return (((delta^(0x9908b0df if parity else 0))<<1)|parity)&MASK

def joined_windows(a,b):
    mixed=[inverse_mixed(x,y) for x,y in zip(a,b)]
    return [(mixed[j]&0x7fffffff)|(mixed[j+1]&0x80000000)
            for j in range(len(mixed)-1)], mixed

def init_state(seed):
    key=[]
    while seed:
        key.append(seed&MASK)
        seed >>=32
    if not key:key=[0]
    s=[19650218]
    for i in range(1,624):
        s.append((1812433253*(s[-1]^(s[-1]>>30))+i)&MASK)
    i,j=1,0
    for _ in range(max(624,len(key))):
        s[i]=((s[i]^((s[i-1]^(s[i-1]>>30))*1664525))+key[j]+j)&MASK
        i+=1;j=(j+1)%len(key)
        if i==624:s[0]=s[623];i=1
    for _ in range(623):
        s[i]=((s[i]^((s[i-1]^(s[i-1]>>30))*1566083941))-i)&MASK
        i+=1
        if i==624:s[0]=s[623];i=1
    s[0]=0x80000000
    return s

INITIAL=[19650218]
for i in range(1,624):
    INITIAL.append((1812433253*(INITIAL[-1]^(INITIAL[-1]>>30))+i)&MASK)

def invert_seed_word(a,b,c,i,key_count):
    previous=((b+i-1)^((a^(a>>30))*1566083941))&MASK
    current=((c+i)^((b^(b>>30))*1566083941))&MASK
    return (current-(INITIAL[i]^((previous^(previous>>30))*1664525))
            -(i-1)%key_count)&MASK

def run(original_zip):
    with zipfile.ZipFile(original_zip) as z:
        raw={name:z.read(name) for name in PINS}
    for name,pin in PINS.items():
        assert hashlib.sha256(raw[name]).hexdigest()==pin
    lines=[line for line in raw[SPOOL].decode().splitlines() if line.startswith('2026-')]
    assert len(lines)==133
    def row(index):
        assert index!=129
        payload=re.search(r'PAYLOAD=([0-9A-F]{32})',lines[index]).group(1)
        return [untemper(x) for x in struct.unpack('<4I',bytes.fromhex(payload))]
    # Source-pinned AX-7778 recurrence geometry. The selected coupon is withheld.
    positions={3:-228,10:-170,33:-6,34:0,41:57,56:166,63:220,
               64:227,86:394,94:451,116:620,125:680}
    state={}
    def insert(i,mask,value):
        mask &=MASK;value &=mask
        previous_mask,previous_value=state.get(i,(0,0))
        assert not ((previous_value^value)&previous_mask&mask),i
        if previous_mask|mask == previous_mask:return 0
        state[i]=(previous_mask|mask,previous_value|value)
        return 1
    for r,start in positions.items():
        for j,x in enumerate(row(r)):
            insert(start+j,MASK,x)
    for _ in range(30):
        changed=0
        for i,(mask,value) in list(state.items()):
            other=state.get(i+227)
            if mask==MASK and other and other[0]==MASK:
                m=inverse_mixed(value,other[1])
                changed +=insert(i-397,0x80000000,m&0x80000000)
                changed +=insert(i-396,0x7fffffff,m&0x7fffffff)
        for i,(mask,value) in list(state.items()):
            nxt=state.get(i+1)
            if not nxt or not(mask&0x80000000) or nxt[0]&0x7fffffff !=0x7fffffff:
                continue
            y=(value&0x80000000)|(nxt[1]&0x7fffffff)
            twist=((y>>1)^(0x9908b0df if y&1 else 0))&MASK
            for left,right in ((i+397,i+624),(i+624,i+397)):
                known=state.get(left)
                if known and known[0]==MASK:
                    changed +=insert(right,MASK,known[1]^twist)
        if not changed:break
    def complete(i):
        assert state.get(i,(0,0))[0]==MASK,i
        return state[i][1]
    # Late initialized-state quartet S[p-1..p+2] and earlier 3-word predecessor.
    late,_=joined_windows([complete(i) for i in range(-229,-224)],
                          [complete(i) for i in range(-2,3)])
    first,_=joined_windows([complete(i) for i in range(0,4)],
                           [complete(i) for i in range(227,231)])
    assert late==[0x6ce0e225,0xf4e8fcb2,0xc517eb25,0x7d3aaf35]
    assert first==[0xbfd3aca1,0xef2dd8bc,0x611914b2]
    transfer=[json.loads(s) for s in raw[AUDIT].decode().splitlines()]
    chunks=sorted((x for x in transfer if x.get('kind')=='CHUNK' and
                   x.get('transfer')=='AX-7778'),key=lambda x:(x['seq'],x['attempt']))
    assert len(chunks)==16
    for j,x in enumerate(first):
        assert (temper(x)>>16)==int.from_bytes(bytes.fromhex(chunks[11+j]['checkpoint']),'little')
    # The partial third initialized-state word needs only these first three predecessors.
    original_ten=[complete(i) for i in range(-170,-166)]
    earlier,mixed=joined_windows(first,original_ten[1:])
    third_low=mixed[2]&0x7fffffff
    assert earlier==[0x0a9de247,0xfbbbb07e] and third_low==0x2a07f662
    # AX-7778 fourth checkpoint independently certifies the next predecessor high bit.
    z=inverse_mixed(complete(3),complete(230))&0x7fffffff
    check=int.from_bytes(bytes.fromhex(chunks[14]['checkpoint']),'little')
    assert [high for high in (0,0x80000000) if temper(z|high)>>16==check]==[0x80000000]
    # Independent Python synthetic controls cross first/second 624-word cycles.
    controls=0
    for key_count in (1,3,7,42,167,168,624):
        keys=[(0x90eab319^(0x12345678*j))&MASK for j in range(key_count)]
        seed=sum(word<<(32*j) for j,word in enumerate(keys))
        actual=init_state(seed)
        rng=random.Random(seed)
        generated=[untemper(rng.getrandbits(32)) for _ in range(854)]
        for p in (535,566,621):
            first_synth,_=joined_windows(generated[p:p+4],generated[p+227:p+231])
            early_synth,mix=joined_windows(first_synth,generated[p-169:p-166])
            assert early_synth==actual[p-168:p-166]
            assert mix[2]&0x7fffffff == actual[p-166]&0x7fffffff
            for i in (p-166,p+1,p+2):
                assert invert_seed_word(*actual[i-2:i+1],i,key_count)==keys[(i-1)%key_count]
            controls+=1
    # The earliest word has one missing initialized-state bit.
    aliases=[]
    for k in range(1,625):
        count=0
        for p in range(535,622):
            earlier_idx=(p-167)%k
            late_idx_a=p%k
            late_idx_b=(p+1)%k
            if earlier_idx not in (late_idx_a,late_idx_b):continue
            count+=1
            a=invert_seed_word(*late[:3],p+1,k)
            b=invert_seed_word(*late[1:],p+2,k)
            old=invert_seed_word(*earlier,third_low,p-166,k)
            if late_idx_a==late_idx_b:
                assert a!=b
            assert (a if earlier_idx==late_idx_a else b)&0x7fffffff !=old&0x7fffffff
        if count:
            assert count==87
            aliases.append(k)
    assert aliases==[1,2,3,4,6,7,8,12,14,21,24,28,42,56,84,167,168]
    print('SOURCE_PINS_OK',PINS)
    print('COUPON_ROW129_WITHHELD',True)
    print('THIRD_INITIALIZED_STATE_LOW31',f'{third_low:08X}')
    print('KEY_WORD_ALIAS_LENGTHS',aliases)
    print('ORIGINAL_PHASE_LENGTH_CHECKS',sum(87 for _ in aliases),'MATCHES',0)
    print('INDEPENDENT_SYNTHETIC_CONTROLS',controls,'PASS')
    print('K04_REMAINS_UNRESOLVED')

if __name__=='__main__':
    if len(sys.argv)!=2:
        raise SystemExit('Usage: python k04_third_initialized_bit.py original-case.zip')
    run(sys.argv[1])
