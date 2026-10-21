"""Read-only historic Common Crawl index probe for BX25/08's exact public host.

Only published public captures. Never interact with the authenticated portal.
"""
import json
import urllib.error
import urllib.parse
import urllib.request

HOST = "noyes-energy-group.pages.dev"
INDICES = [
    "CC-MAIN-2026-39", "CC-MAIN-2026-34", "CC-MAIN-2026-30",
    "CC-MAIN-2026-25", "CC-MAIN-2026-21", "CC-MAIN-2026-17",
    "CC-MAIN-2026-12", "CC-MAIN-2025-51",
]
headers = {"User-Agent": "H17-public-historical-source-probe/1.0"}
for index in INDICES:
    query = urllib.parse.urlencode({
        "url": HOST + "/*",
        "output": "json",
        "filter": "status:200",
    })
    url = f"https://index.commoncrawl.org/{index}-index?{query}"
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=20) as response:
            lines = response.read(300000).decode("utf-8").splitlines()
            captured = []
            for line in lines:
                if not line.strip():
                    continue
                record = json.loads(line)
                path = urllib.parse.urlsplit(record["url"]).path.lower()
                if path.startswith(("/admin", "/api")):
                    continue
                captured.append({
                    "url": record["url"],
                    "timestamp": record["timestamp"],
                    "filename": record.get("filename"),
                    "offset": record.get("offset"),
                    "length": record.get("length"),
                })
            print(json.dumps({"crawl": index, "matches": captured}, sort_keys=True), flush=True)
    except urllib.error.HTTPError as ex:
        print(json.dumps({"crawl": index, "status": ex.code, "body": ex.read(180).decode("utf-8", "replace")}, sort_keys=True), flush=True)
    except (urllib.error.URLError, TimeoutError) as ex:
        print(json.dumps({"crawl": index, "error": str(ex)}, sort_keys=True), flush=True)
