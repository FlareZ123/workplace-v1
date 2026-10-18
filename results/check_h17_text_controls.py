"""Audit byte-level text carriers in the original H-17 resources.

Read-only, Python 3 standard library. Run from a repository checkout; no
evidence writes. In-memory controls verify that detection rules are active.
"""
from collections import Counter
from pathlib import Path
import argparse
import json

ROOT = Path(__file__).resolve().parents[1] / "resources"


def inspect(payload):
    text = payload.decode("utf-8")
    return {
        "non_ascii": dict(Counter(f"U+{ord(ch):04X}" for ch in text if ord(ch) > 127)),
        "controls_except_lf": dict(Counter(
            f"U+{ord(ch):04X}" for ch in text if ord(ch) < 32 and ch != "\n"
        )),
        "utf8_bom": payload.startswith(b"\xef\xbb\xbf"),
        "trailing_whitespace_lines": sum(
            line != line.rstrip(" \t") for line in text.split("\n")
        ),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT,
                        help="Extracted original ZIP root, or current repository resources")
    args = parser.parse_args()
    assert inspect(b"x\xe2\x80\x8by")["non_ascii"] == {"U+200B": 1}
    assert inspect(b"a\tb")["controls_except_lf"] == {"U+0009": 1}
    assert inspect(b"a \n")["trailing_whitespace_lines"] == 1
    assert inspect(b"\xef\xbb\xbf")["utf8_bom"] is True

    manifest = json.loads(
        Path(__file__).with_name("h17-source-blob-manifest.json").read_text(encoding="utf-8")
    )
    source_paths = {item["path"] for item in manifest["files"]}
    discovered = sorted(p for p in args.root.rglob("*") if p.is_file())
    sources = [
        p for p in discovered
        if p.relative_to(args.root).as_posix() in source_paths
    ]
    present = {p.relative_to(args.root).as_posix() for p in sources}
    missing = source_paths - present
    if missing not in (set(), {"AGENT_PROMPT.txt"}):
        raise ValueError(f"Missing original source paths: {sorted(missing)}")
    reports = {}
    for path in sources:
        if path.name == "trip-recorder.raw":
            continue  # Binary TRP2; control bytes here are ordinary data.
        report = inspect(path.read_bytes())
        if report["non_ascii"] or report["controls_except_lf"] or (
            report["utf8_bom"] or report["trailing_whitespace_lines"]
        ):
            reports[path.relative_to(args.root).as_posix()] = report
    result = {
        "input_files": len(sources),
        "ignored_non_source_files": len(discovered) - len(sources),
        "utf8_text_files": len(sources) - 1,
        "text_files_with_unusual_bytes": reports,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
