"""Exact 96-bit CPython numeric-seed inversion under H-17 shared-recorder phase s7=394.

Source-only mode: K04 selected printer row129 and all REC8 inputs are withheld.
There is one unknown 32-bit CPython init_by_array seed word at each row3 phase.
The original row7 pair run and CRC-valid TRP2 record26 reconstruct the terminal
initialized state S[623]. Exhaustive native inversion emits complete-seed
candidates, then genuine CPython output regeneration challenges row3 and row7.

Reproduce: python agents/agent3/k04_seed3_origin_scan.py --phase-min 369 --phase-max 369
No per-commit CI. This is an explicitly conditional producer/origin model.
"""
import argparse
import hashlib
from pathlib import Path
import random
import re
import struct
import subprocess
import sys
import tempfile
from zipfile import ZipFile
import zlib

HERE = Path(__file__).resolve().parent
AGENTS = HERE.parent
sys.path[:0] = [str(AGENTS / name) for name in
                ("agent46", "agent1", "agent8", "agent31", "agent23")]
from k04_python_seed_fragments import extract_pairs, fragments, initial_words
from k04_seed_seven_window import extra_pairs
from k04_cross_carrier_seed_windows import indexed_groups
from k04_mt_rowstart import untemper
from k04_mt_recursive_peel import temper

SPOOL = "evidence/print/spool-reconstruction.log"
TRP = "evidence/recorder/trip-recorder.raw"
SPOOL_SHA = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
TOTAL = 1 << 32
REGEX = re.compile(
    r"FOUND missing_index=(\d+) missing_word=([0-9A-F]{8}) "
    r"full_keys=([0-9A-F]{8}) ([0-9A-F]{8}) ([0-9A-F]{8})"
)


def run_engine(engine, phase, pairs, terminal, workers, count=TOTAL):
    known = fragments(pairs, phase, 3)
    state = initial_words(pairs)
    assert len(state) == 4 and len(known) == 2
    missing = (phase + 231) % 3
    assert missing not in known
    args = [str(engine), str(phase),
            *(str(known.get(i, 0)) for i in range(3)),
            *(str(word) for word in state),
            str(terminal), "0", str(count), str(workers)]
    completed = subprocess.run(args, text=True, check=True,
                               capture_output=True)
    raw = completed.stdout
    assert f"CHECKED phase={phase} n={count} " in raw, raw
    seeds = []
    for match in REGEX.finditer(raw):
        index, word, *keys = match.groups()
        assert int(index) == missing
        assert int(word, 16) == int(keys[missing], 16)
        seed = sum(int(keys[j], 16) << (j * 32) for j in range(3))
        seeds.append(seed)
    assert f"hits={len(seeds)}" in raw, raw
    return seeds, raw.strip().splitlines()[-1]


def synthetic(engine, workers):
    seed = (0xFE412F34 << 64) | (0x1F0A0211 << 32) | 1234
    r = random.Random(seed)
    terminal = r.getstate()[1][623]
    states = [untemper(r.getrandbits(32)) for _ in range(625)]
    phase = 369
    pairs = [(states[phase+j], states[phase+j+227])
             for j in range(5)]
    matches, summary = run_engine(engine, phase, pairs, terminal,
                                  workers, count=100000)
    assert matches == [seed], (matches, seed)
    print("SYNTHETIC_96BIT_RECOVERY_PASS", summary, flush=True)


def source_data(source):
    with ZipFile(source) as z:
        spool = z.read(SPOOL)
        recorder = z.read(TRP)
    assert hashlib.sha256(spool).hexdigest() == SPOOL_SHA
    assert recorder[:8] == b"TRP2DUMP"
    assert struct.unpack_from("<I", recorder, 12)[0] == 88
    r26 = recorder[16 + 26 * 24:16 + 27 * 24]
    assert zlib.crc32(r26[:20]) == struct.unpack_from("<I", r26, 20)[0]
    control = untemper(struct.unpack_from("<I", r26, 12)[0])
    assert control == 0xBBC259FD

    row3, _, _, _ = extract_pairs(source)
    row7, _ = extra_pairs(source)
    assert len(row3) == 5 and len(row7) == 3
    # A pair (X[p],X[p+227]) inverse-twists to the predecessor's
    # highest bit and successor's low31 bits. Two successive pairs
    # combine into the full 32-bit initialized state S[623] when s7=394.
    def mix(a, b):
        delta = a ^ b
        parity = delta >> 31
        return (((delta ^ (0x9908B0DF if parity else 0)) << 1)
                | parity) & 0xFFFFFFFF
    mixed = [mix(a, b) for a, b in row7]
    terminal = (mixed[0] & 0x7FFFFFFF) | (mixed[1] & 0x80000000)
    assert terminal == 0x2F9F1C79
    assert (mixed[2] & 0x7FFFFFFF) == (control & 0x7FFFFFFF)
    print("SOURCE_RECORDED_CRC_OK", True,
          "ORIGIN_ASSUMPTION_s7", 394,
          "STATE_S623", f"{terminal:08X}", flush=True)
    return row3, row7, terminal


