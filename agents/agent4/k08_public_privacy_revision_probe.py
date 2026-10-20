"""Read-only source change watch for publicly published privacy notice.

A human maintainer reported a revised corporate privacy page at 03:31 UTC,
after the prior 03:27 public source census. Visit only the site's published
/privacy/ page and flag original K04/K08 record terms in visible text. Do not
fetch referenced credential/database logs or protected administrative URLs.
"""
from hashlib import sha256
from html.parser import HTMLParser
from urllib.parse import urlparse
from urllib.request import Request, urlopen
import re

URL = "https://noyes-energy-group.pages.dev/privacy/"
EARLIER_SHA256 = "f73c9b0bf4f52443d533b477f479d486b51b4388e895f000a203e6832775428c"
TARGET = re.compile(r"\\b(?:H[- ]?17|PS-261003|REC8|ESC[- ]?N|Emily|desk[- ]?margin|coupon|keeper|261003|BX25|recovery[- ]?envelope)\\b", re.I)


class VisibleText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.skip = 0
        self.lines = []
        self.links = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("script", "style"):
            self.skip += 1
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self.skip:
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip and data.strip():
            self.lines.append(" ".join(data.split()))


def main():
    with urlopen(Request(URL, headers={"User-Agent": "H17-public-notice-review/1.0"}),
                 timeout=15) as response:
        parsed = urlparse(response.url)
        assert parsed.scheme == "https" and parsed.hostname == "noyes-energy-group.pages.dev"
        raw = response.read(150_001)
        assert len(raw) <= 150_000
        print("PUBLIC_PRIVACY", response.status, len(raw), sha256(raw).hexdigest(), flush=True)
    print("DIFFERS_FROM_PRIOR", sha256(raw).hexdigest() != EARLIER_SHA256, flush=True)
    parser = VisibleText()
    parser.feed(raw.decode("utf8", "replace"))
    print("VISIBLE_LINES", len(parser.lines), "LINKS", parser.links, flush=True)
    for line in parser.lines:
        if TARGET.search(line):
            print("ORIGINAL_ARCHIVE_ANCHOR", repr(line[:250]), flush=True)
    # Only harmless summary of current statement about the accidental service.
    for line in parser.lines:
        if re.search(r"(?i)privacy|service|server|incident|update", line):
            print("NOTICE", repr(line[:300]), flush=True)


if __name__ == "__main__":
    main()
