"""One-shot public-site source-delta gate for H-17; no authentication or site probing.

Original: 2025 BX25/08 folio footer gives https://noyes-energy-group.pages.dev/.
Closest prior: Agent5 20 Oct public 11-page inventory, homepage SHA256
5d4aa1dd3f82e3ed63095a24b6ad76a08ac0e1536c0fd7ec7ea96be91431b653.
Difference: temporal content-change test 1 November, not reinterpretation of old pages.
Potential target reach: only if an independently attributed newly published
historical original quotes ESC-N ACK2 media or Emily's exact final keeper caption.
Maximum conditional gain: all 128 K04 selected coupon bits or exact K08 phrase;
actual gain initially zero. Stop at one HTTPS anonymous homepage GET; no guesses,
links, admin, APIs or automatically followed assets. An unchanged hash closes it.
"""
from hashlib import sha256
from urllib.request import Request, urlopen
from datetime import datetime, timezone

URL = "https://noyes-energy-group.pages.dev/"
PREVIOUS = "5d4aa1dd3f82e3ed63095a24b6ad76a08ac0e1536c0fd7ec7ea96be91431b653"

def main():
    request = Request(URL, headers={"User-Agent": "H17-readonly-source-delta/1.0"})
    with urlopen(request, timeout=15) as response:
        content = response.read(1024 * 1024 + 1)
        if len(content) > 1024 * 1024:
            raise ValueError("Exceeded one-megabyte fixed source cap")
        print("checked_utc=", datetime.now(timezone.utc).isoformat())
        print("status=", response.status)
        print("final_url=", response.url)
        print("content_type=", response.headers.get("content-type"))
        digest = sha256(content).hexdigest()
        print("sha256=", digest)
        print("matches_20261020_homepage=", digest == PREVIOUS)
        if digest != PREVIOUS:
            print("SOURCE_DELTA: independently assess historical eligibility before follow-up.")
        else:
            print("NO_DELTA: no reason for another public-page census.")

if __name__ == "__main__":
    main()
