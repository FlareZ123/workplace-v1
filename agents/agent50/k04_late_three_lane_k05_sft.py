"""Read-only source-pinned K04 three-lane TRP2 to late K05 holdout test.

The selected original printer row129, K04 route, mask and all REC8 commitments
are never used. The test is conditional on the published p955 chronology.
"""
import re
import struct
import hashlib
import zlib
import time
import sys
from pathlib import Path

STARTS = [0,7,15,22,30,38,44,51,67,76,84,92,99,112,120,126,132,138,144,151,158,165,171,179,186,192,198,205,211,218,224,230,237,243,250,260,268,278,285,298,305,311,318,328,339,346,352,358,364,370,376,382,388,394,401,407,416,423,429,436,442,456,463,474,481,489,495,507,515,522,530,536,543,549,563,569,576,584,590,597,604,610,617,624,632,638,644,650,659,665,671,679,689,697,705,714,721,733,740,747,753,759,766,772,783,789,796,807,813,820,826,833,839,846,853,861,870,876,882,888,896,906,916,922,928,934,940,946,951,955,959,963,967]
assert len(STARTS) == 133 and STARTS[9] == 76 and STARTS[129] == 955
MIN = -320
MAX = 2250
MAG = 0x9908B0DF
SPOOL_SHA = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
TRP_SHA = "5ebc6204ed773102237dd287772de96d19740e163b49b4075537d937888657ba"

def ur(y, shift):
    x = y
    for _ in range(6):
        x = y ^ (x >> shift)
    return x & 0xFFFFFFFF

def ul(y, shift, mask):
    x = y
    for _ in range(6):
        x = y ^ ((x << shift) & mask)
    return x & 0xFFFFFFFF

def untemper(y):
    return ur(ul(ul(ur(y, 18), 15, 0xEFC60000), 7, 0x9D2C5680), 11)

def expressions():
    states = [[1 << (32*t+b) for b in range(32)] for t in range(624)]
    for i in range(624, MAX-MIN+1):
        older, younger, middle = states[i-624], states[i-623], states[i-227]
        states.append([
            middle[b] ^ (older[31] if b == 30 else younger[b+1] if b < 30 else 0)
            ^ (younger[0] if (MAG >> b) & 1 else 0)
            for b in range(32)
        ])
    return states

class Basis:
    def __init__(self):
        self.b = {}
    def reduce(self, expr, value):
        v = (expr << 1) | (value & 1)
        while v:
            pivot = v.bit_length()-1
            previous = self.b.get(pivot)
            if previous is None:
                return v
            v ^= previous
        return 0
    def add(self, expr, bit):
        row = self.reduce(expr, bit)
        if row == 1:
            raise ValueError("Original source contradicts the conditional layout")
        if row:
            self.b[row.bit_length()-1] = row
    def predict(self, expr):
        residual = self.reduce(expr, 0)
        return residual if residual in (0, 1) else None

def main():
    root = (Path(sys.argv[1]) if len(sys.argv)>1 else
            Path(__file__).resolve().parents[2] / "resources" / "evidence")
    spool = (root / "print" / "spool-reconstruction.log").read_bytes()
    trp = (root / "recorder" / "trip-recorder.raw").read_bytes()
    assert hashlib.sha256(spool).hexdigest() == SPOOL_SHA
    assert hashlib.sha256(trp).hexdigest() == TRP_SHA
    rows = [struct.unpack("<4I", bytes.fromhex(re.search(
        rb"PAYLOAD=([0-9A-F]{32})", line).group(1).decode()))
        for line in spool.splitlines() if b"PAYLOAD=" in line]
    assert len(rows) == 133
    seq = {}
    for record in range(88):
        part = trp[16+24*record:16+24*(record+1)]
        if struct.unpack_from("<H", part, 4)[0] != 49 or part[6] != 82:
            continue
        ident = struct.unpack_from("<I", part, 8)[0]
        seq[ident] = (
            untemper(struct.unpack_from("<I", part, 12)[0]),
            zlib.crc32(part[:20]) == struct.unpack_from("<I", part, 20)[0],
        )
    assert all(seq[s][1] for s in range(300, 304))
    states = expressions()
    basis = Basis()
    # Withhold disputed row 129 entirely.
    for row, outputs in enumerate(rows):
        if row == 129:
            continue
        for j, printed in enumerate(outputs):
            value = untemper(printed)
            for bit, expr in enumerate(states[STARTS[row]+j-MIN]):
                basis.add(expr, (value >> bit) & 1)
    assert len(basis.b) == 15305
    for origin, first in ((-396, 200), (-395, 900), (-394, 990)):
        for d in range(4):
            idx = STARTS[9] + origin + 3*d
            value = seq[first+d][0]
            for bit, expr in enumerate(states[idx-MIN]):
                basis.add(expr, (value >> bit) & 1)
    assert len(basis.b) == 15433
    fixed_target = sum(basis.predict(expr) is not None
        for idx in range(955, 959) for expr in states[idx-MIN])
    assert fixed_target == 0
    predictions = []
    for idx in range(971, MAX+1):
        mask = value = 0
        for bit, expr in enumerate(states[idx-MIN]):
            guess = basis.predict(expr)
            if guess is not None:
                mask |= 1 << bit
                value |= guess << bit
        predictions.append((mask, value))
    actual = [seq[s][0] for s in range(300, 304)]
    checked = []
    for offset in range(len(predictions)-3):
        chunk = predictions[offset:offset+4]
        known = sum(mask.bit_count() for mask, _ in chunk)
        if known < 16:
            continue
        errors = sum(((observed ^ value) & mask).bit_count()
                     for observed, (mask, value) in zip(actual, chunk))
        checked.append((errors, known, 971+offset))
    assert len(checked) == 969
    assert all(errors > 0 for errors, _, _ in checked)
    positive = next(i for i in range(len(predictions)-3)
        if sum(mask.bit_count() for mask, value in predictions[i:i+4]) >= 96)
    synthetic_actual = [value for _, value in predictions[positive:positive+4]]
    assert all((value & mask) == prediction
        for value, (mask, prediction) in zip(
            synthetic_actual, predictions[positive:positive+4]))
    print("Intact printer source rank: 15305")
    print("With 12 original three-lane TRP controls: rank 15433")
    print("K04 selected word bits directly fixed: 0")
    print("Original late K05 quartet seq300..303:",
          [f"{value:08X}" for value in actual])
    print("Late contiguous quartet placements with >=16 predicted bits:",
          len(checked), "exact matches:", 0)
    print("Best mismatches (wrong bits, fixed bits, index):",
          sorted(checked)[:5])
    print("Synthetic injected contiguous quartet positive PASS at",
          971+positive)
    print("Conditional source producer alignment excluded within tested range.")
    print("Original K04 selected coupon gain remains 0/128.")

if __name__ == "__main__":
    main()
