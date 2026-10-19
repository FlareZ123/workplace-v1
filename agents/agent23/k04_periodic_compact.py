"""H17 K04 source-only 168-step CPython seed-word collision gate.
Run: python k04_periodic_compact.py ORIGINAL_ZIP
K04 selected row129, mask, acceptance, K08 materials never opened.
"""
import hashlib
import random
import re
import struct
import sys
import zipfile

U=0xffffffff
SPOOL_SHA='7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083'
LATE=(0x6ce0e225,0xf4e8fcb2,0xc517eb25,0x7d3aaf35)  # Agent9's source-derived four-word window

def untemper(y):
    x=y
    for shift,mask,left in ((18,U,False),(15,0xefc60000,True),(7,0x9d2c5680,True),(11,U,False)):
        a=x
        for _ in range(6):
            x=a^(((x<<shift)&mask) if left else x>>shift)
        x&=U
    return x

def inverse_pair(a,b):
    v=a^b
    return (((v^(0x9908b0df if v>>31 else 0))<<1)|(v>>31))&U

def original_early(zip_path):
    with zipfile.ZipFile(zip_path) as z:
        spool=z.read('evidence/print/spool-reconstruction.log')
    assert hashlib.sha256(spool).hexdigest()==SPOOL_SHA
    rows=[x for x in spool.decode().splitlines() if x.startswith('2026-')]
    assert len(rows)==133
    def words(row):
        line=rows[row]
        raw=bytes.fromhex(re.search(r'PAYLOAD=([0-9A-F]{32})',line).group(1))
        return [untemper(w) for w in struct.unpack('<4I',raw)]
    r10,r34,r64=map(words,(10,34,64))
    mixed=[inverse_pair(a,b) for a,b in zip(r34,r64)]
    ancestors=[(mixed[i]&0x7fffffff)|(mixed[i+1]&0x80000000) for i in range(3)]
    assert ancestors==[0xbfd3aca1,0xef2dd8bc,0x611914b2]
    m=[inverse_pair(ancestors[i],r10[i+1]) for i in range(3)]
    early=((m[0]&0x7fffffff)|(m[1]&0x80000000),
           (m[1]&0x7fffffff)|(m[2]&0x80000000))
    third_low=m[2]&0x7fffffff
    assert early==(0x0a9de247,0xfbbbb07e)
    assert third_low==0x2a07f662
    return early,third_low

INITIAL=[19650218]
for i in range(1,624):
    INITIAL.append((1812433253*(INITIAL[-1]^(INITIAL[-1]>>30))+i)&U)

def key_plus_index(a,b,c,index):
    prev=((b+index-1)^((a^(a>>30))*1566083941))&U
    curr=((c+index)^((b^(b>>30))*1566083941))&U
    return (curr-(INITIAL[index]^((prev^(prev>>30))*1664525)))&U

def synthetic():
    divisors=[n for n in range(1,169) if 168%n==0]
    for n in divisors+[167]:
        seed=int.from_bytes(bytes((17*i+53)%256 for i in range(4*n)),'little')|(1<<(32*n-1))
        s=random.Random(seed).getstate()[1][:624]
        for p in (396,400,535,555,584,605,621):
            known=key_plus_index(*(s[p:p+3] if n!=167 else s[p-1:p+2]),p+(2 if n!=167 else 1))
            choices=[key_plus_index(s[p-168],s[p-167],(s[p-166]&0x7fffffff)|bit,p-166)
                     for bit in (0,0x80000000)]
            assert known in choices,(n,p)
    return divisors

def main(zip_path):
    divisors=synthetic()
    early,low=original_early(zip_path)
    matches={}
    for delta,comparison in ((167,LATE[0:3]),(168,LATE[1:4])):
        hits=[]
        for p in range(396,622):
            known=key_plus_index(*comparison,p+delta-166)
            for bit in (0,0x80000000):
                if key_plus_index(early[0],early[1],low|bit,p-166)==known:
                    hits.append((p,bit))
        matches[delta]=hits
    assert not matches[167] and not matches[168]
    print('source_early_two',*[f'{x:08X}' for x in early])
    print('source_third_low31',f'{low:08X}')
    print('synthetic_controls_PASS',(len(divisors)+1)*7)
    print('source_phase_396_621_two_high_bits_matches',matches)
    print('CPython_integer_seed_word_lengths_excluded_if_firstcycle',divisors+[167])
    print('selected_row129_untouched_and_unread',True)

if __name__=='__main__':
    if len(sys.argv)!=2:
        raise SystemExit('usage: python k04_periodic_compact.py original.zip')
    main(sys.argv[1])
