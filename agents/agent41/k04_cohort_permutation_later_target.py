"""K04 all nonzero row128->129 gaps: eight-bit source-carrier completion.

Run: python agents/agent41/k04_cohort_permutation_later_target.py
Reads only original source-pinned recorder, RC17, and intact spool row43.
Uses unchanged original K04 SHA solely to check completed candidate values.
"""
from hashlib import sha256
from pathlib import Path
from random import Random
import json
import re
import struct
import subprocess
import tempfile

import k04_cohort_permutation_scan as src
import k04_low31_crossrun as previous


def scan(executable, runs, novel, first_word, mask, desired_digest):
    with tempfile.TemporaryDirectory() as dirname:
        path = Path(dirname) / "source_runs.bin"
        with path.open("wb") as file:
            file.write(struct.pack("<II", len(runs), novel))
            for words, label in runs:
                file.write(struct.pack("<4I", *words))
            file.write(struct.pack("<I", first_word))
            file.write(mask)
            file.write(desired_digest)
        result = subprocess.run(
            [str(executable), str(path), "1"], capture_output=True,
            text=True, check=True)
        return result.stdout.strip()


def main():
    originals = {name: file.read_bytes() for name, file in src.FILES.items()}
    assert all(sha256(data).hexdigest() == previous.SHA[name]
               for name, data in originals.items())
    records = src.records(originals["recorder"])
    old = previous.recorder_runs(originals["recorder"]) + previous.procedure_runs(
        originals["procedure"])
    assert len(old) == 298

    spool_rows = [s for s in originals["spool"].decode().splitlines()
                  if s.startswith("2026-")]
    assert len(spool_rows) == 133
    word = bytes.fromhex(re.search(
        r"PAYLOAD=([0-9A-F]{32})", spool_rows[43])[1])[12:16]
    first_word = previous.untemper(int.from_bytes(word, "little"))
    spool_rows[129] = "[WITHHELD original disputed K04 coupon]"

    route = json.loads((src.E / "recovery-routing.json").read_text())
    original_acceptance = json.loads((src.ROOT / "acceptance.json").read_text())
    mask = bytes.fromhex(route["K04"]["masked_component"])
    desired_digest = bytes.fromhex(
        original_acceptance["slot_sha256"]["K04"])

    with tempfile.TemporaryDirectory() as dirname:
        executable = Path(dirname) / "eightbit_scan"
        subprocess.run([
            "cc", "-O3", str(Path(src.__file__).with_suffix(".c")),
            "-lcrypto", "-o", str(executable)], check=True)

        # Four actual CPython MT seeded, independently predicted payloads.
        for start in (628, 631, 650, 681):
            rng = Random(20261019 + start)
            states = [previous.untemper(rng.getrandbits(32))
                      for _ in range(start + 4)]
            early = tuple(x & 0x7FFFFFFF
                          for x in states[start - 623:start - 619])
            late = tuple(x & 0x7FFFFFFF
                         for x in states[start - 227:start - 223])
            payload = b"".join(src.temper(x).to_bytes(4, "little")
                               for x in states[start:start + 4])
            coupon = bytes(a ^ b for a, b in zip(payload, mask))
            control = scan(executable, [(early, "early"), (late, "late")],
                           2, states[3], mask, sha256(coupon).digest())
            assert "HIT early=0 late=1" in control, (start, control)
            print("ACTUAL_CPYTHON_SEEDED_LATER_TARGET_PASS", start)

        valid = src.permutations_in_source_cohorts(records, False)
        observed = scan(executable, valid + old, len(valid),
                        first_word, mask, desired_digest)
        print("CRC_VALID_LATER_TARGET", observed)
        assert "TESTED=35046400 HITS=0" in observed

        all_raw = src.permutations_in_source_cohorts(records, True)
        observed = scan(executable, all_raw + old, len(all_raw),
                        first_word, mask, desired_digest)
        print("ALL_RAW_CRC_AUXILIARY_LATER_TARGET", observed)
        assert "TESTED=39740416 HITS=0" in observed
    print("SELECTED_K04_ROW129_WITHHELD; NO_ACCEPTED_K04")


if __name__ == "__main__":
    main()
