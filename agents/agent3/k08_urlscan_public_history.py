"""Read-only urlscan public history query for the PDF-attested Noyes hostname.

Searches existing publicly archived scans only. Does not submit URLs for scans,
make any request to the Noyes host, use account credentials, or enter portals.
Logs source URL, scan timestamp, exact response SHA256 and target keyword hits.
"""
from __future__ import annotations

import hashlib
import html
import json
import re
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

HOST = "noyes-energy-group.pages.dev"
API = "https://urlscan.io"
TARGET = re.compile(
    r"H[- ]?17|261003|ESC[- ]?N|PS-261003-0417|BX25|FA-17|"
    r"RECOVER|keeper|Emily|late watch|desk margin",
    re.IGNORECASE,
)


def retrieve(path: str, limit: int = 2_000_000) -> bytes | None:
    assert path.startswith("/") and not path.startswith("//"), path
    url = API + path
    try:
        request = Request(url, headers={"User-Agent": "H17-original-public-archive-index/1.0"})
        with urlopen(request, timeout=18) as response:
            raw = response.read(limit + 1)
            if len(raw) > limit:
                print("OVER_LIMIT", url, len(raw), flush=True)
                return None
            print("FETCH", response.status, response.url, len(raw),
                  hashlib.sha256(raw).hexdigest(), flush=True)
            return raw
    except (HTTPError, URLError) as err:
        print("UNAVAILABLE", url, type(err).__name__, str(err)[:180], flush=True)
        return None


def public_published_page(url: str) -> bool:
    parsed = urlparse(url)
    return (parsed.scheme == "https" and parsed.hostname == HOST
            and parsed.port is None and not parsed.username and not parsed.password
            and not parsed.path.startswith(("/admin", "/api/")))


def main() -> None:
    query = urlencode({"q": "domain:" + HOST, "size": "100"})
    raw = retrieve("/api/v1/search/?" + query)
    if raw is None:
        print("SOURCE_INDEX_UNAVAILABLE; no recovery inference")
        return
    try:
        answer = json.loads(raw)
    except json.JSONDecodeError:
        print("SOURCE_INDEX_NON_JSON; no recovery inference")
        return
    results = answer.get("results", [])
    print("SCAN_COUNT", answer.get("total"), "RETURNED", len(results))
    historical = []
    for hit in results:
        task = hit.get("task", {})
        page = hit.get("page", {})
        url = page.get("url") or task.get("url") or ""
        when = task.get("time", "unknown")
        scan_id = hit.get("_id", "")
        print("SCAN", when, url, scan_id)
        if (public_published_page(url) and
                re.fullmatch(r"[0-9a-f-]{36}", scan_id or "")):
            historical.append((when, url, scan_id))
    # Fetch at most 12 already published public DOM snapshots; no live site visit.
    for when, url, scan_id in historical[:12]:
        dom = retrieve("/dom/" + scan_id + "/")
        if dom is None:
            continue
        cleaned = re.sub(r"<[^>]+>", " ", dom.decode("utf-8", "replace"))
        cleaned = html.unescape(cleaned)
        matches = sorted({m.group(0).lower() for m in TARGET.finditer(cleaned)})
        print("PUBLIC_SNAPSHOT", when, url, "MARKERS", matches,
              "DOM_SHA256", hashlib.sha256(dom).hexdigest())
        if matches:
            for match in list(TARGET.finditer(cleaned))[:6]:
                lo, hi = match.span()
                print("SOURCE_CONTEXT", re.sub(r"\s+", " ", cleaned[max(0, lo-90):hi+140]))
    print("SOURCE_ACQUISITION_COMPLETE", len(historical),
          "published scans; no claim of REC8 acceptance")


if __name__ == "__main__":
    main()
