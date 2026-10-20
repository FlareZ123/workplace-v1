"""Read-only K08 photograph/media surface census of the source-linked public site.

The 2025 BX25/08 folio supplies the hostname. A prior HTML/link survey did not
inspect img/srcset/OG-image and linked stylesheet assets. This script discovers
only links published by anonymously reachable same-origin HTML; it neither
guesses hidden routes nor accesses /admin or /api.
"""
from collections import deque
from hashlib import sha256
from html.parser import HTMLParser
from urllib.parse import urljoin, urldefrag, urlparse
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
import re

ORIGIN = "https://noyes-energy-group.pages.dev/"
PAGE_LIMIT = 30
MEDIA_LIMIT = 70
BYTE_LIMIT = 2_000_000
KEYWORDS = re.compile(
    rb"h[- ]?17|watch|crew|late|night|tea|mug|cup|caption|Emily|keeper|"
    rb"photograph|window|voices|envelope|sea|table|lamp|slogan",
    re.IGNORECASE,
)
CSS_URL = re.compile(r"url[(]([^)]*)[)]", re.IGNORECASE)
MEDIA_SUFFIX = (".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg", ".avif", ".pdf")


def same_origin(base, target):
    full, _ = urldefrag(urljoin(base, target))
    parsed = urlparse(full)
    if parsed.scheme != "https" or parsed.netloc != urlparse(ORIGIN).netloc:
        return None
    if parsed.path.startswith(("/admin", "/api/")):
        return None
    return full


def fetch(url):
    try:
        with urlopen(Request(url, headers={"User-Agent": "H17-public-evidence/1.0"}),
                     timeout=15) as response:
            if same_origin(ORIGIN, response.url) is None:
                return None
            raw = response.read(BYTE_LIMIT + 1)
            mime = response.headers.get("content-type", "").split(";")[0].lower()
    except (HTTPError, URLError, TimeoutError, ValueError) as exc:
        print("UNAVAILABLE", url, type(exc).__name__, flush=True)
        return None
    if len(raw) > BYTE_LIMIT:
        print("OVERSIZE", url, flush=True)
        return None
    print("FETCH", url, mime, len(raw), sha256(raw).hexdigest(), flush=True)
    return mime, raw


class Page(HTMLParser):
    def __init__(self, url):
        super().__init__()
        self.url = url
        self.pages = set()
        self.media = set()
        self.css = set()
        self.labels = []

    def handle_starttag(self, tag, attributes):
        a = dict(attributes)
        if tag == "a" and a.get("href"):
            target = same_origin(self.url, a["href"])
            if target:
                if urlparse(target).path.lower().endswith(MEDIA_SUFFIX):
                    self.media.add(target)
                else:
                    self.pages.add(target)
        if tag in ("img", "source", "video", "audio"):
            for attr in ("src", "poster"):
                if a.get(attr):
                    target = same_origin(self.url, a[attr])
                    if target:
                        self.media.add(target)
            if a.get("srcset"):
                for section in a["srcset"].split(","):
                    if not section.strip():
                        continue
                    target = same_origin(self.url, section.strip().split()[0])
                    if target:
                        self.media.add(target)
            for attr in ("alt", "title", "aria-label"):
                if a.get(attr):
                    self.labels.append((tag, attr, a[attr]))
        if tag == "meta":
            name = (a.get("name") or a.get("property") or "").lower()
            if name in ("og:image", "twitter:image") and a.get("content"):
                target = same_origin(self.url, a["content"])
                if target:
                    self.media.add(target)
            if name in ("description", "og:description", "twitter:description"):
                self.labels.append((tag, name, a.get("content", "")))
        if tag == "link" and a.get("href"):
            rel = (a.get("rel") or "").lower()
            target = same_origin(self.url, a["href"])
            if target and "stylesheet" in rel:
                self.css.add(target)
            if target and a.get("as") == "image":
                self.media.add(target)


def main():
    pending = deque([ORIGIN])
    pages_seen = set()
    media = set()
    css = set()
    captions = []
    while pending and len(pages_seen) < PAGE_LIMIT:
        page = pending.popleft()
        if page in pages_seen:
            continue
        pages_seen.add(page)
        fetched = fetch(page)
        if not fetched or "html" not in fetched[0]:
            continue
        parsed = Page(page)
        parsed.feed(fetched[1].decode("utf-8", "replace"))
        captions.extend((page, tag, key, value)
                        for tag, key, value in parsed.labels)
        media.update(parsed.media)
        css.update(parsed.css)
        pending.extend(sorted(parsed.pages - pages_seen))
    print("CAPTIONS", len(captions), flush=True)
    for row in captions:
        print("CAPTION", repr(row), flush=True)
    for stylesheet in sorted(css):
        fetched = fetch(stylesheet)
        if fetched and "css" in fetched[0]:
            for target in CSS_URL.findall(fetched[1].decode("utf-8", "replace")):
                resolved = same_origin(stylesheet, target.strip().strip(chr(34)).strip(chr(39)))
                if resolved:
                    media.add(resolved)
    print("HTML_PAGE_COUNT", len(pages_seen), "STYLESHEET_COUNT", len(css),
          "MEDIA_URL_COUNT", len(media), flush=True)
    for i, asset in enumerate(sorted(media)):
        if i >= MEDIA_LIMIT:
            print("MEDIA_LIMIT_REACHED", MEDIA_LIMIT, flush=True)
            break
        fetched = fetch(asset)
        if not fetched:
            continue
        mime, raw = fetched
        if any(kind in mime for kind in ("text", "svg", "json")):
            for match in list(KEYWORDS.finditer(raw))[:10]:
                print("MEDIA_TEXT_CONTEXT", asset,
                      repr(raw[max(0, match.start()-70):match.end()+90]), flush=True)
        else:
            # Only printable metadata-bearing runs; no image recognition/OCR.
            runs = re.findall(rb"[ -~]{10,}", raw)
            matches = [x[:180] for x in runs if KEYWORDS.search(x)]
            for x in matches[:10]:
                print("MEDIA_PRINTABLE_CONTEXT", asset, repr(x), flush=True)
    print("SOURCE_SURFACE_SCOPE public-HTML-linked-media-only", flush=True)


if __name__ == "__main__":
    main()
