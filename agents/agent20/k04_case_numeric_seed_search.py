"""Source-number CPython MT seed attack with unknown advanced output phase.

Usage: python agents/agent20/k04_case_numeric_seed_search.py original-case.zip
Reads only original records, withholds printer row129 and all REC8 material.
Finds a complete 4x32-bit intact printer row3 fingerprint within 65,536
generator outputs for every integer seed derivable from numeric source tokens.
"""
import datetime
import hashlib
import random
import re
import struct
import sys
import time
import zipfile

if len(sys.argv) != 2:
    raise SystemExit("usage: python k04_case_numeric_seed_search.py original-case.zip")

SPOOL = "evidence/print/spool-reconstruction.log"
SPOOL_SHA = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
MAX_WORDS = 65536
seeds = {}


def add_seed(number, origin):
    if 0 <= number < 2**64:
        seeds.setdefault(number, origin)


with zipfile.ZipFile(sys.argv[1]) as z:
    raw = z.read(SPOOL)
    assert hashlib.sha256(raw).hexdigest() == SPOOL_SHA
    rows = [x for x in raw.decode().splitlines() if x.startswith("2026-")]
    assert len(rows) == 133
    row3 = struct.unpack(
        "<4I", bytes.fromhex(re.search(r"PAYLOAD=([0-9A-F]{32})", rows[3]).group(1))
    )
    row7 = struct.unpack(
        "<4I", bytes.fromhex(re.search(r"PAYLOAD=([0-9A-F]{32})", rows[7]).group(1))
    )

    for name in z.namelist():
        if not name.startswith("evidence/") or name == SPOOL or name.endswith(".raw"):
            continue
        try:
            text = z.read(name).decode("utf-8")
        except UnicodeDecodeError:
            continue
        for value in re.findall(r"(?<![A-Za-z0-9])[0-9]{1,16}(?![A-Za-z0-9])", text):
            add_seed(int(value), name + " decimal")
        for value in re.findall(r"(?<![A-Za-z0-9])[A-Fa-f0-9]{8,16}(?![A-Za-z0-9])", text):
            if any(c in "abcdefABCDEF" for c in value):
                add_seed(int(value, 16), name + " hex")
        for date in re.findall(r"20[12][0-9]-[01][0-9]-[0-3][0-9]", text):
            add_seed(int(date.replace("-", "")), name + " date")
        for timestamp in re.findall(
            r"20[12][0-9]-[01][0-9]-[0-3][0-9]T[0-2][0-9]:[0-5][0-9]:[0-5][0-9](?:\+00:00|Z)",
            text,
        ):
            try:
                stamp = datetime.datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
                add_seed(int(stamp.timestamp()), name + " UTC epoch")
            except ValueError:
                pass

    recorder = z.read("evidence/recorder/trip-recorder.raw")
    assert recorder[:8] == b"TRP2DUMP"
    for i in range((len(recorder) - 16) // 24):
        record = recorder[16 + 24 * i : 16 + 24 * (i + 1)]
        add_seed(struct.unpack_from("<I", record, 0)[0], "TRP2 timestamp " + str(i))
        add_seed(struct.unpack_from("<I", record, 8)[0], "TRP2 sequence " + str(i))


def locate(seed, expected):
    rng = random.Random(seed)
    for i in range(MAX_WORDS - 3):
        if rng.getrandbits(32) != expected[0]:
            continue
        # Preserve every possible overlapping start after a partial mismatch.
        after_first = rng.getstate()
        if all(rng.getrandbits(32) == want for want in expected[1:]):
            return i
        rng.setstate(after_first)
    return None


# Same first-word prefilter and continuation as source search, beyond the first cycle.
control_seed = 9999961
control_phase = 41578
rng = random.Random(control_seed)
for _ in range(control_phase):
    rng.getrandbits(32)
control = tuple(rng.getrandbits(32) for _ in range(4))
assert locate(control_seed, control) == control_phase
print("synthetic_late_cycle_control_PASS", control_phase)
print("source_int_seeds", len(seeds), "max_outputs_per_seed", MAX_WORDS)
started = time.perf_counter()
hits = [(seed, pos, origin) for seed, origin in sorted(seeds.items())
        if (pos := locate(seed, row3)) is not None]
print("row3_fourword_hits", hits, "seconds", round(time.perf_counter() - started, 3))
for seed, phase, origin in hits:
    print("heldout_row7_position", seed, locate(seed, row7))
print("selected_row129_withheld", True)
