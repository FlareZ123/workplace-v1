"""Read-only precommitted 24-caption K08 acceptance experiment.

Run: python agents/agent28/check_k08_cup_transition.py resources
The case is offline and the source files and original verifier remain unchanged.
"""
from pathlib import Path
import hashlib
import hmac
import json
import re
import sys


def main() -> None:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("resources")
    note = Path(__file__).with_name("k08-cup-transition-prerank-20261019.md").read_text(encoding="utf-8")
    numbered = re.findall(r"(?m)^(\d+)\. (.+)$", note)
    assert [int(n) for n, _ in numbered] == list(range(1, 25))
    phrases = [phrase for _, phrase in numbered]
    fingerprint = hashlib.sha256("\n".join(phrases).encode()).hexdigest()
    assert fingerprint == "c9e69f66e6b345172a069c0cdd83faacc021b738d3ad4e3178b9f4b92cb062e5"

    k08 = json.loads((root / "evidence/recovery-routing.json").read_text())["K08"]
    target = json.loads((root / "acceptance.json").read_text())["slot_sha256"]["K08"]
    nonce = bytes.fromhex(k08["desk_nonce"])

    def component(phrase: str) -> bytes:
        normalized = " ".join(re.sub(r"[^a-z0-9\s]", " ", phrase.lower()).split())
        return hmac.new(nonce, normalized.encode("utf-8"), hashlib.sha256).digest()[:16]

    assert component("A good watch leaves the room ready for the next pair of hands.").hex().upper() == "BF889359B0303F2B2B2FD96AE841210B"
    hits = [(n, phrase, component(phrase).hex().upper()) for n, phrase in numbered if hashlib.sha256(component(phrase)).hexdigest() == target]
    print(json.dumps({
        "preranked_count": len(phrases),
        "list_sha256": fingerprint,
        "first_candidate_component": component(phrases[0]).hex().upper(),
        "hits": hits,
        "original_target_unchanged": target == "285eb6b4196d21eaf47e251449e61e0bce28749881ccc5a065ca733b0c3fd747"
    }, indent=2))


if __name__ == "__main__":
    main()
