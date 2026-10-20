"""One-shot, source-addressed public counterpart check for the preserved R: index bookmark.

No site discovery, logins, protected APIs, or redirects are performed.
This is a testable read-only probe for an original, exact missing records index.
"""
from __future__ import annotations

import hashlib
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, Request, build_opener

HOST = "https://noyes-energy-group.pages.dev"
# The bookmarked source path is file:///R:/Records/INDEX/IR-261003-H17.txt.
# Probe only exact case/path equivalents, never credentials, APIs or site enumeration.
PATHS = (
    "/Records/INDEX/IR-261003-H17.txt",
    "/records/index/IR-261003-H17.txt",
    "/records/INDEX/IR-261003-H17.txt",
    "/IR-261003-H17.txt",
)
MARKERS = (b"IR-261003-H17", b"PS-261003-0417", b"ESC-N", b"keeper", b"Emily")


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def inspect(path: str) -> None:
    url = HOST + path
    req = Request(url, headers={"User-Agent": "H17-Records-Custody-ReadOnly/1.0"})
    opener = build_opener(NoRedirect())
    try:
        with opener.open(req, timeout=15) as response:
            status = response.status
            content_type = response.headers.get("Content-Type", "")
            data = response.read(262145)
    except HTTPError as exc:
        status = exc.code
        content_type = exc.headers.get("Content-Type", "")
        data = exc.read(262145)
    except URLError as exc:
        print(f"PATH={path} ERROR={type(exc).__name__} DETAILS={exc.reason}")
        return
    print(
        f"PATH={path} HTTP={status} TYPE={content_type!r} "
        f"SIZE_READ={len(data)} SHA256={hashlib.sha256(data).hexdigest()}"
    )
    if len(data) > 262144:
        print("LIMIT=exceeded; body not examined")
        return
    print("TARGET_MARKERS=" + repr([m.decode("ascii") for m in MARKERS if m.lower() in data.lower()]))
    if status == 200 and any(m.lower() in data.lower() for m in MARKERS):
        print("PUBLIC_TARGET_CANDIDATE_BODY_BEGIN")
        print(data[:16000].decode("utf-8", errors="replace"))
        print("PUBLIC_TARGET_CANDIDATE_BODY_END")


if __name__ == "__main__":
    assert len(PATHS) == len(set(PATHS))
    assert all(p.startswith("/") and "/api/" not in p.lower() and "/admin" not in p.lower() for p in PATHS)
    print("SOURCE=file:///R:/Records/INDEX/IR-261003-H17.txt")
    print("MODE=anonymous GET, no redirect follow, site-only literal bookmarked-path probes")
    for path in PATHS:
        inspect(path)
