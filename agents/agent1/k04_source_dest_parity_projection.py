"""MT19937 symbolic coupon projector enhanced by source metadata.
Selected original spool row129 and all REC8 commitments deliberately withheld.
"""
import hashlib, random, re, struct, zipfile, json, sys

A=0x9908B0DF
MASK=0xffffffff
CLASS={'LABEL':0, 'STORES':1, 'RECOVER':2}
DEST={'store':0, 'desk':1, 'bench':2}

def temper(y):
    y^=y>>11
    y^=(y<<7)&0x9d2c5680
    y^=(y<<15)&0xefc60000
    y^=y>>18
    return y&MASK

def untemper(y):
    for shift,direction,mask in [(18,0,MASK),(15,1,0xefc60000),(7,1,0x9d2c5680),(11,0,MASK)]:
        x=y
        for _ in range(6):
            x=y^(((x<<shift)&mask) if direction else (x>>shift))
        y=x&MASK
    return y

def state_terms(n):
    w=[[1<<(32*i+b) for b in range(32)] for i in range(min(n,624))]
    for i in range(624,n):
        p,q,m=w[i-624],w[i-623],w[i-227]
        w.append([m[b]^(p[31] if b==30 else q[b+1] if b<30 else 0)^(q[0] if A>>b&1 else 0) for b in range(32)])
    return w

def bits_tempered(v):
    x=v[:]
    for left,shift,mask in [(False,11,MASK),(True,7,0x9d2c5680),(True,15,0xefc60000),(False,18,MASK)]:
        z=x[:]
        for b in range(32):
            src=b-shift if left else b+shift
            if 0<=src<32 and mask>>b&1:
                z[b]^=x[src]
        x=z
    return x

def projector(rows,starts,classes,dest_codes,dest_obs=(),add_classes=True,add_dest_invariant=True):
    if len(starts)!=133 or len(rows)!=133 or starts[0]!=0:
        raise ValueError("Need 133 ordered starts, s0=0")
    if any(starts[i+1]<starts[i]+4 for i in range(132)):
        raise ValueError("Overlapping printer blocks")
    if len(rows[129])!=0 or any(len(row)!=4 for i,row in enumerate(rows) if i!=129):
        raise ValueError("Expected 132 intact rows and missing original row129")
    terms=state_terms(starts[-1]+5)
    pivot={}
    def reduce(expr,v):
        x=(expr<<1)|(v&1)
        while x:
            k=x.bit_length()-1
            z=pivot.get(k)
            if z is None:
                return x
            x^=z
        return 0
    def add(expr,v,source):
        x=reduce(expr,v)
        if x==1:
            raise ValueError('Contradiction: '+str(source))
        if x:
            pivot[x.bit_length()-1]=x
    for r,ws in enumerate(rows):
        if r==129:
            continue
        for j,w in enumerate(ws):
            for b,expr in enumerate(terms[starts[r]+j]):
                add(expr,(w>>b)&1,('payload',r,j,b))
    rank_payload=len(pivot)
    if add_classes:
        for r in range(1,128):
            y=bits_tempered(terms[starts[r]-1])
            cls=classes[r]
            for b in range(29,32):
                add(y[b],(cls>>(b-29))&1,('class',r,b))
    rank_plus_class=len(pivot)
    if add_dest_invariant:
        for r in range(128):
            y=bits_tempered(terms[starts[r]+4])
            d=dest_codes[r]
            if d==0:
                add(y[30]^y[31],0,('dest_invariant',r))
            elif d==1:
                add(y[30],1,('dest_invariant',r))
            else:
                add(y[31],1,('dest_invariant',r))
    rank_plus_invariant=len(pivot)
    for r,d in dest_obs:
        y=bits_tempered(terms[starts[r]+4])
        for b in range(30,32):
            add(y[b],(d>>(b-30))&1,('dest',r,b))
    rank_plus_dest=len(pivot)
    known=[]
    target_basis={}
    for j in range(4):
        ww=bits_tempered(terms[starts[129]+j])
        mask=0
        val=0
        for b,e in enumerate(ww):
            z=reduce(e,0)
            if z in (0,1):
                mask|=1<<b
                val|=z<<b
            else:
                x=z>>1
                while x:
                    k=x.bit_length()-1
                    old=target_basis.get(k)
                    if old is None:
                        target_basis[k]=x
                        break
                    x^=old
        known.append((f'{mask:08X}',f'{val:08X}'))
    return {
        'payload_rank':rank_payload,
        'with_class_rank':rank_plus_class,
        'with_dest_invariant_rank':rank_plus_invariant,
        'with_dest_rank':rank_plus_dest,
        'target_unknown_rank':len(target_basis),
        'target_masks_values':known,
    }

