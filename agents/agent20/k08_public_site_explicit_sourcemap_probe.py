"""Read-only probe of explicitly advertised source maps on the folio-linked public site.

Follows only an already linked public script and source-map URLs literally advertised
by its headers or sourceMappingURL annotations. No guessed routes, API, admin,
credentials, or forms. A source map is a candidate record source, not evidence
that its contents are historically authentic.
"""
from __future__ import annotations

import hashlib
import json
import re
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlsplit
from urllib.request import Request, build_opener, HTTPRedirectHandler

HOST = "noyes-energy-group.pages.dev"
SCRIPT = f"https://{HOST}/assets/site.js"
LIMIT = 1_000_000
TARGET = re.compile(r"H-17|IR-261003|ESC-N|PS-261003|Emily|keeper|WN-14|coupon|caption|RECOVER", re.I)


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def permitted(url: str) -> bool:
    p = urlsplit(url)
    return p.scheme == "https" and p.hostname == HOST and not (
        p.path.startswith("/admin") or p.path.startswith("/api/")
    )


def get(url: str):
    if not permitted(url):
        print("SKIP_OUT_OF_SCOPE", url)
        return None
    try:
        with build_opener(NoRedirect).open(
            Request(url, headers={"User-Agent": "H17-public-records-source-map-readonly/1.0"}),
            timeout=18,
        ) as r:
            body = r.read(LIMIT + 1)
            if len(body) > LIMIT:
                print("OVERSIZE", url)
                return None
            print("PUBLIC_SOURCE", url, r.status, len(body), hashlib.sha256(body).hexdigest(),
                  r.headers.get("Content-Type", ""))
            return body, r.headers
    except (HTTPError, URLError, TimeoutError) as e:
        print("UNAVAILABLE", url, str(e))
        return None


def main() -> None:
    response = get(SCRIPT)
    if response is None:
        return
    body, headers = response
    text = body.decode("utf-8", errors="replace")
    urls = set()
    for m in re.finditer(r"(?:[#@]\\s*sourceMappingURL=)([^\\s*]+)", text):
        urls.add(m.group(1).strip())
    for field in ("SourceMap", "X-SourceMap"):
        if headers.get(field):
            urls.add(headers[field].strip())
    print("EXPLICIT_MAP_LOCATORS", sorted(urls))
    for rel in sorted(urls):
        url = urljoin(SCRIPT, rel)
        response = get(url)
        if response is None:
            continue
        raw, _ = response
        try:
            data = json.loads(raw)
        except ValueError:
            print("NON_JSON_MAP", url)
            continue
        sources = data.get("sources", [])
        content = data.get("sourcesContent", [])
        print("MAP_SOURCES", len(sources), "SOURCES_CONTENT", len(content))
        for i, original in enumerate(content):
            if not isinstance(original, str):
                continue
            hits = TARGET.findall(original)
            if hits:
                print("ORIGINAL_SOURCE_TEXT_MARKERS", i, sources[i] if i < len(sources) else "?",
                      hits[:20])
    print("SCOPE_ONLY_EXPLICIT_PUBLIC_SOURCE_MAP_URLS; NO_TARGET_CLAIM")


if __name__ == "__main__":
    main()
