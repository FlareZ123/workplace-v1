"""Read-only, bounded K04 commissioning-mask copy-slip diagnostic (Agent 3).

The route sheet is a transcription. Keep the selected last-ACK ESC-N printer
payload fixed; remove one original mask byte (or nibble) and reinsert any
replacement byte (or nibble) anywhere. Compare the resulting XOR component's
SHA-256 to the original, unchanged K04 acceptance commitment.

The two classes are hypothetical transcription mechanisms. No original
corrected mask has been recovered or authenticated.
"""
import argparse
import configparser
import hashlib
import json
from pathlib import Path
import re


DEFAULT_ROOT = Path(__file__).resolve().parents[1] / "resources"


def byte_slips(mask):
    for cut in range(len(mask)):
        remaining = mask[:cut] + mask[cut + 1:]
        for insert in range(len(mask)):
            for value in range(256):
                yield remaining[:insert] + bytes([value]) + remaining[insert:]


def nibble_slips(mask):
    digits = mask.hex().upper()
    for cut in range(len(digits)):
        remaining = digits[:cut] + digits[cut + 1:]
        for insert in range(len(digits)):
            for digit in "0123456789ABCDEF":
                yield bytes.fromhex(remaining[:insert] + digit + remaining[insert:])


def selected_payload(root):
    routes = configparser.ConfigParser()
    routes.read(root / "evidence/archive-labels.ini")
    job = routes["printer_routes_2026-09-01_to_2026-10-03"]["ESC-N"]
    log = (root / "evidence/print/spool-reconstruction.log").read_text()
    pattern = re.compile(
        r"JOB=(\S+) ATTEMPT=(\d+) STATE=(\S+) CLASS=(\S+) "
        r"PAYLOAD=([0-9A-F]{32})"
    )
    acknowledged = [
        (int(match[2]), bytes.fromhex(match[5]))
        for match in pattern.finditer(log)
        if match[1] == job and match[3] == "ACK" and match[4] == "RECOVER"
    ]
    attempt, payload = max(acknowledged)
    return job, attempt, payload


def run(root):
    routing = json.loads((root / "evidence/recovery-routing.json").read_text())
    acceptance = json.loads((root / "acceptance.json").read_text())
    mask = bytes.fromhex(routing["K04"]["masked_component"])
    target = acceptance["slot_sha256"]["K04"]
    job, attempt, payload = selected_payload(root)

    def component(candidate_mask):
        return bytes(left ^ right for left, right in zip(payload, candidate_mask))

    def slot_digest(candidate_mask):
        return hashlib.sha256(component(candidate_mask)).hexdigest()

    nibble_candidates = set(nibble_slips(mask))
    byte_candidates = set(byte_slips(mask))
    all_candidates = nibble_candidates | byte_candidates
    original_digest = slot_digest(mask)

    # Independent, fixed positive controls supplied by Agent 27. These
    # fixtures were chosen outside the scanner, with expected component bytes
    # and SHA-256 values calculated independently. Acceptance stays untouched.
    fixtures = (
        (
            nibble_candidates,
            "85568CB6140AA7F9A5123AC7571BEE1C",
            "2CFF50E125AF4557228E7DE60B3EB7C9",
            "2472a2caf1d23fdae5e042f627b89acd060f516caf4f61ef257f98551965abce",
        ),
        (
            byte_candidates,
            "8556CB6140A7F9A5123AC7571BEE7E1C",
            "2CFF173671021B0B95A6807647CB27C9",
            "b648d3658a154d440e31193f3ad22d3e0cc1bd32a38b28b91a2d7250086c7a76",
        ),
    )
    for candidates, fixture_mask, expected_component, expected_digest in fixtures:
        candidate = bytes.fromhex(fixture_mask)
        assert candidate in candidates
        assert component(candidate).hex().upper() == expected_component
        assert slot_digest(candidate) == expected_digest

    matches = [
        {"mask": value.hex().upper(), "K04": component(value).hex().upper()}
        for value in all_candidates
        if slot_digest(value) == target
    ]
    return {
        "job": job,
        "ack_attempt": attempt,
        "ack_payload": payload.hex().upper(),
        "original_mask": mask.hex().upper(),
        "original_K04": component(mask).hex().upper(),
        "original_slot_sha256": original_digest,
        "expected_slot_sha256": target,
        "nibble_assignments": len(mask.hex()) ** 2 * 16,
        "nibble_unique": len(nibble_candidates),
        "byte_assignments": len(mask) ** 2 * 256,
        "byte_unique": len(byte_candidates),
        "distinct_union": len(all_candidates),
        "distinct_intersection": len(nibble_candidates & byte_candidates),
        "synthetic_controls": "PASS",
        "matches": matches,
        "status": "PASS" if matches else "NO_MATCH",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    args = parser.parse_args()
    print(json.dumps(run(args.root), indent=2))
