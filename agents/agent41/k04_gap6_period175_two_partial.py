"""K04 gap6 partial/partial CPython period-175 source test.

Usage: python agents/agent41/k04_gap6_period175_two_partial.py ORIGINAL_ZIP
Imports only Agent28's existing MT arithmetic, reconstructs every original
window from intact spool + AX 5/6/7. No AX4, AX8, selected ACK or REC8.
"""
import hashlib
import json
import random
import re
import struct
import sys
import zipfile
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"agent28"))
import k04_row9_ax_seed_gates as mt

TOP=0x80000000
LOW=0x7fffffff
LENGTHS=(5,7,25,35,175)

def source(path):
    with zipfile.ZipFile(path) as z:
        spool=z.read("evidence/print/spool-reconstruction.log")
        transfer=z.read("evidence/transfers/transfer-audit.jsonl")
    assert hashlib.sha256(spool).hexdigest()==mt.P_SHA
    assert hashlib.sha256(transfer).hexdigest()==mt.T_SHA
    rows=[s for s in spool.decode().splitlines() if s.startswith("2026-")]
    assert len(rows)==133
    def row(i):
        hexa=re.search(r"PAYLOAD=([0-9A-F]{32})",rows[i]).group(1)
        return [mt.untemper(x) for x in struct.unpack("<4I",bytes.fromhex(hexa))]
    records=sorted((v["seq"],v["attempt"],v["checkpoint"])
        for line in transfer.decode().splitlines()
        if (v:=json.loads(line))["kind"]=="CHUNK" and v["transfer"]=="AX-7778")
    assert [records[i] for i in (5,6,7)]==[
        (2,2,"1CB5"),(3,1,"AEDE"),(3,2,"C98C")]
    cps=[int.from_bytes(bytes.fromhex(records[i][2]),"little") for i in (5,6,7)]
    anc=mt.ancestor(row(33),row(63),cps)
    assert anc==[0x51da82d0,0x174c046a,0x6447255b]
    early_full,early_low=mt.early(anc,row(9),6)
    early=(*early_full,early_low)
    r3,r34=row(3),row(34)
    inv=[mt.invpair(r3[i],r34[i-1]) for i in (1,2,3)]
    late=((inv[0]&LOW)|(inv[1]&TOP),
          (inv[1]&LOW)|(inv[2]&TOP),
          inv[2]&LOW)
    assert early==(0x418bda1e,0x2e02bc3d,0x38ebb043)
    assert late==(0xc517eb25,0x7d3aaf35,0x31fd69fc)
    return early,late

def possible_terms(words,index):
    a,b,partial=words
    return {mt.plus(a,b,partial|bit,index) for bit in (0,TOP)}

def compatible(early,late,p):
    return bool(possible_terms(early,p-172) & possible_terms(late,p+3))

def seeded_controls():
    count=0
    for n in LENGTHS:
        for p in (402,403,430,535,562,620):
            for trial in range(8):
                seed=sum((((0x9e3779b9*(j+1)+0x1234567*(trial+1))&mt.U)<<(32*j)) for j in range(n))
                state=random.Random(seed).getstate()[1][:624]
                early=(state[p-174],state[p-173],state[p-172]&LOW)
                late=(state[p+1],state[p+2],state[p+3]&LOW)
                assert compatible(early,late,p),(n,p,trial)
                count+=1
    print("ACTUAL_PYTHON_SEEDED_POSITIVES_PASS",count)

def original(path):
    e,l=source(path)
    print("EARLY_STATE",*[f"{w:08X}" for w in e])
    print("LATE_STATE",*[f"{w:08X}" for w in l])
    matches=[p for p in range(402,621) if compatible(e,l,p)]
    assert not matches,matches
    for n in LENGTHS:
        print("KEY_ARRAY_N",n,"PERIOD175_FIRSTCYCLE_PHASES",219,"SURVIVORS",len(matches))
    print("K04_ACK_MASK_K08_AND_REC8_UNREAD")

if __name__=="__main__":
    assert len(sys.argv)==2
    seeded_controls()
    original(sys.argv[1])
