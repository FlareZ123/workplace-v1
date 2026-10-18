"""Test one uniformly shifted mail-Date-header clock against original H-17 events."""
import json
import re
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "resources"


def mail_date(number):
    text = (ROOT / f"evidence/mail/{number:02d}.eml").read_text(encoding="utf-8")
    return parsedate_to_datetime(re.search(r"(?m)^Date: (.+)$", text).group(1))


def source_times():
    start = (ROOT / "START_HERE.md").read_text(encoding="utf-8")
    prepared = re.search(r"(?m)^Prepared: (.+)$", start).group(1)
    export_time = datetime.strptime(prepared, "%d %B %Y, %H:%M UTC").replace(tzinfo=timezone.utc)
    transfers = [json.loads(s) for s in
                 (ROOT / "evidence/transfers/transfer-audit.jsonl").read_text().splitlines()]
    commit = [x for x in transfers if x.get("kind") == "COMMIT"
              and x.get("transfer") == "AX-7782" and x.get("dry_run") is False]
    assert len(commit) == 1
    transfer_time = datetime.fromisoformat(commit[0]["receipt_utc"].replace("Z", "+00:00"))
    requests = []
    for line in (ROOT / "evidence/print/spool-reconstruction.log").read_text().splitlines():
        fields = dict(re.findall(r"([A-Z]+)=([^ ]+)", line))
        if all(fields.get(k) == v for k, v in {
            "JOB": "PS-261003-0417", "ATTEMPT": "3",
            "STATE": "REQUESTED", "CLASS": "RECOVER"
        }.items()):
            requests.append(datetime.fromisoformat(line.split()[0].replace("Z", "+00:00")))
    assert len(requests) == 1
    return {"mail13": mail_date(13), "commit": transfer_time, "mail16": mail_date(16),
            "request": requests[0], "mail20": mail_date(20), "prepared": export_time}


def bounds(t):
    minimum = max(t["commit"] - t["mail13"], t["request"] - t["mail16"])
    maximum = t["prepared"] - t["mail20"]
    return minimum, maximum, minimum <= maximum


if __name__ == "__main__":
    actual = source_times()
    lower, upper, possible = bounds(actual)
    print("minimum clock correction:", lower)
    print("maximum clock correction:", upper)
    print("single uniform correction possible:", possible)
    assert lower == timedelta(days=1, hours=10, minutes=59, seconds=10)
    assert upper == timedelta(minutes=34)
    assert not possible
    synthetic = actual.copy()
    synthetic["mail13"] = synthetic["commit"] - timedelta(minutes=1)
    synthetic["mail16"] = synthetic["request"] - timedelta(minutes=1)
    synthetic["mail20"] = synthetic["prepared"] - timedelta(minutes=5)
    assert bounds(synthetic)[2], "positive-control chronology rejected"
    print("positive-control chronology: PASS")
