"""Source-preserving positive and negative controls for unchanged REC8/1 verifier.

Synthetic acceptance hashes are in memory only and never written to resources.
This proves the checker accepts a complete internally consistent inventory; it
does not recover missing K04 or K08 original secrets.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "resources"


def main() -> None:
    spec = importlib.util.spec_from_file_location("h17_original_verifier", ROOT / "verify.py")
    assert spec is not None and spec.loader is not None
    verify = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(verify)

    original = json.loads((ROOT / "acceptance.json").read_text(encoding="utf-8"))
    baseline = json.loads((Path(__file__).with_name("h17-candidate.json")).read_text(encoding="utf-8"))
    check = verify.evaluate(baseline, original)
    assert check["passed"] == 6 and check["combined"] == "INCOMPLETE" and not check["accepted"]
    assert check["slots"]["K04"] == check["slots"]["K08"] == "MISSING"

    synthetic_inventory = original.copy()
    synthetic_inventory["slot_sha256"] = original["slot_sha256"].copy()
    complete = baseline.copy()
    for slot, payload in (("K04", bytes(range(16))), ("K08", bytes(range(16, 32)))):
        complete[slot] = payload.hex().upper()
        synthetic_inventory["slot_sha256"][slot] = hashlib.sha256(payload).hexdigest()
    joined = synthetic_inventory["combined_prefix"] + "".join(
        complete[f"K{i:02d}"] + "\n" for i in range(1, 9)
    )
    synthetic_inventory["combined_sha256"] = hashlib.sha256(joined.encode("ascii")).hexdigest()

    accepted = verify.evaluate(complete, synthetic_inventory)
    assert accepted["passed"] == 8 and accepted["combined"] == "PASS" and accepted["accepted"]

    invalid = complete.copy()
    invalid["K04"] = ("F" if invalid["K04"][0] != "F" else "E") + invalid["K04"][1:]
    rejected = verify.evaluate(invalid, synthetic_inventory)
    assert not rejected["accepted"] and rejected["slots"]["K04"] == "NO_MATCH"
    assert rejected["combined"] == "NO_MATCH"

    original_rejection = verify.evaluate(complete, original)
    assert original_rejection["slots"]["K04"] == original_rejection["slots"]["K08"] == "NO_MATCH"
    assert not original_rejection["accepted"]

    print("Synthetic accepted-complete control: PASS")
    print("Synthetic bad-component rejection: PASS")
    print("Original commitment rejection of fabricated components: PASS")
    print("Original six-slot incomplete result: PASS")


if __name__ == "__main__":
    main()
