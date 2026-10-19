"""Source-conditioned n=5 CPython 160-bit integer seed reconstruction from 3
initialized-state windows and two 31-bit edge observations. Withhold row129,
acceptance, mask and K08. Run: python k04_n5_three_window_seed.py case.zip
"""
import hashlib
import random
import re
import struct
import sys
import zipfile
from k04_ax_seed_divisor_gate import (
    MASK, LATE, SPOOL_HASH, TRANSFER_HASH, untemper, inverse_twist,
    initialized_pair, seed_word, initialized_state, source_window)

N=5

def source_rows(path):
    with zipfile.ZipFile(path) as z:
        spool=z.read('evidence/print/spool-reconstruction.log')
        transfer=z.read('evidence/transfers/transfer-audit.jsonl')
    assert hashlib.sha256(spool).hexdigest()==SPOOL_HASH
    assert hashlib.sha256(transfer).hexdigest()==TRANSFER_HASH
    lines=[line for line in spool.decode().splitlines() if line.startswith('2026-')]
    assert len(lines)==133
    def row(i):
        assert i in (3,10,34,41)
        payload=re.search(r'PAYLOAD=([0-9A-F]{32})',lines[i]).group(1)
        return [untemper(w) for w in struct.unpack('<4I',bytes.fromhex(payload))]
    return {i:row(i) for i in (3,10,34,41)}


def partial_key(i,a,b,low31,n):
    k=(i-1)%n
    first=(b+i-1)^(((a^(a>>30))*1566083941)&MASK)
    from k04_ax_seed_divisor_gate import INITIAL
    base=INITIAL[i]^(((first^(first>>30))*1664525)&MASK)
    other=((b^(b>>30))*1566083941)&MASK
    return ((((low31+i)&0x7fffffff)^(other&0x7fffffff))-base-k)&0x7fffffff


def seeds(p,early,partial_early,late,partial_late,third):
    """Yield at most four complete 5-word keys, using each source bit once."""
    values={}
    for j in (2,3):
        i=p-1+j;k=(i-1)%N
        values[k]=(seed_word(*late[j-2:j+1],i)-k)&MASK
    i=p+60;k=(i-1)%N
    assert k not in values
    values[k]=(seed_word(*third,i)-k)&MASK
    i=p-166;k=(i-1)%N
    assert k not in values
    values[k]=partial_key(i,*early,partial_early,N)
    first_partial=k
    i=p+3;k=(i-1)%N
    assert k not in values
    values[k]=partial_key(i,late[2],late[3],partial_late,N)
    second_partial=k
    assert len(values)==N
    for high1 in (0,0x80000000):
        for high2 in (0,0x80000000):
            w=values.copy()
            w[first_partial]|=high1
            w[second_partial]|=high2
            if not w[N-1]:continue
            yield sum(w[j]<<(32*j) for j in range(N))


def synthetic():
    count=0
    for p in (396,400,500,535,545,555,560,563):
        seed=sum((0xA1245687+0x51317*j)<<(32*j) for j in range(N))
        s=initialized_state(seed)
        gen=random.Random(seed)
        x=[untemper(gen.getrandbits(32)) for _ in range(p+231)]
        pre=initialized_pair(x[p:p+4],x[p+227:p+231])
        e=initialized_pair(pre,x[p-169:p-166])
        pe=inverse_twist(pre[2],x[p-167])&0x7fffffff
        l=initialized_pair(x[p-229:p-224],x[p-2:p+3])
        pl=inverse_twist(x[p-225],x[p+2])&0x7fffffff
        t=initialized_pair(x[p-170:p-166],x[p+57:p+61])
        assert e==s[p-168:p-166] and l==s[p-1:p+3]
        assert t==s[p+58:p+61]
        assert pl==s[p+3]&0x7fffffff and pe==s[p-166]&0x7fffffff
        candidates=list(seeds(p,e,pe,l,pl,t))
        assert len(candidates)==4 and seed in candidates,(p,len(candidates))
        surviving=[v for v in candidates if initialized_state(v)==s]
        assert surviving==[seed]
        count+=1
    print('SYNTHETIC_N5_EXACT_RECOVERY_PASS',count)


def original(path):
    rows=source_rows(path)
    early,pe=source_window(path)
    late=LATE
    pl=inverse_twist(rows[3][3],rows[34][2])&0x7fffffff
    third=initialized_pair(rows[10],rows[41])
    assert pl==0x31FD69FC
    assert third==[0x348ADB23,0x324EF3E1,0x353CCDFC]
    print('SOURCE_LATE_NEXT_LOW31',f'{pl:08X}')
    print('SOURCE_THIRD_WINDOW',*[f'{v:08X}' for v in third])
    candidate_count=0
    triple_matches=[]
    holdout_matches=[]
    # Third initialized-state window S[p+58:p+61] must stay within first cycle.
    for p in range(396,564):
        for seed in seeds(p,early,pe,late,pl,third):
            candidate_count+=1
            state=initialized_state(seed)
            if (state[p-168:p-166]==early and
                state[p-166]&0x7fffffff==pe and
                state[p-1:p+3]==late and
                state[p+3]&0x7fffffff==pl and
                state[p+58:p+61]==third):
                triple_matches.append((p,f'{seed:040X}'))
                rng=random.Random(seed)
                output=[rng.getrandbits(32) for _ in range(p+4)]
                # Held-out intact row34 fourth payload word, not in the seeded fragments.
                if untemper(output[p+3])==rows[34][3]:
                    holdout_matches.append((p,f'{seed:040X}'))
    print('ORIGINAL_PHASES',168,'N5_CANDIDATES',candidate_count)
    print('EXACT_INITIAL_STATE_WINDOW_MATCHES',triple_matches)
    print('HELDOUT_MATCHES',holdout_matches)
    print('SELECTED_ROW129_WITHHELD True, K04_K08_MISSING')

if __name__=='__main__':
    if len(sys.argv)!=2:raise SystemExit('Usage: python k04_n5_three_window_seed.py case.zip')
    synthetic()
    original(sys.argv[1])
