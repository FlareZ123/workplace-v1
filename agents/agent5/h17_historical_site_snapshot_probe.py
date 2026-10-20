"""Query public Internet Archive indexes for historical captures of BX25's cited site.

The corporate website might have changed since the original 2025 policy page.
Only two anonymous archive-index GETs; no account or origin API access.
"""
from __future__ import annotations

import hashlib
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


URLS = (
    "https://archive.org/wayback/available?url=noyes-energy-group.pages.dev",
    "https://web.archive.org/cdx/search/cdx?url=noyes-energy-group.pages.dev%2F%2A&output=json&fl=timestamp%2Coriginal%2Cstatuscode&filter=statuscode%3A200&collapse=urlkey",
)


def main() -> None:
    for url in URLS:
        print("\nINDEX", url, flush=True)
        try:
            with urlopen(
                Request(url, headers={"User-Agent": "H17-historical-source-preservation/1.0"}),
                timeout=22,
            ) as response:
                body = response.read(300_001)
                print("HTTP", response.status, response.url, flush=True)
        except (HTTPError, URLError) as exc:
            print("ARCHIVE_UNAVAILABLE", str(exc), flush=True)
            continue
        if len(body) > 300_000:
            print("OVERSIZED_RESPONSE", flush=True)
            continue
        print("SHA256", hashlib.sha256(body).hexdigest(), "BYTES", len(body), flush=True)
        print("BODY", body.decode("utf-8", errors="replace")[:12000], flush=True)


if __name__ == "__main__":
    main()
