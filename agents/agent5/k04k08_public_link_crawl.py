"""Bounded crawl of publicly linked Noyes corporate pages only.

Anonymous HTTPS GETs. Excludes robots-disallowed /admin and /api/
and never follows off-domain links or posts forms.
"""
from __future__ import annotations

import hashlib
import re
from collections import deque
from html.parser import HTMLParser
from urllib.error import HTTPError, URLError
from urllib.parse import urldefrag, urljoin, urlparse
from urllib.request import Request, urlopen


ORIGIN = "https://noyes-energy-group.pages.dev"
KEYWORDS = re.compile(
    r"H[- ]?17|PS-261003|ESC[- ]?N|BX25|FA[- ]?17|archive|"
    r"recover|coupon|printer|caption|Emily|records|incident|"
    r"preservation|scanner",
    re.IGNORECASE,
)


class VisibleHTML(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ignore = 0
        self.links: list[str] = []
        self.lines: list[str] = []
        self.script_sources: list[str] = []

    def handle_starttag(self, tag: str, attributes: list[tuple[str, str | None]]) -> None:
        args = dict(attributes)
        if tag in ("style", "script"):
            self.ignore += 1
        if tag == "a" and args.get("href"):
            self.links.append(args["href"])
        if tag == "script" and args.get("src"):
            self.script_sources.append(args["src"])

    def handle_endtag(self, tag: str) -> None:
        if tag in ("style", "script") and self.ignore:
            self.ignore -= 1

    def handle_data(self, data: str) -> None:
        if not self.ignore and data.strip():
            self.lines.append(data.strip())


def bounded_get(path: str) -> tuple[str, str] | None:
    full = urljoin(ORIGIN, path)
    if urlparse(full).netloc != urlparse(ORIGIN).netloc:
        return None
    try:
        with urlopen(
            Request(full, headers={"User-Agent": "H17-preservation-source-census/1.0"}),
            timeout=15,
        ) as reply:
            payload = reply.read(1_000_001)
            url = reply.url
            mime = reply.headers.get("content-type", "")
    except (HTTPError, URLError) as exc:
        print("GET_FAIL", path, str(exc), flush=True)
        return None
    if urlparse(url).netloc != urlparse(ORIGIN).netloc:
        print("EXTERNAL_REDIRECT_SKIP", path, url, flush=True)
        return None
    if len(payload) > 1_000_000:
        print("OVERSIZE_SKIP", path, flush=True)
        return None
    print(
        "GET_OK",
        path,
        len(payload),
        hashlib.sha256(payload).hexdigest(),
        mime,
        flush=True,
    )
    return mime, payload.decode("utf-8", errors="replace")


def normalize_href(href: str) -> str | None:
    full, _ = urldefrag(urljoin(ORIGIN, href))
    parsed = urlparse(full)
    if parsed.scheme != "https" or parsed.netloc != urlparse(ORIGIN).netloc:
        return None
    path = parsed.path
    if path.startswith(("/admin", "/api/")):
        return None
    if not path.startswith("/"):
        return None
    return path


def main() -> None:
    queue: deque[str] = deque(["/"])
    observed: set[str] = set()
    while queue and len(observed) < 24:
        path = queue.popleft()
        if path in observed or path.startswith(("/admin", "/api/")):
            continue
        observed.add(path)
        response = bounded_get(path)
        if response is None:
            continue
        mime, raw = response
        if "html" not in mime:
            continue
        doc = VisibleHTML()
        doc.feed(raw)
        print("PAGE_TITLE", path, doc.lines[0] if doc.lines else "(none)", flush=True)
        print("LINKS", path, doc.links[:45], flush=True)
        for line in doc.lines:
            if KEYWORDS.search(line):
                print("SOURCE_ANCHOR", path, line[:320], flush=True)
        for link in doc.links:
            target = normalize_href(link)
            if target is not None and target not in observed and target not in queue:
                queue.append(target)
    print("PUBLIC_PATHS_SURVEYED", len(observed), sorted(observed), flush=True)
    print("SITE_SCRIPT", flush=True)
    result = bounded_get("/assets/site.js")
    if result:
        _, script = result
        for match in list(KEYWORDS.finditer(script))[:30]:
            print(
                "SCRIPT_CONTEXT",
                repr(script[max(0, match.start() - 90):match.end() + 140]),
                flush=True,
            )
        print("SCRIPT_TOP", script[:1800], flush=True)


if __name__ == "__main__":
    main()
