"""Read-only cohort/identity audit of the H-17 printer reconstruction.

The timestamp serialization boundary and reused job/attempt identity are
observable facts. They imply no corrected coupon bytes or corruption model.
Python 3 standard library only; run from a repository checkout.
"""
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1] / "resources"
SPOOL = ROOT / "evidence/print/spool-reconstruction.log"
PATTERN = re.compile(
    r"^(?P<time>\S+) JOB=(?P<job>\S+) ATTEMPT=(?P<attempt>\d+)"
    r" STATE=(?P<state>\S+) CLASS=(?P<klass>\S+)"
    r" PAYLOAD=(?P<payload>[0-9A-F]{32}) DEST=(?P<dest>\S+)$"
)


def main():
    lines = SPOOL.read_text(encoding="ascii").splitlines()
    assert len(lines) == 134 and lines[0].startswith("# printer buffer")
    rows = []
    for line_no, line in enumerate(lines[1:], 2):
        match = PATTERN.fullmatch(line)
        assert match, f"Malformed spool entry at {line_no}"
        row = match.groupdict()
        row["line"] = line_no
        row["style"] = "Z" if row["time"].endswith("Z") else "+00:00"
        assert row["time"].endswith(("Z", "+00:00"))
        row["dt"] = datetime.fromisoformat(row["time"])
        rows.append(row)

    standard = [r for r in rows if r["style"] == "+00:00"]
    late = [r for r in rows if r["style"] == "Z"]
    assert len(standard) == 128 and len(late) == 5
    assert all(r["state"] == "ACK" and int(r["attempt"]) == 1 for r in standard)
    assert all(r["klass"] == "RECOVER" for r in late)
    assert [r["job"] for r in standard] == [
        f"PS-261003-{i:04d}" for i in range(300, 428)
    ]
    assert all(
        standard[i+1]["dt"] - standard[i]["dt"] == timedelta(minutes=5)
        for i in range(len(standard)-1)
    )

    keyed = defaultdict(list)
    for r in rows:
        keyed[(r["job"], r["attempt"])].append({
            "line": r["line"], "state": r["state"], "class": r["klass"],
            "time": r["time"]
        })
    duplicates = [
        {"job": job, "attempt": attempt, "rows": items}
        for (job, attempt), items in sorted(keyed.items()) if len(items) > 1
    ]
    assert len(duplicates) == 1
    assert (duplicates[0]["job"], duplicates[0]["attempt"]) == (
        "PS-261003-0417", "1"
    )

    selected = [
        r for r in rows if r["job"] == "PS-261003-0417"
        and r["klass"] == "RECOVER" and r["state"] == "ACK"
    ]
    assert len(selected) == 1 and selected[0]["attempt"] == "2"
    routes = json.loads((ROOT / "evidence/recovery-routing.json").read_text())
    target = json.loads((ROOT / "acceptance.json").read_text())
    payload = bytes.fromhex(selected[0]["payload"])
    mask = bytes.fromhex(routes["K04"]["masked_component"])
    component = bytes(x ^ y for x,y in zip(payload, mask))
    source_hash = hashlib.sha256(component).hexdigest()
    assert source_hash != target["slot_sha256"]["K04"]

    print(json.dumps({
        "total_entries": len(rows),
        "regular_entries": len(standard),
        "late_entries": len(late),
        "cohorts": {
            "+00:00": dict(Counter(r["klass"] for r in standard)),
            "Z": dict(Counter(f'{r["state"]}/{r["klass"]}' for r in late))
        },
        "duplicate_job_attempt_identifiers": duplicates,
        "selected_k04": {
            "line": selected[0]["line"],
            "payload_hex": payload.hex().upper(),
            "component_hex": component.hex().upper(),
            "component_sha256": source_hash,
            "commitment": "NO_MATCH"
        },
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
