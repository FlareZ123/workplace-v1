"""Check a proposed REC8/1 K08 keeper caption against the original commitment.

Reads only the checked-in local preservation evidence and acceptance inventory.
Passing a proposed phrase authenticates its normalized HMAC-derived component.
It does not establish provenance of the phrase itself.
"""
from __future__ import annotations

import argparse
import hashlib
import hmac
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1] / "resources"


def normalize(phrase: str) -> str:
    """Apply K08's lowercase, ASCII-alphanumeric, whitespace-collapse rule."""
    return " ".join(re.sub(r"[^a-z0-9\s]", " ", phrase.lower()).split())


def test_caption(phrase: str) -> dict[str, str | bool]:
    routing = json.loads((ROOT / "evidence/recovery-routing.json").read_text(encoding="utf-8"))
    inventory = json.loads((ROOT / "acceptance.json").read_text(encoding="utf-8"))
    message = normalize(phrase)
    key = bytes.fromhex(routing["K08"]["desk_nonce"])
    component = hmac.new(key, message.encode("utf-8"), hashlib.sha256).digest()[:16]
    actual = hashlib.sha256(component).hexdigest()
    return {
        "normalized_caption": message,
        "candidate_K08": component.hex().upper(),
        "candidate_sha256": actual,
        "acceptance": "PASS" if actual == inventory["slot_sha256"]["K08"] else "NO_MATCH",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("caption", help="Exact candidate wording to test")
    args = parser.parse_args()
    result = test_caption(args.caption)
    print(json.dumps(result, indent=2))
    return 0 if result["acceptance"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
