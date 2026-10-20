"""Source-pinned K04 MT19937 reachable-state causal-cut test.

Run from repository root, or supply the unchanged original case ZIP:
    python agents/agent14/k04_reachable_state_cut_sft.py [original-case.zip]

Only intact printer payloads are read; selected row129, all REC8
commitments, route mask, K08 and verifier are excluded.
"""
import hashlib
import random
import re
import struct
import sys
from pathlib import Path
from zipfile import ZipFile

SPOOL_SHA256 = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
MAGIC = 0x9908B0DF
STARTS = (
    0,7,15,22,30,38,44,51,67,76,84,92,99,112,120,126,132,138,144,151,
    158,165,171,179,186,192,198,205,211,218,224,230,237,243,250,260,
    268,278,285,298,305,311,318,328,339,346,352,358,364,370,376,382,
    388,394,401,407,416,423,429,436,442,456,463,474,481,489,495,507,
    515,522,530,536,543,549,563,569,576,584,590,597,604,610,617,624,
    632,638,644,650,659,665,671,679,689,697,705,714,721,733,740,747,
    753,759,766,772,783,789,796,807,813,820,826,833,839,846,853,861,
    870,876,882,888,896,906,916,922,928,934,940,946,951,955,959,963,967,
)

def untemper(y):
    y ^= y >> 18
    y ^= (y << 15) & 0xEFC60000
    for _ in range(7):
        y ^= (y << 7) & 0x9D2C5680
    for _ in range(3):
        y ^= y >> 11
    return y & 0xFFFFFFFF

def twist(x, y):
    pair = (x & 0x80000000) | (y & 0x7FFFFFFF)
    return (pair >> 1) ^ (MAGIC if pair & 1 else 0)

def spool_rows(path):
    if path is None:
        source = Path(__file__).resolve().parents[2] / "resources/evidence/print/spool-reconstruction.log"
        raw = source.read_bytes()
    else:
        with ZipFile(path) as archive:
            raw = archive.read("evidence/print/spool-reconstruction.log")
    assert hashlib.sha256(raw).hexdigest() == SPOOL_SHA256
    rows = [line for line in raw.decode("utf-8").splitlines() if "PAYLOAD=" in line]
    assert len(rows) == len(STARTS) == 133 and STARTS[129] == 955
    return rows

def mt_expressions(limit):
    words = [[1 << (32*i+b) for b in range(32)] for i in range(624)]
    for t in range(limit - 623):
        old, nxt, middle = words[t], words[t+1], words[t+397]
        words.append([
            middle[b]
            ^ (old[31] if b == 30 else nxt[b+1] if b < 30 else 0)
            ^ (nxt[0] if (MAGIC >> b) & 1 else 0)
            for b in range(32)
        ])
    assert len(words) == limit + 1
    return words

class AffineBasis:
    def __init__(self):
        self.pivots = {}

    def add(self, equation, bit):
        while equation:
            pivot = equation.bit_length() - 1
            if pivot not in self.pivots:
                self.pivots[pivot] = (equation, bit)
                return 1
            known_eq, known_bit = self.pivots[pivot]
            equation ^= known_eq
            bit ^= known_bit
        assert bit == 0, "Original intact source contradicts MT model"
        return 0

    def quotient_rank(self, expressions):
        pivots = {k: value[0] for k, value in self.pivots.items()}
        gain = 0
        for expression in expressions:
            while expression:
                pivot = expression.bit_length() - 1
                if pivot not in pivots:
                    pivots[pivot] = expression
                    gain += 1
                    break
                expression ^= pivots[pivot]
        return gain

def check_original(rows):
    symbolic = mt_expressions(970)
    basis = AffineBasis()
    for row_id, start in enumerate(STARTS):
        if row_id == 129:
            continue
        match = re.search(r"PAYLOAD=([0-9A-Fa-f]{32})", rows[row_id])
        assert match is not None
        packed = bytes.fromhex(match.group(1))
        for offset, output in enumerate(struct.unpack("<4I", packed)):
            state = untemper(output)
            for bit, expression in enumerate(symbolic[start + offset]):
                basis.add(expression, (state >> bit) & 1)

    assert len(basis.pivots) == 15305
    target = [e for word in symbolic[955:959] for e in word]
    assert basis.quotient_rank(target) == 128

    # Necessary and sufficient 31-dimensional restriction for a window
    # X0..X623 to have a predecessor X[-1] under the MT recurrence.
    # X[-1].high affects only equation bit30, which is omitted.
    independent = 0
    for bit in range(32):
        if bit == 30:
            continue
        expression = (
            symbolic[623][bit] ^ symbolic[396][bit]
            ^ (symbolic[0][bit+1] if bit < 30 else 0)
            ^ (symbolic[0][0] if (MAGIC >> bit) & 1 else 0)
        )
        independent += basis.add(expression, 0)
    assert independent == 31
    assert len(basis.pivots) == 15336
    assert basis.quotient_rank(target) == 128
    assert 624*32 - len(basis.pivots) - 128 == 4504

    print("ORIGINAL_SOURCE rank=15305; reachable_state_rank=15336")
    print("MT_PREDECESSOR_IMAGE restrictions=31 independent, consistent")
    print("SELECTED_K04 target_quotient=128/128; fixed_source_bits=0")
    print("CONDITIONAL_STATES_PER_POSSIBLE_128BIT_TARGET=2^4504")

def check_causal_support():
    count = 0
    for p in range(945, 956):
        for d in range(11, 66):
            for delta in range(627, d + 617):
                u, q = p-851, p-623
                perturbation_support = {u, q, q+1, q+2, q+3}
                assert perturbation_support.isdisjoint({0, 396, 623})
                assert 0 < u < q and q+3 < 396
                count += 1
    assert count == 16940
    print("UNIFORM_CAUSAL_SUPPORT models=16940; image_constraints_unchanged=True")

def check_seeded_positive_controls():
    for seed in (0, 5489, 123456789, 0xF00DBEEF):
        rng = random.Random(seed)
        stream = [untemper(rng.getrandbits(32)) for _ in range(1248)]
        assert stream[1247] == stream[1020] ^ twist(stream[623], stream[624])
    print("ACTUAL_CPYTHON_MT_POSITIVE_CONTROLS=4/4")

def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    check_seeded_positive_controls()
    check_causal_support()
    check_original(spool_rows(path))
    print("RESULT=CONDITIONAL_NO_K04_GAIN; K08_UNTESTED")

if __name__ == "__main__":
    main()
