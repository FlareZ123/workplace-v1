"""One-shot public Wayback capture-index test for the BX25/08-linked site.

Read-only public metadata. Original target materials are not asserted to exist.
Do not contact the corporate origin, authentication paths, or live systems.
"""
import json
import urllib.error
import urllib.parse
import urllib.request

HOST = "noyes-energy-group.pages.dev"
ROOT = f"https://{HOST}/"
REQUESTS = {
    "cdx_public_index": (
        "https://web.archive.org/cdx/search/cdx?"
        + urllib.parse.urlencode(
            {
                "url": HOST + "/*",
                "output": "json",
                "fl": "timestamp,original,statuscode,mimetype,digest",
                "filter": "statuscode:200",
                "collapse": "urlkey",
                "limit": "200",
                "from": "2025",
                "to": "2026",
            }
        )
    ),
    "availability_incident_date": (
        "https://archive.org/wayback/available?"
        + urllib.parse.urlencode({"url": ROOT, "timestamp": "20261003"})
    ),
}
for label, url in REQUESTS.items():
    print("PROBE", label, flush=True)
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "H17-historical-public-capture-index/1.0"},
    )
    try:
        with urllib.request.urlopen(req, timeout=45) as response:
            body = response.read(300000).decode("utf-8", "replace")
            status = response.status
    except urllib.error.HTTPError as exc:
        body = exc.read(500).decode("utf-8", "replace")
        status = exc.code
    except (urllib.error.URLError, TimeoutError) as exc:
        print(json.dumps({"probe": label, "transport_error": str(exc)}), flush=True)
        continue
    info = {"probe": label, "http_status": status}
    if status != 200:
        info["body_prefix"] = body[:200]
    elif not body.strip():
        info["state"] = "empty_success_body_inconclusive"
    else:
        try:
            doc = json.loads(body)
            if label == "cdx_public_index":
                header, *rows = doc
                items = [dict(zip(header, row)) for row in rows]
                allowed = [
                    item for item in items
                    if urllib.parse.urlsplit(item["original"]).path.lower()
                       .startswith(("/admin", "/api/")) is False
                ]
                info["returned_count"] = len(items)
                info["public_count"] = len(allowed)
                info["public_captures"] = allowed[:100]
                info["limited_to_200"] = len(items) == 200
            else:
                info["closest_snapshot"] = doc.get("archived_snapshots", {})
        except (ValueError, TypeError, IndexError, KeyError) as exc:
            info["parse_error"] = str(exc)
            info["body_prefix"] = body[:200]
    print(json.dumps(info, sort_keys=True), flush=True)
