"""Read-only source-linked urlscan.io public archive index probe.

Only probes published scan metadata for the historically source-linked company host.
Never scans a new URL, signs in, follows private/admin routes, or probes live APIs.
"""
import json
import urllib.error
import urllib.parse
import urllib.request

HOST = "noyes-energy-group.pages.dev"
QUERIES = (f"page.domain:{HOST}", f"domain:{HOST}")
UA = "H17-preservation-public-archive-index/1.0"


def read_public_index(query):
    url = "https://urlscan.io/api/v1/search/?" + urllib.parse.urlencode(
        {"q": query, "size": "100"}
    )
    request = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(request, timeout=25) as response:
            raw = response.read(2_000_000)
            return response.status, response.headers.get("Date"), raw, url
    except urllib.error.HTTPError as exc:
        return exc.code, exc.headers.get("Date"), exc.read(500), url


def parse_public_results(raw):
    obj = json.loads(raw)
    if not isinstance(obj, dict):
        raise ValueError("urlscan response must be JSON object")
    rows = obj.get("results", [])
    if not isinstance(rows, list):
        raise ValueError("urlscan results must be list")
    output = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        task = row.get("task") or {}
        page = row.get("page") or {}
        target = task.get("url") or page.get("url") or ""
        if not isinstance(target, str):
            continue
        split = urllib.parse.urlsplit(target)
        if split.hostname != HOST or split.path.startswith(("/admin", "/api")):
            continue
        output.append({
            "task_time": task.get("time"),
            "target": target,
            "scan_id": row.get("_id"),
            "scan_page": row.get("result"),
            "page_title": page.get("title"),
        })
    return obj.get("total", 0), output


def test_parser():
    fixture = {"total": 3, "results": [
        {"task": {"time": "2026-10-01T00:00:00Z", "url": "https://" + HOST + "/public"}},
        {"task": {"url": "https://" + HOST + "/admin"}},
        {"task": {"url": "https://other.example/public"}},
    ]}
    total, rows = parse_public_results(json.dumps(fixture).encode())
    assert total == 3 and len(rows) == 1 and rows[0]["target"].endswith("/public")
    print("SYNTHETIC_PARSER_POSITIVE_CONTROL: PASS")


def main():
    test_parser()
    for query in QUERIES:
        try:
            status, date, raw, url = read_public_index(query)
            print("QUERY", query, "HTTP", status, "SERVER_DATE", date, "INDEX_URL", url)
            if status == 200:
                total, matches = parse_public_results(raw)
                print("PUBLISHED_MATCHES", total, "IN_SCOPE_PUBLIC_RESULTS", len(matches))
                for row in matches:
                    print("ARCHIVED_PUBLIC_SCAN", json.dumps(row, sort_keys=True))
            else:
                print("INDEX_UNAVAILABLE", raw.decode("utf-8", "replace")[:300])
        except (ValueError, TimeoutError, OSError, json.JSONDecodeError) as exc:
            print("INDEX_ERROR", type(exc).__name__, str(exc)[:300])


if __name__ == "__main__":
    main()
