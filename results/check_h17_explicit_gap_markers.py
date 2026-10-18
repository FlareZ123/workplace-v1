"""Enumerate explicit omission markers in the original H-17 local export.

A negative result does not establish completeness: the custodian explicitly
warns that unmarked export gaps are possible. This script is read-only.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import sys
from zipfile import ZipFile

OMISSION = re.compile(r"\bomitted\b|\bnot included\b|\bexport gap\b|\bextraction gap\b", re.I)
BRACKET = re.compile(r"\[([^\]\n]{1,120})\]")


def source_files(path: Path) -> list[tuple[str, bytes]]:
    manifest = json.loads(
        Path(__file__).with_name("h17-source-blob-manifest.json").read_text(encoding="utf-8")
    )
    source_paths = {item["path"] for item in manifest["files"]}

    def require_sources(present: set[str], *, allow_instructions_omission: bool) -> None:
        missing = source_paths - present
        if missing and not (
            allow_instructions_omission and missing == {"AGENT_PROMPT.txt"}
        ):
            raise ValueError(f"Missing original source paths: {sorted(missing)}")

    if path.is_file():
        with ZipFile(path) as archive:
            names = [name for name in archive.namelist() if name in source_paths]
            if len(names) != len(set(names)):
                raise ValueError("Duplicate original source path in ZIP")
            require_sources(set(names), allow_instructions_omission=False)
            return [(name, archive.read(name)) for name in names]

    selected = [
        f for f in sorted(path.rglob("*"))
        if f.is_file() and f.relative_to(path).as_posix() in source_paths
    ]
    require_sources(
        {f.relative_to(path).as_posix() for f in selected},
        allow_instructions_omission=True,
    )
    return [(f.relative_to(path).as_posix(), f.read_bytes()) for f in selected]

def census(path: Path) -> dict:
    files = source_files(path)
    omission_lines = []
    brackets = []
    redactions = 0
    ellipses = []
    text_count = 0
    for name, content in files:
        try:
            decoded = content.decode("utf-8")
        except UnicodeDecodeError:
            continue
        text_count += 1
        for number, line in enumerate(decoded.splitlines(), 1):
            if OMISSION.search(line):
                omission_lines.append({"path": name, "line": number, "text": line})
            redactions += line.count("[censored]")
            if "..." in line:
                ellipses.append({"path": name, "line": number})
            if name.startswith("evidence/") and name != "evidence/archive-labels.ini":
                for match in BRACKET.finditer(line):
                    if match.group(1) != "censored":
                        brackets.append({"path": name, "line": number, "marker": match.group()})
    return {"members": len(files), "utf8_members": text_count,
            "redaction_token_count": redactions,
            "explicit_omission_lines": omission_lines,
            "nonredaction_bracket_markers_in_evidence": brackets,
            "three_dot_ellipsis_lines": ellipses}


def main() -> None:
    default = Path(__file__).resolve().parents[1] / "resources"
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else default
    report = census(path)
    if path.is_file():
        report["source_zip_sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
