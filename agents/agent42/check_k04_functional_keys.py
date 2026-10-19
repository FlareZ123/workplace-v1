"""Read-only K04 printer metadata functional-key falsifier. No REC8 hash read.

Usage: python agents/agent42/check_k04_functional_keys.py resources
Alternatively pass original case ZIP path.
"""
import argparse
import itertools
from collections import defaultdict
from pathlib import Path
from zipfile import ZipFile

FIELDS = ("ATTEMPT", "CLASS", "STATE", "DEST")


def load_rows(source):
    if source.is_file():
        with ZipFile(source) as archive:
            data = archive.read("evidence/print/spool-reconstruction.log").decode("utf-8")
    else:
        data = (source / "evidence/print/spool-reconstruction.log").read_text(encoding="utf-8")
    rows = []
    for line_number, line in enumerate(data.splitlines(), 1):
        if not line.strip() or line.startswith("#"):
            continue
        timestamp, *pairs = line.split()
        row = {"TIMESTAMP": timestamp, "LINE": line_number}
        row.update(pair.split("=", 1) for pair in pairs)
        rows.append(row)
    return rows


def conflicts(rows, fields):
    by_key = defaultdict(list)
    for row in rows:
        by_key[tuple(row[field] for field in fields)].append(row)
    return [group for group in by_key.values()
            if len({row["PAYLOAD"] for row in group}) > 1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    args = parser.parse_args()
    rows = load_rows(args.source)
    assert len(rows) == 133

    # A synthetic positive/negative detector pair before original evidence.
    assert len(conflicts([{"JOB": "x", "PAYLOAD": "A"},
                          {"JOB": "x", "PAYLOAD": "B"}], ("JOB",))) == 1
    assert not conflicts([{"JOB": "x", "PAYLOAD": "A"},
                          {"JOB": "x", "PAYLOAD": "A"}], ("JOB",))

    candidate_keys = []
    for count in range(len(FIELDS) + 1):
        for fields in itertools.combinations(FIELDS, count):
            key = ("JOB",) + fields
            failures = conflicts(rows, key)
            print(",".join(key), "conflicting groups", len(failures))
            if failures:
                print(" example lines", [row["LINE"] for row in failures[0]])
            elif not any(previous.issubset(set(key)) for previous in candidate_keys):
                candidate_keys.append(set(key))

    minimal = [tuple(field for field in ("JOB",) + FIELDS if field in keys)
               for keys in candidate_keys]
    print("minimal conflict-free keys:", minimal)
    assert minimal == [("JOB", "ATTEMPT", "CLASS"),
                       ("JOB", "ATTEMPT", "STATE")]
    assert [row["LINE"] for row in conflicts(
        rows, ("JOB", "CLASS", "STATE", "DEST"))[0]] == [130, 132]
    print("PASS; original K04 commitment was not consulted")


if __name__ == "__main__":
    main()
