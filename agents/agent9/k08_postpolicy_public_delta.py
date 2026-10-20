"""Read only the newly amended public privacy page and its published links.

Source trigger: human broadcast 2026-10-20 03:31 UTC.
No portal, account, login, or API requests.
"""
from __future__ import annotations

import hashlib
from html.parser import HTMLParser
from urllib.request import Request, urlopen
from urllib.parse import urlparse

BASE = "https://noyes-energy-group.pages.dev"
PATH = "/privacy/"


class PublicText(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.skip = 0
        self.text: list[str] = []
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = dict(attrs)
        if tag in ("script", "style"):
            self.skip += 1
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style") and self.skip:
            self.skip -= 1

    def handle_data(self, data: str) -> None:
        if not self.skip and data.strip():
            self.text.append(data.strip())


def main() -> None:
    request = Request(BASE + PATH, headers={"User-Agent": "H17-published-policy-research/1.0"}, method="GET")
    with urlopen(request, timeout=20) as response:
        assert response.status == 200
        assert urlparse(response.url).hostname == urlparse(BASE).hostname
        raw = response.read(1000001)
    assert len(raw) <= 1000000
    doc = PublicText()
    doc.feed(raw.decode("utf-8", "replace"))
    visible = "\n".join(doc.text)
    print("PUBLIC_POLICY_URL", BASE + PATH, flush=True)
    print("PUBLIC_POLICY_SHA256", hashlib.sha256(raw).hexdigest(), flush=True)
    print("PUBLIC_POLICY_BYTES", len(raw), flush=True)
    print("PUBLISHED_LINKS", doc.links, flush=True)
    print("PUBLIC_POLICY_TEXT_BEGIN", flush=True)
    print(visible[:18000], flush=True)
    print("PUBLIC_POLICY_TEXT_END", flush=True)


if __name__ == "__main__":
    main()
