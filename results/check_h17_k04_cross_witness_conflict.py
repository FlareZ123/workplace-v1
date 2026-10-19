"""Two exact cross-row MT identities incompatible with one chronological four-word stream.

Run: python results/check_h17_k04_cross_witness_conflict.py original-case.zip
The original source spool is read only. No acceptance hashes are used.
"""
import hashlib
import re
import struct
import sys
import zipfile
from pathlib import Path

SOURCE = "evidence/print/spool-reconstruction.log"
DIGEST = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"


def ur(y, n):
    x = y
    for _ in range(6):
        x = y ^ (x >> n)
    return x & 0xFFFFFFFF


def ul(y, n, m):
    x = y
    for _ in range(6):
        x = y ^ ((x << n) & m)
    return x & 0xFFFFFFFF


def ut(y):
    return ur(ul(ul(ur(y, 18), 15, 0xEFC60000), 7, 0x9D2C5680), 11)


def twist(a, b):
    v = (a & 0x80000000) | (b & 0x7FFFFFFF)
    return ((v >> 1) ^ (0x9908B0DF if v & 1 else 0)) & 0xFFFFFFFF


def run(source):
    if source.is_file():
        with zipfile.ZipFile(source) as archive:
            raw = archive.read(SOURCE)
    else:
        raw = (source / SOURCE).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == DIGEST
    rows = [bytes.fromhex(h.decode()) for h in re.findall(rb"PAYLOAD=([0-9A-F]{32})", raw)]
    assert len(rows) == 133
    w = [tuple(ut(v) for v in struct.unpack("<4I", row)) for row in rows]

    assert w[67][1] ^ twist(w[12][3], w[13][0]) == w[97][2]
    assert w[68][1] ^ twist(w[13][3], w[14][0]) == w[98][3]
    print("cross_row_witnesses", 2, "PASS")
    # Hypothetical stream indices: first pair 12[3],13[0] consecutive
    # requires s13=s12+4. Then first witness gives s97=s12+625,
    # second gives s98=s13+624=s12+628, hence s98-s97=3.
    assert w[97][3] != w[98][0]
    print("s98_minus_s97_if_both_are_actual_MT_recurrences", 3)
    print("observed_97_last_word", f"{w[97][3]:08X}")
    print("observed_98_first_word", f"{w[98][0]:08X}")
    print("joint_nonoverlapping_chronological_stream_model", "CONTRADICTION")
    print("K04", "UNRECOVERED")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python check_h17_k04_cross_witness_conflict.py ORIGINAL_CASE.zip")
    run(Path(sys.argv[1]))
