"""Test a preserved ESC-N RECOVER coupon payload against REC8/1 K04.

This is a read-only byte validator. A PASS is not proof of the coupon's
provenance or an integrity certificate for the original physical media.
The baseline spool-derived payload in export 06 fails the commitment.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1] / "resources"


def check_coupon(payload_hex: str) -> dict[str, str]:
    """XOR an exactly 16-byte opaque payload and check the original K04 hash."""
    if re.fullmatch(r"[0-9A-Fa-f]{32}", payload_hex) is None:
        raise ValueError("payload must be exactly 32 hexadecimal characters")
    routing = json.loads((ROOT / "evidence/recovery-routing.json").read_text(encoding="utf-8"))
    acceptance = json.loads((ROOT / "acceptance.json").read_text(encoding="utf-8"))
    mask = bytes.fromhex(routing["K04"]["masked_component"])
    payload = bytes.fromhex(payload_hex)
    if len(mask) != 16:
        raise ValueError("routing mask must be exactly 16 bytes")
    component = bytes(a ^ b for a, b in zip(payload, mask))
    actual = hashlib.sha256(component).hexdigest()
    return {
        "payload_hex": payload.hex().upper(),
        "candidate_K04": component.hex().upper(),
        "candidate_sha256": actual,
        "target_sha256": acceptance["slot_sha256"]["K04"],
        "acceptance": "PASS" if actual == acceptance["slot_sha256"]["K04"] else "NO_MATCH",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("payload", help="Independently recovered 16-byte coupon payload in hex")
    args = parser.parse_args()
    result = check_coupon(args.payload)
    print(json.dumps(result, indent=2))
    return 0 if result["acceptance"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
