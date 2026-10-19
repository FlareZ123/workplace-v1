"""Read-only source-conditioned MT bridge from TRP2 node50 sequence order.

Run: python agents/agent11/k04_node50_sequence_bridge.py case-export.zip
Uses original spool and recorder only; never reads selected row129 or REC8
acceptance, route, mask, nonce, or verifier.
"""
from pathlib import Path
from zipfile import ZipFile
import hashlib
import re
import struct
import sys
import zlib

SPOOL = "evidence/print/spool-reconstruction.log"
RECORDER = "evidence/recorder/trip-recorder.raw"
SHA_SPOOL = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
SHA_REC = "5ebc6204ed773102237dd287772de96d19740e163b49b4075537d937888657ba"
MASK = 0xffffffff
TWIST = 0x9908b0df


def ur(y, shift):
    x = y
    for _ in range(6):
        x = y ^ (x >> shift)
    return x & MASK


def ul(y, shift, mask):
    x = y
    for _ in range(6):
        x = y ^ ((x << shift) & mask)
    return x & MASK


def untemper(word):
    return ur(ul(ul(ur(word, 18), 15, 0xefc60000), 7, 0x9d2c5680), 11)


def temper(word):
    word ^= word >> 11
    word ^= (word << 7) & 0x9d2c5680
    word ^= (word << 15) & 0xefc60000
    word ^= word >> 18
    return word & MASK


def twist(left, right):
    y = (left & 0x80000000) | (right & 0x7fffffff)
    return (y >> 1) ^ (TWIST if y & 1 else 0)


def printer_record(line):
    payload = bytes.fromhex(re.search(r"PAYLOAD=([0-9A-F]{32})", line).group(1))
    return [untemper(value) for value in struct.unpack("<4I", payload)]


def main(path):
    with ZipFile(path) as source:
        spool = source.read(SPOOL)
        recorder = source.read(RECORDER)
    assert hashlib.sha256(spool).hexdigest() == SHA_SPOOL
    assert hashlib.sha256(recorder).hexdigest() == SHA_REC
    lines = [line for line in spool.decode("ascii").splitlines()
             if line.startswith("2026-")]
    assert len(lines) == 133
    # Original, intact rows 7 and 38 are the only printer payload inputs.
    row7 = printer_record(lines[7])
    row38 = printer_record(lines[38])
    assert "CLASS=RECOVER" in lines[38]
    assert "DEST=bench" in lines[7]

    # node50's sequence numbers uniquely span 0..71, despite shuffled file order.
    control = {}
    for i in range(88):
        raw = recorder[16 + 24*i:16 + 24*(i+1)]
        timestamp, node, event, latch, seq, opaque, aux, crc = (
            struct.unpack("<IHBBI4sII", raw))
        if node == 50:
            assert zlib.crc32(raw[:20]) == crc
            assert seq not in control
            control[seq] = untemper(int.from_bytes(opaque, "little"))
    assert set(control) == set(range(72))

    # Previously published source anchor s38-s7=230 corresponds to
    # inverse-twist low31 alignment of control[70] with row7[3]/row38[0].
    # New hypothesis: node50 control[69..71] are neighboring MT draws
    # preceding control[70] and following it in their recorded seq order.
    k69_70 = twist(control[69], control[70])
    assert ((row7[3] ^ row38[0]) ^ k69_70) == 0
    print("ROW7_WORD3_SOURCE", f"{row7[3]:08X}")
    print("ROW7_WORD3_SEQUENCE_MODEL", f"{row38[0] ^ k69_70:08X}")
    print("ANCHOR_CAVEAT", "31 bits were already fixed by seq70 fingerprint; seq69 tests the last bit")

    # For relative positions: node50 seq68/69 lead to s38-1,
    # seq70/71 lead to s7+4. Source metadata are held out from arithmetic.
    pre38 = row7[2] ^ twist(control[68], control[69])
    post7 = row38[1] ^ twist(control[70], control[71])
    assert (pre38, post7) == (0xF1522284, 0x0E60D17D)
    assert temper(pre38) >> 29 == 2  # row38 CLASS=RECOVER
    assert temper(post7) >> 30 == 2  # row7 DEST=bench
    print("PREDICTED_ROW38_PRE_CLASS_MT", f"{pre38:08X}")
    print("ROW38_CLASS_TOP3", temper(pre38) >> 29, "RECOVER")
    print("PREDICTED_ROW7_POST_DEST_MT", f"{post7:08X}")
    print("ROW7_DEST_TOP2", temper(post7) >> 30, "bench")
    print("NODE50_SEQUENCES", len(control), "ALL_CRC_VALID")
    print("SOURCE_ONLY_NEW_WORDS", True)
    print("K04_K08_STATUS", "UNRESOLVED")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python k04_node50_sequence_bridge.py original-case.zip")
    main(Path(sys.argv[1]))
