"""Bounded, anonymous Common Crawl inventory of the historical BX25/08 footer host.

This probes public crawl index metadata only. It never visits a company login or
protected API, and never posts or sends credentials to the source domain.
"""
import json
import re
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

HOST = "noyes-energy-group.pages.dev"
AGENT = "H17-archive-custodian-historical-source-check/1.0"

def fetch(url):
    req = Request(url, headers={"User-Agent": AGENT})
    try:
        with urlopen(req, timeout=25) as response:
            return response.status, response.read(300_001)
    except HTTPError as error:
        return error.code, error.read(300_001)

def main():
    status, raw = fetch("https://index.commoncrawl.org/collinfo.json")
    assert status == 200 and len(raw) <= 300000
    indexes = [item["id"] for item in json.loads(raw) if re.fullmatch(r"CC-MAIN-202[56]-\d{2}", item["id"])][:16]
    print("SOURCE=BX25/08 2025 original; footer public correspondence hostname")
    print("MODE=Common Crawl public index; NO source-host GET, API, login or POST")
    print("INDICES=" + ",".join(indexes), flush=True)
    count = 0
    for index in indexes:
        query = urlencode({"url": HOST + "/*", "output": "json", "filter": "status:200", "limit": "50"})
        try:
            status, data = fetch("https://index.commoncrawl.org/" + index + "-index?" + query)
        except (TimeoutError, URLError, ConnectionError) as error:
            print("INDEX=" + index + " ERROR=" + repr(error), flush=True)
            time.sleep(1)
            continue
        if status == 404:
            print("INDEX=" + index + " CAPTURES=0", flush=True)
        elif status == 200:
            entries = [json.loads(line) for line in data.decode("utf-8").splitlines() if line.strip()]
            entries = [entry for entry in entries if entry.get("url", "").lower().startswith(("https://" + HOST, "http://" + HOST))]
            print("INDEX=" + index + " CAPTURES=" + str(len(entries)), flush=True)
            count += len(entries)
            for entry in entries:
                path = entry["url"].split(HOST, 1)[1]
                if path.startswith(("/admin", "/api/")):
                    print("  PROTECTED_PATH=excluded", flush=True)
                else:
                    print("  TIME=" + str(entry.get("timestamp")) + " URL=" + entry["url"] + " MIME=" + str(entry.get("mime")) + " DIGEST=" + str(entry.get("digest")), flush=True)
        else:
            print("INDEX=" + index + " STATUS=" + str(status) + " RESPONSE=" + repr(data[:100]), flush=True)
        time.sleep(1)
    print("TOTAL_INDEXED_CAPTURES=" + str(count))
    print("NOTE=An index capture alone does not authenticate 2026 REC8 target bytes.")

if __name__ == "__main__":
    main()
