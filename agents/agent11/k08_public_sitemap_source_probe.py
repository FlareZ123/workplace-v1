"""Read-only public sitemap discovery for the original BX25/08 correspondence host.

Visits standard published indexes only; never visits /admin or /api, guesses
credentials, or modifies any external service.
"""
from __future__ import annotations

import hashlib
import re
from urllib.error import HTTPError
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from xml.etree import ElementTree

HOST = "noyes-energy-group.pages.dev"
BASE = f"https://{HOST}"
MARK = re.compile(r"H[- ]?17|261003|ESC[- ]?N|BX25|coupon|keeper|record|Emily|printer|preserv", re.I)


def safe_url(url: str) -> bool:
    parts = urlparse(url)
    return (parts.scheme == "https" and parts.hostname == HOST and
            parts.port is None and parts.username is None and
            parts.password is None and not parts.path.startswith(("/admin", "/api/")))


def get_public(url: str) -> bytes | None:
    assert safe_url(url), url
    try:
        with urlopen(Request(url, headers={"User-Agent": "H17-public-original-source-index/1.0"}), timeout=15) as response:
            if not safe_url(response.url):
                print("SKIP_REDIRECT", url, response.url, flush=True)
                return None
            body = response.read(1000001)
            if len(body) > 1000000:
                print("SKIP_OVERSIZE", url, flush=True)
                return None
            print("GET", response.status, url, len(body), hashlib.sha256(body).hexdigest(), flush=True)
            return body
    except HTTPError as exc:
        print("GET_HTTP", exc.code, url, flush=True)
        return None


def main() -> None:
    robots = get_public(BASE + "/robots.txt")
    sitemaps = [BASE + "/sitemap.xml"]
    if robots:
        for line in robots.decode("utf-8", "replace").splitlines():
            if line.lower().startswith("sitemap:"):
                found = line.split(":", 1)[1].strip()
                if safe_url(found):
                    sitemaps.append(found)
    paths = set()
    for url in dict.fromkeys(sitemaps):
        raw = get_public(url)
        if not raw:
            continue
        try:
            root = ElementTree.fromstring(raw)
        except ElementTree.ParseError:
            print("NOT_XML", url, flush=True)
            continue
        for element in root.iter():
            if element.tag.rsplit("}", 1)[-1] != "loc" or not element.text:
                continue
            loc = element.text.strip()
            if safe_url(loc):
                paths.add(loc)
                print("SITEMAP_PUBLIC_PATH", loc, bool(MARK.search(loc)), flush=True)
        print("SITEMAP_INDEXED_PUBLIC", len(paths), flush=True)
    for url in sorted(paths)[:16]:
        if not MARK.search(url):
            continue
        content = get_public(url)
        if content:
            decoded = re.sub(r"<[^>]+>", " ", content.decode("utf-8", "replace"))
            print("TARGET_PATH_SOURCE_TEXT", url, decoded[:3000], flush=True)
    print("PUBLIC_INDEX_CHECK_COMPLETE", len(paths), flush=True)


if __name__ == "__main__":
    main()
