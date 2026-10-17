"""Bounded K04 32-bit source-fragment reassembly audit (Agent 10).

Read-only. Run from a checkout with: python results/check_h17_k04_word_reassembly.py
"""
from __future__ import annotations

import hashlib
import itertools
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "resources"
SPOOL = ROOT / "evidence/print/spool-reconstruction.log"
ROUTE = ROOT / "evidence/recovery-routing.json"
ACCEPTANCE = ROOT / "acceptance.json"
JOB = "PS-261003-0417"


def run() -> None:
    source = SPOOL.read_text(encoding="utf-8")
    digest = hashlib.sha256(source.encode("utf-8")).hexdigest()
    assert digest == "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083", digest
    routing = json.loads(ROUTE.read_text(encoding="utf-8"))
    commitments = json.loads(ACCEPTANCE.read_text(encoding="utf-8"))
    mask = bytes.fromhex(routing["K04"]["masked_component"])
    expected = bytes.fromhex(commitments["slot_sha256"]["K04"])

    entries = [
        line for line in source.splitlines()
        if f"JOB={JOB}" in line and "CLASS=RECOVER" in line
    ]
    assert len(entries) == 3, "Unexpected same-job RECOVER record count"
    payloads = [
        bytes.fromhex(re.search(r"PAYLOAD=([0-9A-F]{32})", line).group(1))
        for line in entries
    ]
    assert all(len(x) == 16 for x in payloads)

    words = [payload[i:i + 4] for payload in payloads for i in range(0, 16, 4)]
    choices = tuple(w for word in words for w in (word, word[::-1]))
    assert len(choices) == 24 and len(set(choices)) == 24
    baseline = bytes(a ^ b for a, b in zip(payloads[1], mask))
    print(f"last ACK XOR: {baseline.hex().upper()}")
    print(f"last ACK SHA256: {hashlib.sha256(baseline).hexdigest()}")
    assert hashlib.sha256(baseline).digest() != expected

    # Positive control: the chosen tuple must be accepted by the same hash test.
    control = bytes(x ^ y for x, y in zip(b"".join(choices[:4]), mask))
    control_digest = hashlib.sha256(control).digest()
    assert hashlib.sha256(control).digest() == control_digest

    checked = 0
    control_found = False
    for parts in itertools.product(choices, repeat=4):
        component = bytes(x ^ y for x, y in zip(b"".join(parts), mask))
        candidate_hash = hashlib.sha256(component).digest()
        checked += 1
        if candidate_hash == control_digest:
            control_found = True
        if candidate_hash == expected:
            raise AssertionError(
                f"Original K04 commitment MATCHED: {component.hex().upper()}"
            )
    assert checked == 24**4 and control_found
    print(f"NO_MATCH for {checked:,} assignments (24^4); control_found={control_found}")


if __name__ == "__main__":
    run()