def original_rows(zip_path):
    with zipfile.ZipFile(zip_path) as z:
        raw=z.read('evidence/print/spool-reconstruction.log')
    assert hashlib.sha256(raw).hexdigest()=='7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083'
    lines=[line for line in raw.decode().splitlines() if line.startswith('2026-')]
    rows=[];classes=[];dests=[]
    for line in lines:
        q=re.search(r'PAYLOAD=([0-9A-F]{32})',line).group(1)
        rows.append([untemper(x) for x in struct.unpack('<4I',bytes.fromhex(q))])
        classes.append(CLASS[re.search(r'CLASS=(\w+)',line).group(1)])
        dests.append(DEST[re.search(r'DEST=(\w+)',line).group(1)])
    assert len(rows)==133
    rows[129]=[]
    return rows,classes,dests

def synthetic(seed):
    rng=random.Random(seed)
    used=[]
    starts=[];rows=[];classes=[];dests=[];accepted=[]
    def draw():
        x=rng.getrandbits(32)
        used.append(untemper(x))
        return x
    for r in range(133):
        if 1<=r<128:
            while True:
                cl=draw()>>29
                if cl<3:
                    break
            classes.append(cl)
        else:
            classes.append(2)
        starts.append(len(used))
        rows.append([draw() for _ in range(4)])
        if r<128:
            j=starts[-1]+4
            while True:
                d=draw()>>30
                if d<3:
                    break
            dests.append(d)
            if j==len(used)-1:
                accepted.append((r,d))
        else:
            dests.append(0)
    vals=[[untemper(w) for w in row] for row in rows]
    actual=rows[129]
    vals[129]=[]
    return vals,starts,classes,dests,accepted,actual

if __name__=='__main__':
    for seed in [433,958,2267,2311,3142,6785,8113,8122]:
        rows,starts,classes,dest_codes,dest,actual=synthetic(seed)
        base=projector(rows,starts,classes,dest_codes,(),False,False)
        classonly=projector(rows,starts,classes,dest_codes,(),True,False)
        invariant=projector(rows,starts,classes,dest_codes,(),True,True)
        result=projector(rows,starts,classes,dest_codes,dest)
        for j,(mask,val) in enumerate(result['target_masks_values']):
            assert actual[j]&int(mask,16)==int(val,16)
        assert starts[129]=={433:946,958:949,2267:950,2311:955,3142:954,6785:953,8113:954,8122:952}[seed]
        print(seed,'selected index',starts[129],'unknown target bits',
            base['target_unknown_rank'],classonly['target_unknown_rank'],
            invariant['target_unknown_rank'],result['target_unknown_rank'],flush=True)
    if len(sys.argv)==3:
        rows,classes,dests=original_rows(sys.argv[1])
        with open(sys.argv[2],encoding='utf8') as f:
            starts=json.load(f)['row_starts']
        obs=[(r,dests[r]) for r in [53,80,82,84,92,95,96,97,98,99,116,126]]
        print('ORIGINAL',json.dumps(projector(rows,starts,classes,dests,obs),indent=2))
