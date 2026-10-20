"""Source-pinned, selected-coupon-withheld three-lane TRP2 MT prediction test.

Run from the repository root (resources/) or pass the original case ZIP path.
No K04/K08 recovery commitment is read. Standard library only.
"""
import hashlib
import re
import struct
import sys
import zipfile
import zlib
from pathlib import Path

SPOOL_SHA = '7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083'
TRP_SHA = '5ebc6204ed773102237dd287772de96d19740e163b49b4075537d937888657ba'
MAG = 0x9908B0DF
BASE = -400
ROW_START = {9: 0, 40: 229, 63: 398, 124: 852}
LANES = ((200, -396), (900, -395), (990, -394))


def source_bytes(path):
    if path is None:
        root = Path(__file__).resolve().parents[2] / 'resources/evidence'
        spool = (root / 'print/spool-reconstruction.log').read_bytes()
        trp = (root / 'recorder/trip-recorder.raw').read_bytes()
    else:
        with zipfile.ZipFile(path) as z:
            spool = z.read('evidence/print/spool-reconstruction.log')
            trp = z.read('evidence/recorder/trip-recorder.raw')
    assert hashlib.sha256(spool).hexdigest() == SPOOL_SHA
    assert hashlib.sha256(trp).hexdigest() == TRP_SHA
    return spool, trp


def untemper(y):
    y ^= y >> 18
    y ^= (y << 15) & 0xEFC60000
    for _ in range(7):
        y ^= (y << 7) & 0x9D2C5680
    for _ in range(3):
        y ^= y >> 11
    return y & 0xFFFFFFFF


def equations():
    """Linear symbolic MT recurrence, with arbitrary unrestricted initial state."""
    state = [None] * (884 - BASE)
    for i in range(624):
        state[i] = tuple(1 << (32 * i + b) for b in range(32))
    for k in range(BASE + 624, 884):
        older = state[k - 624 - BASE]
        younger = state[k - 623 - BASE]
        middle = state[k - 227 - BASE]
        state[k - BASE] = tuple(
            middle[b]
            ^ (older[31] if b == 30 else younger[b + 1] if b < 30 else 0)
            ^ (younger[0] if (MAG >> b) & 1 else 0)
            for b in range(32)
        )
    return state


class Basis:
    def __init__(self):
        self.pivots = {}

    def add(self, expr, value):
        while expr:
            pos = expr.bit_length() - 1
            if pos not in self.pivots:
                self.pivots[pos] = expr, value
                return
            other, fixed = self.pivots[pos]
            expr ^= other
            value ^= fixed
        assert value == 0, 'Intact printer source contradicts the proposed alignment'

    def predicted(self, expr):
        result = 0
        while expr:
            pos = expr.bit_length() - 1
            if pos not in self.pivots:
                return None
            other, value = self.pivots[pos]
            expr ^= other
            result ^= value
        return result


def run(path):
    spool, trp = source_bytes(path)
    entries = [row for row in spool.decode('utf-8').splitlines() if 'PAYLOAD=' in row]
    assert len(entries) == 133
    symbolic = equations()
    bs = Basis()
    for row_idx, start in ROW_START.items():
        raw = bytes.fromhex(re.search(r'PAYLOAD=([0-9A-Fa-f]{32})', entries[row_idx]).group(1))
        for j in range(4):
            value = untemper(int.from_bytes(raw[j * 4:j * 4 + 4], 'little'))
            for b in range(32):
                bs.add(symbolic[start + j - BASE][b], (value >> b) & 1)
    assert len(bs.pivots) == 448

    seqmap = {}
    header = trp[:16]
    assert header[:8] == b'TRP2DUMP'
    assert struct.unpack_from('<I', header, 12)[0] == 88
    for rec in range(88):
        raw = trp[16 + 24 * rec:16 + 24 * (rec + 1)]
        if struct.unpack_from('<H', raw, 4)[0] != 49 or raw[6] != 82:
            continue
        seq = struct.unpack_from('<I', raw, 8)[0]
        control = untemper(struct.unpack_from('<I', raw, 12)[0])
        ok = zlib.crc32(raw[:20]) == struct.unpack_from('<I', raw, 20)[0]
        seqmap[seq] = rec, control, ok
    assert all(seq + d in seqmap for seq, _ in LANES for d in range(4))

    findings = []
    for origin, pos in LANES:
        for d in range(4):
            seq = origin + d
            index = pos + 3 * d
            rec, actual, crc = seqmap[seq]
            knownmask = 0
            predvalue = 0
            for b, expr in enumerate(symbolic[index - BASE]):
                got = bs.predicted(expr)
                if got is not None:
                    knownmask |= 1 << b
                    predvalue |= got << b
            assert (actual & knownmask) == predvalue, (
                f'seq{seq} contradicts withheld printer prediction'
            )
            findings.append((seq, rec, index, crc, knownmask, predvalue, actual))
            print(f'seq={seq} rec={rec:02} X[{index:>4}] '
                  f'CRC={"GOOD" if crc else "BAD"} '
                  f'predicted_mask={knownmask:08X} predicted_bits={predvalue:08X} '
                  f'observed={actual:08X} MATCH')

    new901 = next(f for f in findings if f[0] == 901)
    new991 = next(f for f in findings if f[0] == 991)
    assert new901[4] == 0xffffffff and new901[5] == 0x9FF49339 and not new901[3]
    # Agent43's conditional CRC-correcting *control-field* alternative fails
    # the newly predicted original word, independently of the REC8 commitment.
    repaired901 = untemper(int.from_bytes(bytes.fromhex('8582758F'), 'little'))
    assert repaired901 == 0xD7EB5833
    assert repaired901 != new901[5]
    assert new991[4] == 0x4DEE9E40 and new991[3]
    print('PROSPECTIVE_HOLDOUT: seq901 full32, seq991 independently fixed 16bits; both match')
    print('SOURCE_MODEL: four intact printer rows, rank448; two-step source relations only')
    print('COUPON_GAIN: zero observed selected K04 bits; K08 exact words zero')


if __name__ == '__main__':
    run(sys.argv[1] if len(sys.argv) > 1 else None)
