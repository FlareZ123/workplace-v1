"""Conditional K04 donor completion: four possible coupons, often fewer under metadata.
Only the original row43/44 labels are read. The disputed row129, routing
mask, slot commitment and verifier are never read or used.
"""
import hashlib
import random
import re
import struct
import sys
import zipfile
from pathlib import Path

A = 0x9908B0DF
MASK32 = 0xFFFFFFFF
SPOOL_SHA = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"


def temper(v):
    v ^= v >> 11
    v ^= (v << 7) & 0x9D2C5680
    v ^= (v << 15) & 0xEFC60000
    return (v ^ (v >> 18)) & MASK32


def untemper(y):
    for shift, mask, left in ((18, MASK32, False), (15, 0xEFC60000, True),
                              (7, 0x9D2C5680, True), (11, MASK32, False)):
        v = y
        for _ in range(6):
            v = y ^ (((v << shift) & mask) if left else (v >> shift))
        y = v & MASK32
    return y


def twist(pre, successor):
    v = (pre & 0x80000000) | (successor & 0x7FFFFFFF)
    return (v >> 1) ^ (A if v & 1 else 0)


def candidates(last_row43_state, q_low31, middle_full, strict=False):
    """Four 31-bit successor states at X[332..335]; four full middle X[728..731].

    The first hidden draw after ordinary row43 is the DEST=bench sampler:
    tempered top2 must be 2 (accepted bench) or 3 (rejected).
    With strict=True, also require a no-extra-call gap of seven draws
    ending in row44 CLASS=STORES. This is a conditional producer model.
    """
    assert len(q_low31) == len(middle_full) == 4
    assert all(0 <= v < 0x80000000 for v in q_low31)
    first = [q_low31[0] | (b << 31) for b in (0, 1)
             if temper(q_low31[0] | (b << 31)) >> 30 in (2, 3)]
    assert len(first) == 1
    payloads = set()
    for high1 in (0, 1):
        for high2 in (0, 1):
            for high3 in ((0, 1) if strict else (0,)):
                q = [first[0], q_low31[1] | (high1 << 31),
                     q_low31[2] | (high2 << 31),
                     q_low31[3] | (high3 << 31)]
                if strict:
                    mode = "DEST"
                    valid = True
                    for word in q:
                        code = temper(word) >> 29
                        if mode == "DEST":
                            dest = code >> 1
                            if dest == 2:
                                mode = "CLASS"
                            elif dest != 3:
                                valid = False
                                break
                        elif code < 3:
                            valid = False
                            break
                    if not valid:
                        continue
                predecessor = [last_row43_state, q[0], q[1], q[2]]
                y = [temper(middle_full[j] ^ twist(predecessor[j], q[j]))
                     for j in range(4)]
                payloads.add(struct.pack("<4I", *y))
    return payloads


def original_boundary(source_zip):
    with zipfile.ZipFile(source_zip) as z:
        spool = z.read("evidence/print/spool-reconstruction.log")
    assert hashlib.sha256(spool).hexdigest() == SPOOL_SHA
    lines = [s.decode() for s in spool.splitlines() if b"PAYLOAD=" in s]
    assert len(lines) == 133
    assert "DEST=bench" in lines[43] and "CLASS=STORES" in lines[44]
    raw = bytes.fromhex(re.search(r"PAYLOAD=([0-9A-F]{32})", lines[43]).group(1))
    return untemper(struct.unpack("<4I", raw)[3])


def positive_controls():
    tested = 0
    strict_count = 0
    distribution = {}
    used = set(range(331, 339)) | set(range(728, 732)) | set(range(955, 959))
    for seed in range(25000):
        rng = random.Random(seed)
        x = {i: untemper(y)
             for i, y in enumerate(rng.getrandbits(32) for _ in range(959))
             if i in used}
        q = [x[i] for i in range(332, 339)]
        if temper(q[0]) >> 30 not in (2, 3):
            continue
        middle = [x[i] for i in range(728, 732)]
        true = struct.pack("<4I", *(temper(x[i]) for i in range(955, 959)))
        inputs = [v & 0x7FFFFFFF for v in q[:4]]
        four = candidates(x[331], inputs, middle)
        assert len(four) == 4 and true in four
        assert len({payload[:8] for payload in four}) == 1
        true_last = struct.unpack("<2I", true[8:])
        for payload in four:
            pair = struct.unpack("<2I", payload[8:])
            assert all((a ^ b) in (0, 0x44081102)
                       for a, b in zip(pair, true_last))
        tested += 1
        mode, valid = "DEST", True
        for j, v in enumerate(q):
            code = temper(v) >> 29
            if mode == "DEST":
                dest = code >> 1
                if dest == 2:
                    mode = "CLASS"
                elif dest != 3:
                    valid = False
                    break
            elif j == 6:
                if code != 1:
                    valid = False
            elif code < 3:
                valid = False
                break
        if valid and mode == "CLASS":
            reduced = candidates(x[331], inputs, middle, strict=True)
            assert true in reduced and len(reduced) in (1, 2, 4)
            distribution[len(reduced)] = distribution.get(len(reduced), 0) + 1
            strict_count += 1
    assert tested == 12616 and strict_count == 93
    assert distribution == {1: 53, 2: 30, 4: 10}
    print("synthetic valid first DEST draws:", tested)
    print("synthetic seven-draw exact row43->44 label controls:", strict_count)
    print("candidate size distribution:", distribution)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Provide the path of the untouched original H17 case ZIP.")
    assert original_boundary(Path(sys.argv[1])) >= 0
    positive_controls()
    print("K04 original target, mask and original commitments withheld.")
