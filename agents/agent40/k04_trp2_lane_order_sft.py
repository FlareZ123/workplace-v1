"""K04: source-only 48-way TRP2 three-lane ordering discriminator.

Read-only, no disputed row129, REC8 commitments, mask, or K08 nonce.
Uses Agent14's original-state symbolic recurrence and source hash pins.
Run from repository root with optional original-case ZIP path.
"""
from itertools import permutations, product
from pathlib import Path
import random
import re
import struct
import sys
import zlib

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'agent14'))
from k04_trp2_interleaved_cohort_sft import (
    BASE, MAG, ROW_START, Basis, equations, source_bytes, untemper
)

COHORTS = (200, 900, 990)
OFFSET = (-396, -395, -394)


def prediction(arr, rows):
    basis = Basis()
    for row, start in ROW_START.items():
        for j, word in enumerate(rows[row]):
            for bit, expr in enumerate(arr[start + j - BASE]):
                basis.add(expr, (word >> bit) & 1)
    assert len(basis.pivots) == 448
    result = {}
    for idx in range(-396, -384):
        mask = value = 0
        for bit, expr in enumerate(arr[idx - BASE]):
            predicted = basis.predicted(expr)
            if predicted is not None:
                mask |= 1 << bit
                value |= predicted << bit
        result[idx] = mask, value
    return result


def variants(predicted, controls):
    cases = []
    for order in permutations(COHORTS):
        for reversed_lanes in product((False, True), repeat=3):
            failures = []
            for lane, first_seq in enumerate(order):
                for d in range(4):
                    idx = -396 + lane + 3 * d
                    seq = first_seq + (3 - d if reversed_lanes[lane] else d)
                    actual, crc_ok = controls[seq]
                    mask, value = predicted[idx]
                    if actual & mask != value:
                        failures.append((seq, idx, crc_ok, mask.bit_count()))
            cases.append((order, reversed_lanes, failures))
    assert len(cases) == 48
    return cases


def synthetic_controls(arr):
    for trial in range(16):
        rng = random.Random(0x1723AC + trial)
        state = [rng.getrandbits(32) for _ in range(624)]
        for k in range(624, 884 - BASE):
            prev, nxt, middle = state[k - 624], state[k - 623], state[k - 227]
            part = (prev & 0x80000000) | (nxt & 0x7FFFFFFF)
            state.append(middle ^ (part >> 1) ^ (MAG if part & 1 else 0))
        rows = {
            row: [state[start + j - BASE] for j in range(4)]
            for row, start in ROW_START.items()
        }
        truth = {
            base + d: (state[-396 + lane + 3*d - BASE], base != 900)
            for lane, base in enumerate(COHORTS) for d in range(4)
        }
        cases = variants(prediction(arr, rows), truth)
        exact = [c for c in cases if not c[2]]
        assert len(exact) == 1
        assert exact[0][:2] == (COHORTS, (False, False, False))
    print('SYNTHETIC_16_UNRESTRICTED_STATE_POSITIVE_CONTROLS_PASS')


def main(source=None):
    spool, recorder = source_bytes(source)
    lines = [line for line in spool.decode().splitlines() if line.startswith('2026-')]
    assert len(lines) == 133
    original_rows = {}
    for row in ROW_START:
        payload = bytes.fromhex(
            re.search(r'PAYLOAD=([A-Fa-f0-9]{32})', lines[row]).group(1)
        )
        original_rows[row] = [
            untemper(int.from_bytes(payload[j*4:j*4+4], 'little'))
            for j in range(4)
        ]
    control = {}
    assert recorder[:8] == b'TRP2DUMP'
    assert struct.unpack_from('<I', recorder, 12)[0] == 88
    for i in range(88):
        record = recorder[16 + 24*i:16 + 24*(i+1)]
        if struct.unpack_from('<H', record, 4)[0] != 49 or record[6] != 82:
            continue
        seq = struct.unpack_from('<I', record, 8)[0]
        word = untemper(struct.unpack_from('<I', record, 12)[0])
        valid = zlib.crc32(record[:20]) == struct.unpack_from('<I', record, 20)[0]
        control[seq] = word, valid
    assert all(base + d in control for base in COHORTS for d in range(4))
    arr = equations()
    synthetic_controls(arr)
    predicted = prediction(arr, original_rows)
    cases = variants(predicted, control)
    exact = [case for case in cases if not case[2]]
    valid_crc_only = [
        case for case in cases
        if not any(crc_good for _, _, crc_good, _ in case[2])
    ]
    assert len(exact) == 1
    assert exact[0][:2] == (COHORTS, (False, False, False))
    assert len(valid_crc_only) == 2
    assert [case[:2] for case in valid_crc_only] == [
        (COHORTS, (False, False, False)),
        (COHORTS, (False, True, False))
    ]
    histogram = {
        n: sum(len(case[2]) == n for case in cases)
        for n in range(13)
        if any(len(case[2]) == n for case in cases)
    }
    masks = {index: f'{mask:08X}' for index, (mask, _) in predicted.items()}
    print('PRINTER_ONLY_CONSTRAINT_MASKS', masks)
    print('ORIGINAL_48_MODELS_FAILURE_HISTOGRAM', histogram)
    print('ALL_SOURCE_UNIQUE_ORDER', exact[0][:2])
    print('CRC_GOOD_ONLY_TWO_ORDERS', [case[:2] for case in valid_crc_only])
    print('PER_ORDER_FIXED_CONSTRAINTS', sum(m.bit_count() for m, _ in predicted.values()))
    print('ACTUAL_SELECTED_COUPON_BITS_GAIN', 0)
    print('K08_FINAL_QUOTED_WORDS_GAIN', 0)


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) == 2 else None)
