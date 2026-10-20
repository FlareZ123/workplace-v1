"""Test original AX 16-bit low-halfword MT donor triples, excluding printer row129."""
import collections
import hashlib
import itertools
import json
import re
import sys
import zipfile
from k04_lt204_low16_bridge_sft import ancestor, temper, untemper

def main(source_zip):
    with zipfile.ZipFile(source_zip) as z:
        spool=z.read("evidence/print/spool-reconstruction.log")
        raw=z.read("evidence/transfers/transfer-audit.jsonl")
    assert hashlib.sha256(spool).hexdigest()=="7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
    assert hashlib.sha256(raw).hexdigest()=="32970ad4431a9d610cc12dcca2813f39dd8fd2e396f9e748dc94b5932cb69adf"
    data=[json.loads(line) for line in raw.splitlines()]
    triples=collections.defaultdict(list)
    for name in sorted({r["transfer"] for r in data}):
        run=sorted((r for r in data if r["kind"]=="CHUNK" and r["transfer"]==name),
                   key=lambda r:(r["seq"],r["attempt"]))
        assert len(run)==16
        for i in range(len(run)-2):
            v=[int(x["checkpoint"],16) for x in run[i:i+3]]
            for swap in (False,True):
                signature=tuple(int.from_bytes(n.to_bytes(2,"big"),"little")
                                if swap else n for n in v)
                triples[signature].append((name,i,swap))
    rows=[]
    for line in spool.splitlines()[1:]:
        b=bytes.fromhex(re.search(rb"PAYLOAD=([0-9A-F]{32})",line).group(1).decode())
        rows.append([untemper(int.from_bytes(b[k:k+4],"little")) for k in (0,4,8,12)])
    assert len(rows)==133
    rows[129]=None
    matches=[]
    windows=0
    for a in range(133):
        if rows[a] is None:continue
        for b in range(a+1,133):
            if rows[b] is None:continue
            for i in (0,1):
                for j in (0,1):
                    lows=[ancestor(rows[a][i+k],rows[b][j+k]) for k in range(3)]
                    opts=[(temper(x)&65535,temper(x|0x80000000)&65535) for x in lows]
                    windows+=1
                    for values in itertools.product(*opts):
                        if values in triples:matches.append((a,b,i,j,values,triples[values]))
    assert windows==34584
    print({"source_triples":len(triples),"windows":windows,"matches":matches})

if __name__=="__main__":
    main(sys.argv[1])
