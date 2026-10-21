"""One-shot, anonymous MemGator discovery of independently dated public original pages.

The original 2025 BX25/08 property folio names the domain. This script does not
guess URLs, log in, submit forms, or read the disputed K04/K08 commitments.
"""
from __future__ import annotations

import fcntl
import json
import os
import tempfile
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


SERVICE = "https://memgator.cs.odu.edu/timemap/json/"
ORIGINALS = (
    "https://noyes-energy-group.pages.dev/",
    "http://noyes-energy-group.pages.dev/",
)
CONTROL = "https://example.com/"
CUT_OFF = datetime(2026, 10, 4, tzinfo=timezone.utc)
OUT = Path("h17-memgator-original-witness.json")


def capture_time(value: str) -> datetime:
    try:
        return parsedate_to_datetime(value).astimezone(timezone.utc)
    except (ValueError, TypeError):
        return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


def inventory(original: str) -> dict:
    url = SERVICE + original
    try:
        with urlopen(Request(url, headers={"User-Agent": "H17-readonly-original-index/1.0"}),
                     timeout=45) as reply:
            body = reply.read(2_000_001)
            status = reply.status
    except (HTTPError, URLError, TimeoutError) as error:
        return {"original": original, "error": str(error)}
    if len(body) > 2_000_000:
        return {"original": original, "error": "timetable exceeds 2 MB"}
    try:
        data = json.loads(body)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        return {"original": original, "status": status, "error": str(error)}
    records = data.get("mementos", {}).get("list", [])
    before = []
    malformed = 0
    for record in records:
        try:
            when = capture_time(record["datetime"])
        except (KeyError, ValueError, TypeError):
            malformed += 1
            continue
        if when < CUT_OFF:
            before.append({"datetime": when.isoformat(), "uri": record.get("uri", "")})
    return {
        "original": original,
        "status": status,
        "total": len(records),
        "pre_incident_count": len(before),
        "pre_incident_recent": sorted(before, key=lambda e: e["datetime"], reverse=True)[:30],
        "unparsed_dates": malformed,
    }


def main() -> None:
    results = {
        "type": "anonymous-public-archive-index-only",
        "historical_cutoff_utc": CUT_OFF.isoformat(),
        "queries": [inventory(CONTROL)] + [inventory(item) for item in ORIGINALS],
    }
    for item in results["queries"]:
        print(json.dumps({
            "original": item["original"],
            "status": item.get("status"),
            "total": item.get("total"),
            "pre_incident_count": item.get("pre_incident_count"),
            "error": item.get("error"),
        }), flush=True)
    with open(str(OUT) + ".lock", "w", encoding="utf-8") as guard:
        fcntl.flock(guard.fileno(), fcntl.LOCK_EX)
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=".", delete=False) as tmp:
            json.dump(results, tmp, indent=2)
            tmp.write("\n")
            tmp_name = tmp.name
        os.replace(tmp_name, OUT)


if __name__ == "__main__":
    main()
