"""Read-only public correspondence-index probe for original BX25/08 source.

The original property folio labels the named company website an electronic
correspondence index. Test conventional public path counterparts to that label
without credentials, protected APIs, redirects, or state-changing requests.
A path hit does not by itself authenticate an October 2026 archive record.
"""
from __future__ import annotations

import hashlib
import re
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

ORIGIN = "https://noyes-energy-group.pages.dev"
PATHS = (
    "/correspondence/",
    "/correspondence/index.html",
    "/correspondence-index/",
    "/records/",
    "/records/index.html",
    "/records-index/",
)
PATTERN = re.compile(rb"H[- ]?17|261003|ESC[- ]?N|coupon|keeper|Emily|incident|retention|desk", re.I)


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def main() -> None:
    opener = build_opener(NoRedirect())
    for path in ("/", *PATHS):
        assert path.startswith("/") and not path.startswith(("/admin", "/api"))
        url = ORIGIN + path
        assert urlsplit(url).hostname == "noyes-energy-group.pages.dev"
        req = Request(url, headers={"User-Agent": "H17-read-only-original-correspondence/1.0"})
        try:
            with opener.open(req, timeout=15) as response:
                status = response.status
                mime = response.headers.get("content-type", "")
                data = response.read(1000001)
        except HTTPError as exc:
            status = exc.code
            mime = exc.headers.get("content-type", "")
            data = exc.read(1000001)
        except URLError as exc:
            print(f"PATH={path} ERROR={exc.reason}", flush=True)
            continue
        if len(data) > 1000000:
            print(f"PATH={path} OVERSIZE", flush=True)
            continue
        found = bool(PATTERN.search(data))
        print(
            f"PATH={path} HTTP={status} MIME={mime!r} BYTES={len(data)} "
            f"SHA256={hashlib.sha256(data).hexdigest()} TARGET_MARKER={found}",
            flush=True,
        )
        if status == 200 and "text" in mime and found:
            print("SOURCE_TEXT_BEGIN\n" + data[:16000].decode("utf-8", "replace") + "\nSOURCE_TEXT_END", flush=True)


if __name__ == "__main__":
    main()
