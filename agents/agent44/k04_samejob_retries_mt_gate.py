"""Original-case read-only gate: ESC-N REQUESTED retries as MT source donors.
Usage: python agents/agent44/k04_samejob_retries_mt_gate.py <unpacked-case-root>
Selected ACK row129, REC8 commitments, mask, nonce and verifier excluded.
"""
import hashlib
import re
import struct
import sys
from collections import defaultdict
from pathlib import Path

M32 = 0xFFFFFFFF
LOW = 0x7FFFFFFF
MAG = 0x9908B0DF

def undo_right(value, shift):
    x = value
    for _ in range(6):
        x = value ^ (x >> shift)
    return x & M32

def undo_left(value, shift, mask):
    x = value
    for _ in range(6):
        x = value ^ ((x << shift) & mask)
    return x & M32

def untemper(y):
    y = undo_right(y, 18)
    y = undo_left(y, 15, 0xEFC60000)
    y = undo_left(y, 7, 0x9D2C5680)
    return undo_right(y, 11)

def inverse_twist(middle, end):
    z = middle ^ end
    parity = z >> 31
    join = ((z ^ (MAG if parity else 0)) << 1) & M32
    return (join | parity) & LOW, (join >> 31) & 1

def parse(case):
    source = (case / "evidence/print/spool-reconstruction.log").read_bytes()
    assert hashlib.sha256(source).hexdigest() == "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
    rows = []
    for line in source.decode().splitlines():
        if not line.startswith("2026-"):
            continue
        fields = dict(re.findall(r"([A-Z]+)=([^\s]+)", line))
        row = {**fields, "timestamp": line.split()[0]}
        assert len(bytes.fromhex(fields["PAYLOAD"])) == 16
        rows.append(row)
    assert len(rows) == 133
    exact = [(i,r) for i,r in enumerate(rows) if r["JOB"]=="PS-261003-0417"]
    assert [(r["ATTEMPT"],r["STATE"]) for _,r in exact] == [("1","ACK"),("1","REQUESTED"),("2","ACK"),("3","REQUESTED")]
    assert [(i,r["ATTEMPT"]) for i,r in exact if r["CLASS"]=="RECOVER"] == [(128,"1"),(129,"2"),(130,"3")]
    return rows

def as_words(raw, mode):
    b = bytes.fromhex(raw)
    return tuple(untemper(int.from_bytes(b[j:j+4],mode)) for j in range(0,16,4))

def run(root):
    rows = parse(root)
    selected = [(i,r) for i,r in enumerate(rows) if r["JOB"]=="PS-261003-0417" and r["ATTEMPT"]=="2" and r["CLASS"]=="RECOVER"]
    assert len(selected) == 1
    si = selected[0][0]
    requested = [(i,r) for i,r in enumerate(rows) if r["JOB"]=="PS-261003-0417" and r["STATE"]=="REQUESTED" and r["CLASS"]=="RECOVER"]
    assert len(requested) == 2
    print("source row count",len(rows),"selected index",si,"requested rows",[(i,r["ATTEMPT"]) for i,r in requested])
    print("Selected row completely excluded from all state arrays and matches")
    intact = [(i,r) for i,r in enumerate(rows) if i!=si and r["STATE"]=="ACK"]
    print("intact ACK source rows",len(intact))
    left = []
    for i,r in intact:
        for j,w in enumerate(as_words(r["PAYLOAD"],"little")):
            left.append((i,j,w))
    fingerprint = defaultdict(list)
    for x,(i,j,middle) in enumerate(left):
        for k,l,end in left[x+1:]:
            if k==i:
                continue
            predecessor,_ = inverse_twist(middle,end)
            fingerprint[predecessor].append(((i,j),(k,l)))
    print("ordered cross-row pair count",sum(len(v) for v in fingerprint.values()),"unique low31 predecessors",len(fingerprint))
    full = {i:as_words(r["PAYLOAD"],"little") for i,r in intact}
    low,_ = inverse_twist(full[7][3],full[38][0])
    assert low == (0xBBC259FD & LOW)
    print("TRP2 record26 known original positive precursor PASS",hex(low))
    for i,r in requested:
        for mode in ("little","big"):
            words = as_words(r["PAYLOAD"],mode)
            hits = [(j,hex(z),fingerprint[z & LOW][:4]) for j,z in enumerate(words) if (z & LOW) in fingerprint]
            print("retry",r["ATTEMPT"],"orientation",mode,"four source low31 predecessor matches",len(hits),hits)
    binary = (root / "evidence/recorder/trip-recorder.raw").read_bytes()
    assert binary[:8] == b"TRP2DUMP"
    version,size,count = struct.unpack_from("<HHI",binary,8)
    assert size==24 and len(binary)==16+size*count
    control_bytes = [binary[16+i*size+12:16+i*size+16] for i in range(count)]
    assert len(control_bytes)==88
    procedure = (root/"evidence/procedures/RC-17-scans.txt").read_text()
    strips = [bytes.fromhex(h) for h in re.findall(r"Footer control strip:\s*([0-9A-F]{8})",procedure)]
    assert len(strips)==12
    reference = defaultdict(list)
    for kind,vals in [("TRP2",control_bytes),("RC17",strips)]:
        for idx,raw in enumerate(vals):
            for mode in ("little","big"):
                reference[untemper(int.from_bytes(raw,mode)) & LOW].append((kind,idx,mode))
    assert inverse_twist(full[10][0],full[41][0])[0] in reference
    print("TRP2 record28 matched original intact row10/41 precursor: PASS")
    for i,r in requested:
        for mode in ("little","big"):
            words = as_words(r["PAYLOAD"],mode)
            for role in ("end","middle"):
                matches = []
                total = 0
                for j,w in enumerate(words):
                    for k,l,other in left:
                        if role=="end" and not k<i:
                            continue
                        if role=="middle" and not k>i:
                            continue
                        low,_ = inverse_twist(other,w) if role=="end" else inverse_twist(w,other)
                        total+=1
                        for source in reference.get(low,[]):
                            matches.append((j,(k,l),source))
                print("retry",r["ATTEMPT"],"orientation",mode,"role",role,"tested",total,"matches",len(matches),matches[:8])

if __name__=="__main__":
    run(Path(sys.argv[1]))
