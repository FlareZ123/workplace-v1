"""Small read-only pilot for independent pre-export H-17 source witnesses.

Only query a target-bearing identifier if this same index first finds an original
positive-control string from the public H-17 repository. A zero from an index
that misses its known control says nothing about absence of original records.
"""
import json
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

CONTROL = "PS-261003-0417"
TARGET = "930a52a1bab97ca2966332137c99e99298ea6182fb32ab63a3421dfb4fd8c9e0"
HEADERS = {"User-Agent": "H17-Archive-Source-Research/1.0", "Accept": "application/json, text/event-stream"}


def request(url):
    try:
        with urlopen(Request(url, headers=HEADERS), timeout=12) as response:
            return response.read(500000).decode("utf-8", "replace"), response.status
    except (HTTPError, URLError, TimeoutError, OSError) as error:
        return None, str(error)


def grep_app(query):
    url = "https://grep.app/api/search?" + urlencode({"q": query, "page": "1"})
    body, status = request(url)
    if body is None:
        return {"status": status, "matches": None}
    try:
        obj = json.loads(body)
        hits = obj.get("hits", {})
        results = hits.get("hits", [])
        return {"status": status, "matches": hits.get("total"), "examples": [str(hit.get("repo", "")) + "/" + str(hit.get("path", "")) for hit in results[:5]]}
    except (json.JSONDecodeError, AttributeError):
        return {"status": status, "matches": None, "error": "non-JSON response"}


def sourcegraph(query):
    q = query + " count:5"
    url = "https://sourcegraph.com/.api/search/stream?" + urlencode({"q": q, "v": "V3", "t": "keyword", "display": 5})
    body, status = request(url)
    if body is None:
        return {"status": status, "matches": None}
    count = None
    repositories = []
    for line in body.splitlines():
        if not line.startswith("data: "):
            continue
        try:
            obj = json.loads(line[6:])
        except json.JSONDecodeError:
            continue
        if isinstance(obj, list):
            for match in obj:
                if isinstance(match, dict) and match.get("type") in ("content", "path"):
                    repositories.append(str(match.get("repository", "")) + "/" + str(match.get("path", "")))
        elif isinstance(obj, dict) and "matchCount" in obj:
            count = obj["matchCount"]
    return {"status": status, "matches": count, "examples": repositories[:5], "body_bytes": len(body)}


for name, search in (("grep.app", grep_app), ("Sourcegraph", sourcegraph)):
    control = search(CONTROL)
    print(json.dumps({"index": name, "phase": "known-original-positive-control", **control}, sort_keys=True))
    if not isinstance(control.get("matches"), int) or control["matches"] <= 0:
        print(json.dumps({"index": name, "phase": "stop", "reason": "no proven original positive-control coverage"}))
        continue
    target = search(TARGET)
    print(json.dumps({"index": name, "phase": "single-upstream-target-identifier", **target}, sort_keys=True))
