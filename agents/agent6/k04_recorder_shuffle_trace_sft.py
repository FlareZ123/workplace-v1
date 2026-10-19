"""Bounded Fisher-Yates trace test on original TRP2 physical order.

Input: original 43-member ZIP. Withhold disputed printer row129 and commitments.
Only tests three original-field orderings and no-rejection four-draw matches.
The source does not authenticate a shuffle, shared producer or clock.
"""
import hashlib
import random
import re
import struct
import sys
from zipfile import ZipFile

RECORDER = "evidence/recorder/trip-recorder.raw"
SPOOL = "evidence/print/spool-reconstruction.log"
RECORDER_SHA = "5ebc6204ed773102237dd287772de96d19740e163b49b4075537d937888657ba"
SPOOL_SHA = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"


def inverse_shuffle(start, final):
    running = list(start)
    result = []
    for i in range(len(running) - 1, 0, -1):
        j = running.index(final[i], 0, i + 1)
        running[i], running[j] = running[j], running[i]
        result.append((i, j))
    assert running == list(final)
    return result


def source_matches(draws, printer):
    matched = []
    checks = 0
    for offset in range(len(draws) - 3):
        four = draws[offset:offset + 4]
        widths = [(i + 1).bit_length() for i, _ in four]
        for row, block in enumerate(printer):
            if row == 129:
                continue
            checks += 1
            if all(block[j] >> (32 - widths[j]) == four[j][1]
                   for j in range(4)):
                matched.append((offset, row, sum(widths)))
    return checks, matched


def synthetic_control():
    initial = list(range(88))
    for seed in range(2000):
        rng = random.Random(seed)
        first = [rng.getrandbits(32) for _ in range(4)]
        widths = [(i + 1).bit_length() for i in range(87, 83, -1)]
        indices = [first[j] >> (32 - widths[j]) for j in range(4)]
        if any(k > i for k, i in zip(indices, range(87, 83, -1))):
            continue
        arr = initial[:]
        for step, i in enumerate(range(87, 0, -1)):
            width = (i + 1).bit_length()
            if step < 4:
                j = indices[step]
            else:
                while (j := rng.getrandbits(width)) > i:
                    pass
            arr[i], arr[j] = arr[j], arr[i]
        assert [j for _, j in inverse_shuffle(initial, arr)[:4]] == indices
        assert source_matches(inverse_shuffle(initial, arr), [tuple(first)])[1] == [
            (0, 0, sum(widths))
        ]
        return seed
    raise AssertionError("synthetic control failed")


def main(source):
    with ZipFile(source) as z:
        binary, spool = z.read(RECORDER), z.read(SPOOL)
    assert hashlib.sha256(binary).hexdigest() == RECORDER_SHA
    assert hashlib.sha256(spool).hexdigest() == SPOOL_SHA
    assert struct.unpack_from("<8sHHI", binary) == (b"TRP2DUMP", 2, 24, 88)
    records = [struct.unpack_from("<IHBBI4sII", binary, 16 + 24 * i)
               for i in range(88)]
    labels = [(rec[1], rec[4]) for rec in records]
    assert len(set(labels)) == 88
    lines = [line for line in spool.decode().splitlines()
             if line.startswith("2026-")]
    assert len(lines) == 133
    printer = [
        struct.unpack("<4I", bytes.fromhex(re.search(
            r"PAYLOAD=([0-9A-F]{32})", line).group(1)))
        for line in lines
    ]
    preorders = {
        "node49_first": sorted(range(88), key=lambda i:
                               (records[i][1], records[i][4])),
        "node50_first": sorted(range(88), key=lambda i:
                               (-records[i][1], records[i][4])),
        "timestamp_first": sorted(range(88), key=lambda i:
                                  (records[i][0], records[i][1], records[i][4])),
    }
    print("synthetic_control_seed", synthetic_control())
    for label, order in preorders.items():
        draws = inverse_shuffle([labels[i] for i in order], labels)
        checks, matches = source_matches(draws, printer)
        print(label, "checked", checks, "matches", matches,
              "at_least_24bit", sum(bits >= 24 for _, _, bits in matches))
    print("historical_shuffle_producer_authenticated", False)
    print("target_donor_index_bridges", 0)
    print("K04_K08_UNRESOLVED")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python k04_recorder_shuffle_trace_sft.py original.zip")
    main(sys.argv[1])
