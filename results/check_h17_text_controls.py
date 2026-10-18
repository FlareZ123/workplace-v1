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

    sources = sorted(p for p in args.root.rglob("*") if p.is_file())
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
        "utf8_text_files": len(sources) - 1,
        "text_files_with_unusual_bytes": reports,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
