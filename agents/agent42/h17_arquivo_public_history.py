"""Check independent Arquivo.pt public captures of the original BX25/08 site.

Read-only anonymous archive search; no access to the corporate origin server.
No account, protected page or inferred unlinked corporate route is contacted.
"""
import json
import urllib.error
import urllib.parse
import urllib.request

HOST = "noyes-energy-group.pages.dev"
ROOT = f"https://{HOST}/"
HEADERS = {"User-Agent": "H17-public-archive-metadata-check/1.0"}


def read_archive(url):
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=25) as response:
            return response.status, response.read(300_000).decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read(400).decode("utf-8", "replace")
    except (urllib.error.URLError, TimeoutError) as exc:
        return "transport_error", str(exc)


queries = {
    "url_history_root": "https://arquivo.pt/textsearch?"
    + urllib.parse.urlencode({"versionHistory": ROOT, "maxItems": 20, "prettyPrint": "false"}),
    "url_history_host": "https://arquivo.pt/textsearch?"
    + urllib.parse.urlencode({"versionHistory": HOST, "maxItems": 20, "prettyPrint": "false"}),
    "cdx_public_host": "https://arquivo.pt/wayback/cdx?"
    + urllib.parse.urlencode({"url": HOST + "/*", "output": "json", "filter": "statuscode:200"}),
}
for label, url in queries.items():
    status, body = read_archive(url)
    result = {"probe": label, "status": status}
    if status == 200:
        try:
            obj = json.loads(body)
            if isinstance(obj, dict):
                records = obj.get("response_items", [])
                result["reported_total"] = obj.get("total_items", obj.get("estimated_nr_results"))
            else:
                records = obj
            if records and isinstance(records[0], list):
                header, rows = records[0], records[1:]
                records = [dict(zip(header, row)) for row in rows]
            keep = []
            for r in records:
                uri = r.get("originalURL") or r.get("original") or r.get("url", "")
                path = urllib.parse.urlsplit(uri).path.lower()
                if path.startswith(("/admin", "/api/")):
                    continue
                keep.append({
                    "originalURL": uri,
                    "timestamp": r.get("timestamp", r.get("tstamp")),
                    "title": r.get("title", "")[:100],
                })
            result["public_records"] = keep[:30]
            result["public_count_in_page"] = len(keep)
        except (ValueError, TypeError, KeyError) as exc:
            result["parse_error"] = str(exc)
            result["body_prefix"] = body[:250]
    else:
        result["error_prefix"] = body[:250]
    print(json.dumps(result, sort_keys=True), flush=True)
