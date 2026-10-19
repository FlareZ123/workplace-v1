"""Read-only source-rooted test of the two preregistered K08 caption sets."""
from pathlib import Path
import hashlib
import hmac
import json
import re

ROOT = Path(__file__).resolve().parents[2]
ROUTING = json.loads((ROOT / "resources/evidence/recovery-routing.json").read_text(encoding="utf-8"))
ACCEPTANCE = json.loads((ROOT / "resources/acceptance.json").read_text(encoding="utf-8"))
NONCE = bytes.fromhex(ROUTING["K08"]["desk_nonce"])
TARGET = ACCEPTANCE["slot_sha256"]["K08"]
FILES = [
    ROOT / "agents/agent12/k08-new-natural-prerank-20261019.md",
    ROOT / "agents/agent12/k08-empty-bench-prerank.md",
]


def normalized(phrase: str) -> str:
    return " ".join(re.sub(r"[^a-z0-9\s]", " ", phrase.lower()).split())


def component(phrase: str) -> bytes:
    return hmac.new(NONCE, normalized(phrase).encode("utf-8"), hashlib.sha256).digest()[:16]


def candidates(file_path: Path) -> list[str]:
    return [
        line.partition(". ")[2]
        for line in file_path.read_text(encoding="utf-8").splitlines()
        if re.fullmatch(r"\d+\. .+", line)
    ]


def main() -> None:
    phrases = [phrase for file_path in FILES for phrase in candidates(file_path)]
    assert [len(candidates(f)) for f in FILES] == [40, 12]
    assert len({normalized(phrase) for phrase in phrases}) == len(phrases)
    assert component("A good watch leaves the room ready for the next pair of hands.").hex().upper() == "BF889359B0303F2B2B2FD96AE841210B"
    matches = [
        {"rank": index, "phrase": phrase, "K08": component(phrase).hex().upper()}
        for index, phrase in enumerate(phrases, 1)
        if hashlib.sha256(component(phrase)).hexdigest() == TARGET
    ]
    print(json.dumps({
        "candidate_count": len(phrases),
        "per_set_count": [len(candidates(f)) for f in FILES],
        "set_sha256": [hashlib.sha256("\n".join(candidates(f)).encode("utf-8")).hexdigest() for f in FILES],
        "matched": matches,
        "result": "PASS" if matches else "NO_MATCH",
    }, indent=2))


if __name__ == "__main__":
    main()
