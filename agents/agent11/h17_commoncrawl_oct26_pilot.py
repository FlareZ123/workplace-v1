"""Bounded public Common Crawl index study of BX25/08 correspondence host.

Manual-only, third-party published index. Never contacts a corporate domain or an account.
"""
import json
import time
import urllib.error
import urllib.parse
import urllib.request

INDEX = "https://index.commoncrawl.org"
HEADERS = {"User-Agent": "H17HistoricalIndexResearch/1.0 (public-domain archive verification)"}


def lookup(crawl, pattern):
    query = urllib.parse.urlencode({"url": pattern, "output": "json", "filter": "status:200"})
    url = f"{INDEX}/{crawl}-index?{query}"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=25) as response:
            body = response.read(180_000).decode("utf-8", "replace")
            status = response.status
    except urllib.error.HTTPError as exc:
        body = exc.read(2000).decode("utf-8", "replace")
        status = exc.code
    rows = []
    if status == 200:
        for line in body.splitlines():
            rows.append(json.loads(line))
    print("INDEX", crawl, pattern, "HTTP", status, "COUNT", len(rows), "BODY_HEAD", body[:120] if status != 200 else "", flush=True)
    for row in rows[:30]:
        print("CAPTURE", json.dumps({key: row.get(key) for key in ("timestamp", "url", "status", "mime", "filename", "offset", "length")}, sort_keys=True), flush=True)
    return status, rows


def main():
    status, control = lookup("CC-MAIN-2026-43", "commoncrawl.org/*")
    if status != 200 or not control:
        print("STOP: public index positive capture control unavailable; no source absence claim")
        return
    time.sleep(2)
    status, rows = lookup("CC-MAIN-2026-43", "noyes-energy-group.pages.dev/*")
    if status not in (200, 404):
        print("STOP: Oct public source index unavailable")
        return
    if rows:
        print("SOURCE_WITNESS_FOUND: examine dated public WARC only with independent provenance; metadata alone is not K04 or K08")
        return
    time.sleep(2)
    lookup("CC-MAIN-2026-39", "noyes-energy-group.pages.dev/*")
    print("DONE: historical index metadata observations only; K04/K08 not inferred")


if __name__ == "__main__":
    main()
