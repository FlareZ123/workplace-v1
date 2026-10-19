"""K04 selected-ACK independent AX transfer checkpoint integrity attack.

Usage: python agents/agent9/k04_selected_ax_witness_sft.py ORIGINAL_CASE_ZIP
Original route mask, REC8 digest/nonce and verifier are deliberately not read.
"""
import collections
import hashlib
import json
import random
import re
import struct
import sys
from zipfile import ZipFile

SPOOL_SHA = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
AX_SHA = "32970ad4431a9d610cc12dcca2813f39dd8fd2e396f9e748dc94b5932cb69adf"
ALL = 0xFFFFFFFF

def right(y, shift):
    x = y
    for _ in range(6):
        x = y ^ (x >> shift)
    return x & ALL

def left(y, shift, mask):
    x = y
    for _ in range(8):
        x = y ^ ((x << shift) & mask)
    return x & ALL

def untemper(y):
    return right(left(left(right(y, 18), 15, 0xEFC60000),
                      7, 0x9D2C5680), 11)

def temper(x):
    x ^= x >> 11
    x ^= (x << 7) & 0x9D2C5680
    x ^= (x << 15) & 0xEFC60000
    return (x ^ (x >> 18)) & ALL

def inverse(z):
    bit = z >> 31
    return (((z ^ (0x9908B0DF if bit else 0)) << 1) | bit) & ALL

def twist(a, b):
    y = (a & 0x80000000) | (b & 0x7FFFFFFF)
    return (y >> 1) ^ (0x9908B0DF if y & 1 else 0)

def test(case_path):
    with ZipFile(case_path) as z:
        raw = z.read("evidence/print/spool-reconstruction.log")
        transfers_raw = z.read("evidence/transfers/transfer-audit.jsonl")
    assert hashlib.sha256(raw).hexdigest() == SPOOL_SHA
    assert hashlib.sha256(transfers_raw).hexdigest() == AX_SHA
    payloads = re.findall(rb"PAYLOAD=([A-F0-9]{32})", raw)
    assert len(payloads) == 133
    byte_rows = [bytes.fromhex(v.decode()) for v in payloads]
    words = [tuple(untemper(v) for v in struct.unpack("<4I", b))
             for b in byte_rows]
    transfer_records = [json.loads(line) for line in transfers_raw.splitlines()]
    lookup = collections.defaultdict(list)
    for transfer in ("AX-7778", "AX-7781", "AX-7782", "AX-7783"):
        items = sorted((v for v in transfer_records
                        if v.get("kind") == "CHUNK" and v["transfer"] == transfer),
                       key=lambda v: (v["seq"], v["attempt"]))
        assert len(items) == 16
        for endian in ("little", "big"):
            vals = [int.from_bytes(bytes.fromhex(v["checkpoint"]), endian)
                    for v in items]
            for position in range(14):
                lookup[tuple(vals[position:position+3])].append(
                    (transfer, endian, position)
                )

    def backwards(a, b):
        mixed = [inverse(x ^ y) for x, y in zip(words[a], words[b])]
        state = [(mixed[j] & 0x7FFFFFFF) | (mixed[j+1] & 0x80000000)
                 for j in range(3)]
        return tuple(temper(v) >> 16 for v in state)

    def forwards(a, b):
        return tuple(temper(words[b][j] ^ twist(words[a][j], words[a][j+1])) >> 16
                     for j in range(3))

    control = backwards(34, 64)
    assert ("AX-7778", "little", 11) in lookup[control]
    r = random.Random(974321)
    state = [untemper(r.getrandbits(32)) for _ in range(630)]
    assert all(temper(state[397+j] ^ twist(state[j], state[j+1])) ==
               temper(state[624+j]) for j in range(3))

    inverse_hits = [(i, lookup[backwards(129, i)]) for i in range(133)
                    if i != 129 and backwards(129, i) in lookup]
    forward_hits = [(i, lookup[forwards(129, i)]) for i in range(133)
                    if i != 129 and forwards(129, i) in lookup]
    direct_hits = []
    for endian in ("little", "big"):
        vals = [int.from_bytes(byte_rows[129][2*j:2*j+2], endian)
                for j in range(8)]
        direct_hits += [(endian, i, lookup[tuple(vals[i:i+3])])
                        for i in range(6) if tuple(vals[i:i+3]) in lookup]
    assert not inverse_hits and not forward_hits and not direct_hits
    print("ROW129_UNVERIFIED_ACK", byte_rows[129].hex().upper())
    print("SOURCE_POSITIVE_AX7778_ROW34_64", control, lookup[control])
    print("SYNTHETIC_FORWARD_MT_CONTROL_PASS")
    print("ACK_INVERSE_PAIR_TESTS", 132, "MATCHES", len(inverse_hits))
    print("ACK_FORWARD_PAIR_TESTS", 132, "MATCHES", len(forward_hits))
    print("ACK_DIRECT_HALFWORD_TESTS", 12, "MATCHES", len(direct_hits))
    print("NO_NEW_INDEXED_ACK_SOURCE_WITNESS; K04_NOT_RECOVERED")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python k04_selected_ax_witness_sft.py ORIGINAL_CASE_ZIP")
    test(sys.argv[1])
