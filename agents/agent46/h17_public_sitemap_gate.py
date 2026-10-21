"""One-time, read-only 2025-folio-linked public sitemap source-locator probe.

Strictly standard public sitemap/robots resources. Only case-named same-origin
URLs are fetched (at most four), with redirects disabled and bounded reads.
Never attempts credentials, restricted APIs, guessed files, or live equipment.
This does not authenticate any historical 2026 document or recover REC8.
"""
import hashlib
import re
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from urllib.parse import urlsplit

HOST = "noyes-energy-group.pages.dev"
BASE = "https://" + HOST
CASE = re.compile(r"h[-_]?17|ir[-_]?261003|ps[-_]?261003|wn[-_]?14|esc[-_]?n|keeper", re.I)
LIMIT = 65536


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


OPENER = urllib.request.build_opener(NoRedirect)


def fetch(path):
    request = urllib.request.Request(
        BASE + path,
        headers={"User-Agent": "H17-preservation-public-sitemap-readonly/1.0"},
    )
    try:
        with OPENER.open(request, timeout=16) as response:
            data = response.read(LIMIT + 1)
            status = response.status
            content_type = response.headers.get("Content-Type", "")
    except urllib.error.HTTPError as error:
        data = error.read(256)
        status = error.code
        content_type = error.headers.get("Content-Type", "")
    except (urllib.error.URLError, TimeoutError) as error:
        print("NETWORK_ERROR", path, type(error).__name__, str(error)[:150])
        return None
    if len(data) > LIMIT:
        print("RESPONSE_TOO_LARGE", path, status, len(data))
        return None
    print("FETCH", path, "status", status, "bytes", len(data),
          "sha256", hashlib.sha256(data).hexdigest(),
          "type", content_type.split(";")[0])
    return data if status == 200 else None


def main():
    robots = fetch("/robots.txt")
    if robots is not None:
        for line in robots.decode("utf-8", "replace").splitlines():
            if line.lower().strip().startswith("sitemap:"):
                print("ROBOTS_PUBLIC_SITEMAP_REF", line.strip()[:250])

    sitemap = fetch("/sitemap.xml")
    if sitemap is None:
        print("STOP no public sitemap bytes, no original target information")
        return
    try:
        root = ET.fromstring(sitemap)
    except ET.ParseError:
        print("STOP non-XML sitemap, no original target information")
        return

    urls = []
    for element in root.iter():
        if element.tag.split("}")[-1] == "loc" and element.text:
            url = element.text.strip()
            split = urlsplit(url)
            if split.scheme == "https" and split.netloc == HOST and not split.query:
                path = split.path
                if not path.startswith(("/admin", "/api")):
                    urls.append(path)
    urls = sorted(set(urls))
    eligible = [p for p in urls if CASE.search(p)]
    print("SITEMAP_LOCATIONS", len(urls), "CASE_NAMED", len(eligible))
    for path in eligible[:4]:
        fetch(path)
    if not eligible:
        print("STOP no case-named public sitemap paths, no original target information")
    print("K04_SELECTED_BITS_RECOVERED", 0, "K08_EXACT_FINAL_WORDS", 0)


if __name__ == "__main__":
    assert CASE.search("/IR-261003-H17.txt")
    assert not CASE.search("/insights/generic-renewables")
    main()