def phase_bounds(source):
    # Common-stream conditional row equalities: 42 original MT witnesses
    # plus 3 schema-defined recorder/RC-17 bridges. Under the CLASS and
    # DEST producer hypothesis each regular row transition consumes
    # at least 6 MT output words: 4 payload + 2 metadata draws.
    values, groups = indexed_groups(source, True)
    assert len(values) == 133 and not values[129]
    edges = []
    for group in groups.values():
        root, origin = group[0]
        for row, offset in group[1:]:
            shift = offset - origin
            edges.extend(((root, row, shift), (row, root, -shift)))
    edges.extend((row + 1, row, -6 if row < 128 else -4)
                 for row in range(132))

    def shortest(start, target):
        d = [10**8] * 133
        d[start] = 0
        for iteration in range(133):
            changed = False
            for a, b, distance in edges:
                if d[a] + distance < d[b]:
                    d[b] = d[a] + distance
                    changed = True
            if not changed:
                break
        assert not changed, "contradictory producer-phase hypothesis"
        return d[target]

    minimum_gap = -shortest(7, 3)
    maximum_gap = shortest(3, 7)
    assert (minimum_gap, maximum_gap) == (28, 37)
    # Row3 five-pair window starts one draw before row3 payload.
    # Given the explicitly hypothesized absolute s7=394:
    # p3 = s3-1 = 393-(s7-s3).
    result = 393 - maximum_gap, 393 - minimum_gap
    assert result == (356, 365)
    print("SOURCE_CONDITIONAL_PHASE_BOUNDS", result,
          "row3_to_7_gap", (minimum_gap, maximum_gap), flush=True)
    return result


def heldout(seed, phase, row3, row7, terminal):
    rng = random.Random(seed)
    real_terminal = rng.getstate()[1][623]
    outputs = [untemper(rng.getrandbits(32)) for _ in range(625)]
    def matches(run, at):
        return sum(outputs[at+j] == a and outputs[at+j+227] == b
                   for j, (a, b) in enumerate(run))
    return real_terminal == terminal, matches(row3, phase), matches(row7, 395)


def main(args):
    assert 356 <= args.phase_min <= args.phase_max <= 365
    synthetic(args.engine, args.workers)
    with tempfile.TemporaryDirectory(prefix="h17-seed3-") as d:
        source = Path(d) / "source.zip"
        with ZipFile(source, "w") as z:
            for relative in (SPOOL, TRP):
                z.write(args.resources / relative, relative)
        row3, row7, terminal = source_data(source)
        assert phase_bounds(source) == (356, 365)
        checked = 0
        accepted = 0
        for p in range(args.phase_min, args.phase_max + 1):
            candidates, summary = run_engine(args.engine, p, row3, terminal,
                                             args.workers)
            checked += 1
            print("EXHAUSTIVE_PHASE", summary, flush=True)
            for seed in candidates:
                terminal_ok, a, b = heldout(seed, p, row3, row7, terminal)
                status = "SOURCE_SEED_PASS" if (terminal_ok and a == 5 and b == 3) else "SOURCE_SEED_REJECT"
                print(status, "phase", p, "seed", f"{seed:024X}",
                      "actual_initialized_state", terminal_ok,
                      "row3_pairs", a, "of", 5,
                      "row7_pairs", b, "of", 3, flush=True)
                if status == "SOURCE_SEED_PASS":
                    accepted += 1
        print("ORIGINAL_PHASES_EXHAUSTED", checked,
              "COMPLETE_SOURCE_MATCHES", accepted,
              "selected_row129_withheld", True,
              "original_verifier_and_commitments_untouched", True, flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--resources", type=Path,
                        default=Path(__file__).resolve().parents[2] / "resources")
    parser.add_argument("--engine", type=Path,
                        default=HERE / "k04_seed3_word")
    parser.add_argument("--phase-min", type=int, default=321)
    parser.add_argument("--phase-max", type=int, default=369)
    parser.add_argument("--workers", type=int, default=2)
    main(parser.parse_args())
