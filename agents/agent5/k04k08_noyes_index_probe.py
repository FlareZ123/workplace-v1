"""Read-only source triage of the newly permitted original BX25 correspondence index.

The URL is printed in the original, 2025-dated BX25/08 property declaration.
The human maintainer removed the former "local export only; no external access"
restriction from resources/START_HERE.md on 20 October 2026 at 02:50 UTC.
This probe makes one HTTPS GET; it does not follow links or execute remote code.
"""
from __future__ import annotations

import hashlib
import html.parser
import urllib.request


URL = "https://noyes-energy-group.pages.dev/"


class PageText(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.skip = 0
        self.text: list[str] = []
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in ("script", "style"):
            self.skip += 1
        if tag == "a":
            self.links.extend(value for name, value in attrs if name == "href" and value)

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style") and self.skip:
            self.skip -= 1

    def handle_data(self, data: str) -> None:
        if not self.skip and data.strip():
            self.text.append(data.strip())


def main() -> None:
    print("SOURCE", URL, flush=True)
    req = urllib.request.Request(
        URL, headers={"User-Agent": "H17-evidence-archive/1.0", "Accept": "text/html,*/*"}
    )
    with urllib.request.urlopen(req, timeout=20) as reply:
        raw = reply.read(2_000_001)
        print("HTTP", reply.status, reply.url, flush=True)
        print("CONTENT_TYPE", reply.headers.get("content-type"), flush=True)
    if len(raw) > 2_000_000:
        raise ValueError("Unexpected page size over 2 MB")
    print("BYTES", len(raw), "SHA256", hashlib.sha256(raw).hexdigest(), flush=True)
    page = PageText()
    page.feed(raw.decode("utf-8", errors="replace"))
    print("LINKS_BEGIN", flush=True)
    for link in page.links[:100]:
        print(link, flush=True)
    print("LINKS_END", flush=True)
    print("PAGE_TEXT_BEGIN", flush=True)
    print("\n".join(page.text)[:30_000], flush=True)
    print("PAGE_TEXT_END", flush=True)


if __name__ == "__main__":
    main()
