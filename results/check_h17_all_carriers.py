"""Read-only exhaustive search of verbatim K04 and K08 carriers including direct component bytes in the local export.

This scanner tests finite extraction hypotheses. A miss does not establish that
the original printer coupon or final desk caption was never created.
"""

from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import re
from pathlib import Path

WORD_RE = re.compile(r"[a-z0-9]+")


def check_k04(payload: bytes, mask: bytes, target: bytes) -> bool:
    component = bytes(a ^ b for a, b in zip(payload, mask))
    return hashlib.sha256(component).digest() == target


def check_k08(words: list[str], nonce: bytes, target: bytes) -> bool:
    component = hmac.digest(nonce, " ".join(words).encode("utf-8"), "sha256")[:16]
    return hashlib.sha256(component).digest() == target


def search(root: Path, target_k04: bytes, target_k08: bytes, *, max_words: int = 40) -> dict:
    routing = json.loads((root / "evidence/recovery-routing.json").read_text(encoding="utf-8"))
    mask = bytes.fromhex(routing["K04"]["masked_component"])
    nonce = bytes.fromhex(routing["K08"]["desk_nonce"])
    counts = {
        "files": 0,
        "k04_raw_windows": 0,
        "k04_hex_windows": 0,
        "k08_word_spans": 0,
        "k08_text_files": 0,
        "k08_skipped_non_utf8": 0,
    }
    hits: list[dict] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.relative_to(root).parts[0] == "results":
            continue
        relative = path.relative_to(root).as_posix()
        payload = path.read_bytes()
        counts["files"] += 1

        for offset in range(max(0, len(payload) - 15)):
            counts["k04_raw_windows"] += 1
            candidate = payload[offset:offset + 16]
            if check_k04(candidate, mask, target_k04):
                hits.append({
                    "slot": "K04", "encoding": "raw", "file": relative,
                    "offset": offset, "payload_hex": candidate.hex().upper(),
                })
            for slot, target in (("K04", target_k04), ("K08", target_k08)):
                if hashlib.sha256(candidate).digest() == target:
                    hits.append({
                        "slot": slot, "encoding": "direct-component-raw",
                        "file": relative, "offset": offset,
                        "component_hex": candidate.hex().upper(),
                    })

        for match in re.finditer(rb"[0-9A-Fa-f]{32,}", payload):
            group = match.group(0)
            for offset in range(len(group) - 31):
                counts["k04_hex_windows"] += 1
                candidate = bytes.fromhex(group[offset:offset + 32].decode("ascii"))
                if check_k04(candidate, mask, target_k04):
                    hits.append({
                        "slot": "K04", "encoding": "hex", "file": relative,
                        "offset": match.start() + offset,
                        "payload_hex": candidate.hex().upper(),
                    })
                for slot, target in (("K04", target_k04), ("K08", target_k08)):
                    if hashlib.sha256(candidate).digest() == target:
                        hits.append({
                            "slot": slot, "encoding": "direct-component-hex",
                            "file": relative, "offset": match.start() + offset,
                            "component_hex": candidate.hex().upper(),
                        })

        try:
            content = payload.decode("utf-8")
        except UnicodeDecodeError:
            counts["k08_skipped_non_utf8"] += 1
            continue
        counts["k08_text_files"] += 1
        # Route semantics: lowercase, replace every non-ASCII alphanumeric or
        # non-whitespace character by a space, collapse whitespace, trim.
        normalized = re.sub(r"[^a-z0-9\s]", " ", content.lower())
        words = WORD_RE.findall(normalized)
        for start in range(len(words)):
            for end in range(start + 1, min(start + max_words, len(words)) + 1):
                counts["k08_word_spans"] += 1
                if check_k08(words[start:end], nonce, target_k08):
                    hits.append({
                        "slot": "K08", "file": relative, "word_start": start,
                        "word_count": end - start,
                        "normalized_caption": " ".join(words[start:end]),
                    })

    return {
        "scope": f"{counts['files']} files, K08 contiguous normalized spans of 1..{max_words} words",
        "counts": counts,
        "hits": hits,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root", type=Path,
        default=Path(__file__).resolve().parents[1] / "resources",
    )
    parser.add_argument("--max-words", type=int, default=40)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.max_words < 1:
        parser.error("--max-words must be positive")

    acceptance = json.loads((args.root / "acceptance.json").read_text(encoding="utf-8"))
    target_k04 = bytes.fromhex(acceptance["slot_sha256"]["K04"])
    target_k08 = bytes.fromhex(acceptance["slot_sha256"]["K08"])
    print(json.dumps(
        search(args.root, target_k04, target_k08, max_words=args.max_words),
        indent=2,
    ))

    if args.self_test:
        routing = json.loads((args.root / "evidence/recovery-routing.json").read_text())
        mask = bytes.fromhex(routing["K04"]["masked_component"])
        nonce = bytes.fromhex(routing["K08"]["desk_nonce"])
        payload = bytes.fromhex("A9A9DC5731A5E2AE879C47215C2559D5")
        phrase = "the sea looks different when you have finally finished your tea"
        synthetic_k04 = hashlib.sha256(
            bytes(a ^ b for a, b in zip(payload, mask))
        ).digest()
        synthetic_k08 = hashlib.sha256(
            hmac.digest(nonce, phrase.encode("utf-8"), "sha256")[:16]
        ).digest()
        controls = search(args.root, synthetic_k04, synthetic_k08, max_words=12)
        assert any(
            hit["slot"] == "K04" and hit["encoding"] == "hex"
            and hit["payload_hex"] == payload.hex().upper()
            for hit in controls["hits"]
        ), "K04 positive control missing"
        assert any(
            hit["slot"] == "K08" and hit["normalized_caption"] == phrase
            for hit in controls["hits"]
        ), "K08 positive control missing"
        print("K04 coupon and K08 caption positive controls: PASS")
        raw_component = b"# printer buffer"
        hex_component = bytes.fromhex("FBBBC54356483F5864BB3F06794518A5")
        direct = search(
            args.root,
            hashlib.sha256(raw_component).digest(),
            hashlib.sha256(hex_component).digest(),
            max_words=1,
        )
        assert any(
            hit["slot"] == "K04" and hit["encoding"] == "direct-component-raw"
            and hit["file"] == "evidence/print/spool-reconstruction.log"
            and hit["offset"] == 0
            for hit in direct["hits"]
        ), "K04 direct-component raw positive control missing"
        assert any(
            hit["slot"] == "K08" and hit["encoding"] == "direct-component-hex"
            and hit["file"] == "evidence/print/spool-reconstruction.log"
            and hit["component_hex"] == hex_component.hex().upper()
            for hit in direct["hits"]
        ), "K08 direct-component hex positive control missing"
        print("K04/K08 direct-component positive controls: PASS")


if __name__ == "__main__":
    main()
