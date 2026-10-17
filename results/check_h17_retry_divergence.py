"""Read-only byte divergence check for retained H-17 ESC-N RECOVER attempts."""
import hashlib
import itertools
import json
import re
from pathlib import Path

SOURCE_SHA256 = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"
PATTERN = re.compile(r"ATTEMPT=(\d+) STATE=(\w+) CLASS=(\w+) PAYLOAD=([0-9A-F]{32})")


def analyze(root: Path) -> dict:
    src = root / "evidence" / "print" / "spool-reconstruction.log"
    raw = src.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != SOURCE_SHA256:
        raise ValueError(f"Source digest mismatch: {digest}")

    records = []
    for line in raw.decode("ascii").splitlines():
        if "JOB=PS-261003-0417" not in line:
            continue
        match = PATTERN.search(line)
        if match is None:
            raise ValueError(f"Malformed retained job line: {line}")
        attempt, state, klass, payload = match.groups()
        records.append({"attempt": int(attempt), "state": state, "class": klass, "payload": payload})

    recover = [r for r in records if r["class"] == "RECOVER"]
    if len(recover) != 3 or {r["attempt"] for r in recover} != {1, 2, 3}:
        raise ValueError("Unexpected RECOVER attempt inventory")

    pairs = []
    for left, right in itertools.combinations(recover, 2):
        a, b = bytes.fromhex(left["payload"]), bytes.fromhex(right["payload"])
        pairs.append({
            "attempts": [left["attempt"], right["attempt"]],
            "different_byte_positions": sum(x != y for x, y in zip(a, b)),
            "different_bits": sum((x ^ y).bit_count() for x, y in zip(a, b)),
        })

    consensus_positions = sum(
        len({bytes.fromhex(r["payload"])[i] for r in recover}) == 1 for i in range(16)
    )
    routing = json.loads((root / "evidence" / "recovery-routing.json").read_text(encoding="utf-8"))
    mask = bytes.fromhex(routing["K04"]["masked_component"])
    selected = next(r for r in recover if r["state"] == "ACK")
    derived = bytes(x ^ y for x, y in zip(bytes.fromhex(selected["payload"]), mask))
    targets = json.loads((root / "acceptance.json").read_text(encoding="utf-8"))
    digest_derived = hashlib.sha256(derived).hexdigest()
    return {
        "source_sha256": digest,
        "recover_attempts": recover,
        "pairwise_comparison": pairs,
        "unanimous_byte_positions": consensus_positions,
        "written_rule_derived_K04": derived.hex().upper(),
        "written_rule_sha256": digest_derived,
        "commitment_pass": digest_derived == targets["slot_sha256"]["K04"],
    }


if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent
    case = root / "resources" if (root / "resources").is_dir() else root
    print(json.dumps(analyze(case), indent=2))
