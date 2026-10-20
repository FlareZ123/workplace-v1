"""Read-only source SFT. Usage: python k04_lt204_low16_bridge_sft.py original.zip."""
import zipfile, json, hashlib, re, itertools, collections, sys

def untemper(y):
    for shift, mask in ((18,None),(15,0xEFC60000),(7,0x9D2C5680),(11,None)):
        original=y
        for _ in range(6):
            y=original^((y>>shift) if mask is None else ((y<<shift)&mask))
    return y & 0xffffffff

def temper(y):
    y^=y>>11
    y^=(y<<7)&0x9D2C5680
    y^=(y<<15)&0xEFC60000
    return (y^(y>>18))&0xffffffff

def ancestor(m,e):
    x=m^e
    z=x^(0x9908B0DF if x>>31 else 0)
    return ((z<<1)|(x>>31))&0x7fffffff

def main(path):
    with zipfile.ZipFile(path) as archive:
        spool=archive.read("evidence/print/spool-reconstruction.log")
        raw=archive.read("evidence/telemetry/freeze-export.jsonl")
    assert hashlib.sha256(spool).hexdigest()=="7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
    assert hashlib.sha256(raw).hexdigest()=="3787dbd6bab3930ea5293c25a995175161a1c0d7683daad29f498026e057639f"
    data=[json.loads(s) for s in raw.splitlines()]
    rs=[r for r in data if r["tag"]=="LT-204" and r["field"]=="DIAG_WORD" and r["revision"]<=4]
    assert len(rs)==32
    runs=[]
    for rev in range(1,5):
        runs.append(sorted((r for r in rs if r["revision"]==rev),key=lambda r:r["seq"]))
    for seq in range(8):
        runs.append(sorted((r for r in rs if r["seq"]==seq),key=lambda r:r["revision"]))
    runs.extend((rs,sorted(rs,key=lambda r:(r["ts"],r["seq"],r["revision"])),
                 sorted(rs,key=lambda r:(r["seq"],r["revision"])),
                 sorted(rs,key=lambda r:(r["revision"],r["seq"]))))
    assert len(runs)==16
    signatures=set()
    for run in runs:
        for i in range(len(run)-2):
            nums=[r["value"] for r in run[i:i+3]]
            signatures.add(tuple(nums))
            signatures.add(tuple(int.from_bytes(v.to_bytes(2,"big"),"little") for v in nums))
    rows=[]
    for line in spool.splitlines()[1:]:
        b=bytes.fromhex(re.search(rb"PAYLOAD=([0-9A-F]{32})",line).group(1).decode())
        rows.append([untemper(int.from_bytes(b[i:i+4],"little")) for i in (0,4,8,12)])
    assert len(rows)==133
    rows[129]=None
    count=0
    hits=[]
    for a in range(133):
        if rows[a] is None:continue
        for b in range(a+1,133):
            if rows[b] is None:continue
            for i in (0,1):
                for j in (0,1):
                    bits=[ancestor(rows[a][i+k],rows[b][j+k]) for k in range(3)]
                    variants=[(temper(v)&65535,temper(v|0x80000000)&65535) for v in bits]
                    count+=1
                    for values in itertools.product(*variants):
                        if values in signatures:hits.append((a,b,i,j,values))
    assert count==34584
    print({"source_rows":len(rs),"signatures":len(signatures),
           "intact_printer_windows":count,"hits":hits})

if __name__=="__main__":
    main(sys.argv[1])
