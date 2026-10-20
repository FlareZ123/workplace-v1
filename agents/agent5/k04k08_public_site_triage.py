"""Bounded, anonymous read-only survey of public Noyes pages.

The original BX25/08 footer identifies this host. The human maintainer removed
the local-only restriction from resources/START_HERE.md on 2026-10-20.
No credentials, state changes, forms, private APIs, or JS execution.
"""
from __future__ import annotations

import hashlib
from html.parser import HTMLParser
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from urllib.parse import urljoin, urlparse


ORIGIN = "https://noyes-energy-group.pages.dev"
PATHS = (
    "/",
    "/company/",
    "/insights/",
    "/projects/",
    "/admin",
    "/robots.txt",
    "/sitemap.xml",
)


class Document(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.skip = 0
        self.text: list[str] = []
        self.links: list[str] = []
        self.scripts: list[str] = []
        self.forms: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = dict(attrs)
        if tag in ("style", "script"):
            self.skip += 1
        if tag == "script" and a.get("src"):
            self.scripts.append(a["src"])
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag == "form":
            self.forms.append(a.get("action") or "(no explicit action)")

    def handle_endtag(self, tag: str) -> None:
        if tag in ("style", "script") and self.skip:
            self.skip -= 1

    def handle_data(self, data: str) -> None:
        if not self.skip and data.strip():
            self.text.append(data.strip())


def read_path(path: str) -> None:
    target = urljoin(ORIGIN + "/", path.removeprefix("/"))
    assert urlparse(target).netloc == urlparse(ORIGIN).netloc
    print("\n=== SOURCE", target, "===", flush=True)
    try:
        with urlopen(
            Request(target, headers={"User-Agent": "H17-offline-preservation/1.0"}),
            timeout=15,
        ) as response:
            raw = response.read(2_000_001)
            final_url = response.url
            status = response.status
            mime = response.headers.get("content-type", "")
    except (HTTPError, URLError) as exc:
        print("FETCH_ERROR", str(exc), flush=True)
        return
    if urlparse(final_url).netloc != urlparse(ORIGIN).netloc:
        print("REDIRECT_OUTSIDE_ORIGIN (content not processed)", final_url, flush=True)
        return
    if len(raw) > 2_000_000:
        print("TOO_LARGE", flush=True)
        return
    print("HTTP", status, "MIME", mime, "BYTES", len(raw), flush=True)
    print("SHA256", hashlib.sha256(raw).hexdigest(), "FINAL_URL", final_url, flush=True)
    content = raw.decode("utf-8", errors="replace")
    if "html" in mime:
        doc = Document()
        doc.feed(content)
        print("PUBLIC_LINKS", repr(doc.links[:100]), flush=True)
        print("SCRIPT_SRCS", repr(doc.scripts[:15]), flush=True)
        print("FORM_ACTIONS", repr(doc.forms[:15]), flush=True)
        content = "\n".join(doc.text)
    print("PAGE_BEGIN", flush=True)
    print(content[:18000], flush=True)
    print("PAGE_END", flush=True)


def main() -> None:
    for path in PATHS:
        read_path(path)


if __name__ == "__main__":
    main()
