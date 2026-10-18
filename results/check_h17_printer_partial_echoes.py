"""Check whether the recorded K04 ACK has redundant literal fragments in the 43 original members.

This is a read-only source-context test; a negative result cannot recover an
unknown historical original that differs from the recorded fragment.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re

SPOOL = "evidence/print/spool-reconstruction.log"
EXPECTED_SHA256 = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"


def longest_echo(fragment: bytes, sources: dict[str, bytes]):
    last_matches: list[tuple[int, str]] = []
    maximum = 0
    for size in range(1, len(fragment) + 1):
        matches = [
            (start, name)
            for start in range(len(fragment) - size + 1)
            for name, contents in sources.items()
            if fragment[start:start + size] in contents
        ]
        if not matches:
            break
        maximum = size
        last_matches = matches
    return maximum, last_matches


def load_source_members(root: Path) -> tuple[dict[str, bytes], int]:
    """Limit the comparison corpus to preserved original source paths only.

    The original ZIP has 43 members; the current repository checkout has 42,
    following the documented AGENT_PROMPT.txt deletion. Generated working
    copies beside a case extraction are never evidence.
    """
    manifest_path = Path(__file__).with_name("h17-source-blob-manifest.json")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    source_paths = {item["path"] for item in manifest["files"]}
    discovered = sorted(p for p in root.rglob("*") if p.is_file())
    members = {
        relative: p.read_bytes()
        for p in discovered
        if (relative := p.relative_to(root).as_posix()) in source_paths
    }
    missing = source_paths - members.keys()
    if missing not in (set(), {"AGENT_PROMPT.txt"}):
        raise ValueError(f"Missing original source paths: {sorted(missing)}")
    return members, len(discovered) - len(members)


def run(root: Path) -> None:
    members, ignored = load_source_members(root)
    print(f"Source members: {len(members)}; ignored generated files: {ignored}")
    spool = members[SPOOL]
    assert hashlib.sha256(spool).hexdigest() == EXPECTED_SHA256
    selected = []
    remaining = []
    for line in spool.splitlines(keepends=True):
        if (b"JOB=PS-261003-0417" in line and b"ATTEMPT=2" in line
                and b"STATE=ACK" in line and b"CLASS=RECOVER" in line):
            selected.append(line)
        else:
            remaining.append(line)
    assert len(selected) == 1
    match = re.search(rb"PAYLOAD=([0-9A-F]{32})", selected[0])
    assert match is not None
    payload = bytes.fromhex(match.group(1).decode("ascii"))
    members[SPOOL] = b"".join(remaining)
    different_members = {name: content for name, content in members.items() if name != SPOOL}

    # Synthetic echo validates the exact comparison code in both forms.
    assert longest_echo(payload, {"synthetic": b"\0" + payload + b"\0"})[0] == 16
    assert longest_echo(payload.hex().upper().encode("ascii"),
                        {"synthetic": b"#" + payload.hex().upper().encode("ascii")})[0] == 32

    for scope, corpus in (("all sources except selected line", members),
                          ("other members only", different_members)):
        for encoding, fragment in (
            ("raw bytes", payload),
            ("uppercase hexadecimal", payload.hex().upper().encode("ascii")),
            ("lowercase hexadecimal", payload.hex().lower().encode("ascii")),
        ):
            size, matches = longest_echo(fragment, corpus)
            print(scope, encoding, "maximum length", size, "example matches", matches[:8])
        normalized_corpus = {name: content.upper() for name, content in corpus.items()}
        size, matches = longest_echo(payload.hex().upper().encode("ascii"), normalized_corpus)
        print(scope, "case-insensitive hexadecimal", "maximum length", size,
              "example matches", matches[:8])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    run(parser.parse_args().root)
