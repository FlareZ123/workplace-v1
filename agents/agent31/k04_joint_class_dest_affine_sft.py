"""SFT: test fixed 128-to-32-bit linear printer transition plus joint CLASS×DEST XOR masks.

Run: python agents/agent31/k04_joint_class_dest_affine_sft.py ORIGINAL_CASE_ZIP
Original selected ACK, every exceptional late row, K04 route and digest stay unread.
"""
import hashlib
import random
import re
import sys
import zipfile

SPOOL_SHA = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
CLASSES = ("LABEL", "STORES", "RECOVER")
DESTS = ("store", "desk", "bench")


def vector(words, t, cell):
    return sum(words[t - 4 + i] << (32 * i) for i in range(4)) | (1 << (128 + cell))


def fit(rows):
    basis = {}
    for i, (x, y) in enumerate(rows):
        certificate = 1 << i
        while x:
            pivot = x.bit_length() - 1
            if pivot not in basis:
                basis[pivot] = x, y, certificate
                break
            bx, by, bc = basis[pivot]
            x ^= bx
            y ^= by
            certificate ^= bc
        else:
            if y:
                return basis, (i, certificate, y)
    return basis, None


def predict(basis, x):
    y = 0
    while x:
        pivot = x.bit_length() - 1
        bx, by, _ = basis[pivot]
        x ^= bx
        y ^= by
    return y


def synthetic_control():
    rng = random.Random(20261029)
    columns = [rng.getrandbits(32) for _ in range(137)]
    cells = [rng.randrange(9) for _ in range(128)]
    words = [rng.getrandbits(32) for _ in range(4)]
    def linear(x):
        y = 0
        while x:
            bit = x & -x
            y ^= columns[bit.bit_length() - 1]
            x ^= bit
        return y
    for t in range(4, 512):
        words.append(linear(vector(words, t, cells[t // 4])))
    train = [(vector(words, t, cells[t // 4]), words[t]) for t in range(4, 400)]
    basis, bad = fit(train)
    assert bad is None and len(basis) == 137
    assert all(predict(basis, vector(words, t, cells[t // 4])) == words[t]
               for t in range(400, 420))
    print("SYNTHETIC_PASS: 20/20 held-out 32-bit words, rank=137")


def original(case_zip):
    with zipfile.ZipFile(case_zip) as archive:
        raw = archive.read("evidence/print/spool-reconstruction.log")
    assert hashlib.sha256(raw).hexdigest() == SPOOL_SHA
    lines = [line for line in raw.decode("ascii").splitlines()
             if line.startswith("2026-") and "+00:00" in line.split(" ", 1)[0]]
    assert len(lines) == 128
    records = [dict(re.findall(r"\b(\w+)=(\S+)", line)) for line in lines]
    cells = [CLASSES.index(row["CLASS"]) * 3 + DESTS.index(row["DEST"])
             for row in records]
    words = [int.from_bytes(bytes.fromhex(row["PAYLOAD"])[j:j + 4], "big")
             for row in records for j in (0, 4, 8, 12)]
    assert len(words) == 512
    train = [(vector(words, t, cells[t // 4]), words[t]) for t in range(4, 400)]
    basis, bad = fit(train)
    if bad is not None:
        i, certificate, delta = bad
        used = [j + 4 for j in range(i + 1) if certificate >> j & 1]
        parity = [sum(cells[t // 4] == k for t in used) % 2 for k in range(9)]
        assert parity == [0] * 9
        assert i + 4 == 139 and len(basis) == 135 and delta == 0x4E8F0710
        print("ORIGINAL_CONTRADICTION: t=139, rank=135, "
              f"witness={len(used)}, delta=0x{delta:08X}, "
              f"all 9 CLASSxDEST parities even={parity == [0]*9}")
        print("No source-supported selected coupon prediction; recovered K04 bits: 0/128")
        return
    for t in range(400, 512):
        if predict(basis, vector(words, t, cells[t // 4])) != words[t]:
            print("HELD_OUT_ORIGINAL_FAILURE at", t)
            return
    print("ORDINARY_MODEL_SURVIVED; needs independent late same-class transfer test")


if __name__ == "__main__":
    assert len(sys.argv) == 2, "Usage: python k04_joint_class_dest_affine_sft.py ORIGINAL_CASE_ZIP"
    synthetic_control()
    original(sys.argv[1])
