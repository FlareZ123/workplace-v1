"""Read-only test: original 128-bit route fields as MT precursor donors.

Usage: python agents/agent8/k04_route_opaque_mt_donor_gate.py ORIGINAL_ZIP

Checks the K04 mask and K08 desk nonce's original four-byte words as either
little-/big-endian MT outputs. The 31-bit inverse-twist fingerprint is
compared against every intact original inter-row printer pair.
A real TRP2 control word (record28) is the original-source positive control.
No selected K04 row129, original acceptance digest or verifier is read.
"""
import hashlib
import json
import re
import struct
import sys
import zipfile
from collections import defaultdict
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"agent18"))
from k04_ax_31bit_seed_sieve import SHA, untemper, inverse_pair

LOW=0x7FFFFFFF


def inspect(source):
    with zipfile.ZipFile(source) as z:
        raw=z.read("evidence/print/spool-reconstruction.log")
        route=json.loads(z.read("evidence/recovery-routing.json"))
        recorder=z.read("evidence/recorder/trip-recorder.raw")
    assert hashlib.sha256(raw).hexdigest()==SHA
    lines=[s for s in raw.decode().splitlines() if s.startswith("2026-")]
    assert len(lines)==133
    rows=[
        [untemper(word) for word in struct.unpack("<4I",bytes.fromhex(
            re.search(r"PAYLOAD=([0-9A-F]{32})",line).group(1)
        ))] for line in lines
    ]
    rows[129]=[]
    observed=defaultdict(list)
    for a in range(len(rows)):
        for b in range(a+1,len(rows)):
            for j,first in enumerate(rows[a]):
                for k,second in enumerate(rows[b]):
                    low=inverse_pair(first,second)&LOW
                    observed[low].append((a,j,b,k))

    original_rec28=recorder[16+28*24+12:16+28*24+16]
    control=untemper(int.from_bytes(original_rec28,"little"))&LOW
    assert (10,0,41,0) in observed[control]
    print("TRP2_RECORD28_ORIGINAL_SOURCE_POSITIVE_CONTROL_PASS")

    carriers=(
        ("K04_mask",bytes.fromhex(route["K04"]["masked_component"])),
        ("K08_nonce",bytes.fromhex(route["K08"]["desk_nonce"])),
    )
    assert all(len(data)==16 for _,data in carriers)
    matches=[]
    tokens=0
    for label,raw16 in carriers:
        for order in ("little","big"):
            for j in range(4):
                block=raw16[4*j:4*j+4]
                low=untemper(int.from_bytes(block,order))&LOW
                tokens+=1
                for witness in observed.get(low,()):
                    matches.append((label,order,j,witness))
    print("SOURCE_PRINTER_INTERROW_PAIRS",sum(map(len,observed.values())))
    print("SOURCE_OPAQUE_FIELD_TOKENS",tokens)
    print("ORIGINAL_SOURCE_MT_PRECURSOR_MATCHES",len(matches))
    assert tokens==16 and len(matches)==0
    print("NO_NEW_INDEXED_ROUTE_DONOR; K04_K08_UNRECOVERED")


if __name__=="__main__":
    if len(sys.argv)!=2:
        raise SystemExit("usage: python k04_route_opaque_mt_donor_gate.py ORIGINAL_ZIP")
    inspect(sys.argv[1])
