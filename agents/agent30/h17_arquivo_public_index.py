"""Bounded anonymous query of an independent historical public archive's index."""
import json
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

HOST = "noyes-energy-group.pages.dev"
URLS = ("https://" + HOST + "/", HOST + "/*")
for source_url in URLS:
    query = urlencode({"url": source_url, "output": "json", "filter": "statuscode:200"})
    request = Request("https://arquivo.pt/wayback/cdx?" + query,
                      headers={"User-Agent": "H17-archival-custodian/1.0"})
    print("ORIGINAL", source_url, flush=True)
    try:
        with urlopen(request, timeout=25) as response:
            data = response.read(350001)
            print("HTTP", response.status, "BYTES", len(data), flush=True)
    except (HTTPError, URLError, TimeoutError) as error:
        print("UNAVAILABLE", type(error).__name__, str(error)[:220], flush=True)
        continue
    if len(data) > 350000:
        print("OVERSIZE: unassessed", flush=True)
        continue
    try:
        records = json.loads(data)
    except json.JSONDecodeError:
        print("NONJSON", repr(data[:200]), flush=True)
        continue
    if not isinstance(records, list):
        print("UNEXPECTED_SHAPE", type(records).__name__, flush=True)
        continue
    print("INDEXED_ROWS", len(records), flush=True)
    if records and isinstance(records[0], list) and "url" in records[0]:
        fields = records.pop(0)
        records = [dict(zip(fields, record)) for record in records]
    for record in records[:100]:
        if not isinstance(record, dict):
            continue
        url = str(record.get("url", ""))
        if HOST not in url.lower() or "/admin" in url.lower() or "/api/" in url.lower():
            continue
        print("PUBLIC_CAPTURE", record.get("timestamp"), record.get("statuscode"), url, flush=True)
