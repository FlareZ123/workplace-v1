"""Test finite one-bit-per-row source carriers in the 128 regular spool records.

A supplementary, hypothetical local-evidence search; read-only and no key claims
unless unchanged K04 commitment matches. Python standard library only.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE if (HERE / "evidence").is_dir() else HERE.parent / "resources"
EVIDENCE = ROOT / "evidence"
SPOOL = EVIDENCE / "print" / "spool-reconstruction.log"
SPOOL_SHA256 = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"


def pack(bits: list[int], reverse: bool, low_first: bool) -> bytes:
    assert len(bits) == 128
    if reverse:
        bits = bits[::-1]
    result = bytearray(16)
    for n, bit in enumerate(bits):
        result[n // 8] |= bit << ((n % 8) if low_first else (7 - n % 8))
    return bytes(result)


def candidates(payloads: list[bytes]):
    for byte_idx in range(16):
        for bit_idx in range(8):
            bits = [(p[byte_idx] >> bit_idx) & 1 for p in payloads]
            for reverse in (False, True):
                for low_first in (False, True):
                    yield f"byte{byte_idx}_bit{bit_idx}_reverse{int(reverse)}_little{int(low_first)}", pack(bits, reverse, low_first)
    for byte_idx in range(16):
        bits = [p[byte_idx].bit_count() & 1 for p in payloads]
        for reverse in (False, True):
            for low_first in (False, True):
                yield f"byte{byte_idx}_parity_reverse{int(reverse)}_little{int(low_first)}", pack(bits, reverse, low_first)
    for bit_idx in range(8):
        bits = [(sum((value >> bit_idx) & 1 for value in p) & 1) for p in payloads]
        for reverse in (False, True):
            for low_first in (False, True):
                yield f"column_bit{bit_idx}_parity_reverse{int(reverse)}_little{int(low_first)}", pack(bits, reverse, low_first)
    bits = [sum(byte.bit_count() for byte in p) & 1 for p in payloads]
    for reverse in (False, True):
        for low_first in (False, True):
            yield f"allbits_parity_reverse{int(reverse)}_little{int(low_first)}", pack(bits, reverse, low_first)


def main():
    original = SPOOL.read_bytes()
    assert hashlib.sha256(original).hexdigest() == SPOOL_SHA256
    rows = []
    for line in original.decode("utf-8").splitlines():
        if not line or line.startswith("#"):
            continue
        fields = dict(re.findall(r"\b(\w+)=(\S+)", line))
        rows.append((line.split(" ", 1)[0], fields))
    regular = [(ts, fields) for ts, fields in rows if ts.endswith("+00:00")]
    tail = [(ts, fields) for ts, fields in rows if ts.endswith("Z")]
    assert len(rows) == 133 and len(regular) == 128 and len(tail) == 5
    assert [int(f["JOB"].split("-")[-1]) for _, f in regular] == list(range(300, 428))
    payloads = [bytes.fromhex(f["PAYLOAD"]) for _, f in regular]
    assert all(len(p) == 16 for p in payloads)
    route = json.loads((EVIDENCE / "recovery-routing.json").read_text(encoding="utf-8"))
    commitments = json.loads((ROOT / "acceptance.json").read_text(encoding="utf-8"))
    mask = bytes.fromhex(route["K04"]["masked_component"])
    target = commitments["slot_sha256"]["K04"]
    def digest(raw):
        return hashlib.sha256(bytes(a ^ b for a,b in zip(raw,mask))).hexdigest()
    tests = list(candidates(payloads))
    assert len(tests) == 612, len(tests)
    control = digest(tests[0][1])
    assert any(digest(raw) == control for _, raw in tests)
    hits = [(label, raw.hex().upper()) for label, raw in tests if digest(raw) == target]
    print(json.dumps({"rows_regular":128,"rows_tail_excluded":5,"candidate_assignments":len(tests),"synthetic_positive_control":"PASS","original_k04_hits":hits,"status":"MATCH" if hits else "NO_MATCH"}, indent=2))


if __name__ == "__main__":
    main()
