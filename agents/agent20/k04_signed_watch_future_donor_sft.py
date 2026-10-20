"""Test signed WN-14 32-bit ink fields against the precomputed K04 future-donor XOR fingerprints.

Scope: 4 source-signed WN14 groups in mail03/mail06, compared with the 100
TRP2/RC17 typed source fields already tested separately by Agent29. Both
endian interpretations, with MT19937 untempering. Does not read original
spool row129, routing mask, nonce, REC8 acceptance or candidate bytes.

Usage: python agents/agent20/k04_signed_watch_future_donor_sft.py ORIGINAL_ZIP
"""
from __future__ import annotations

import hashlib
import itertools
import re
import sys
from zipfile import ZipFile

EXPECTED_HASHES = {
    "evidence/mail/03.eml": "3cf886c12e094cb0362999c5a4d93f913c848a64471f833fbddbfdc2d57ff889",
    "evidence/mail/06.eml": "6049994562a82e46afd3f0231e136a1e6911cc3040d848e32eaa5771a6f8c2f3",
    "evidence/mail/14.eml": "9c86de086a1727ca09b4df6f12cf5c634eaa22a3949424171cc50b4ef9983be5",
    "evidence/recorder/trip-recorder.raw": "5ebc6204ed773102237dd287772de96d19740e163b49b4075537d937888657ba",
    "evidence/procedures/RC-17-scans.txt": "a4b649fdbb6909115fb9505133012b5c1dda42141aafc1c6ec756199ddf1fc6d",
}
FINGERPRINTS = {
    "1412:1866": (0xFFFFFFFF, 0xBD2761F8),
    "1185:1412": (0xBFFFFFFF, 0x359EC0C7),
    "1185:1866": (0xBFFFFFFF, 0x88B9A13F),
    "1411:1865": (0x9FFFFFFF, 0x0CDE27B9),
}


def invert_right(x: int, shift: int) -> int:
    y = x
    for _ in range(5):
        y = x ^ (y >> shift)
    return y & 0xFFFFFFFF


def invert_left(x: int, shift: int, mask: int) -> int:
    y = x
    for _ in range(5):
        y = x ^ ((y << shift) & mask)
    return y & 0xFFFFFFFF


def untemper(x: int) -> int:
    return invert_right(
        invert_left(invert_left(invert_right(x, 18), 15, 0xEFC60000),
                    7, 0x9D2C5680),
        11,
    )


def oriented(records: list[tuple[str, bytes]]) -> list[tuple[str, str, int]]:
    return [
        (name, endian, untemper(int.from_bytes(value, endian)))
        for name, value in records
        for endian in ("big", "little")
    ]


def main(archive_path: str) -> None:
    with ZipFile(archive_path) as archive:
        files = {name: archive.read(name) for name in EXPECTED_HASHES}
    for name, expected in EXPECTED_HASHES.items():
        assert hashlib.sha256(files[name]).hexdigest() == expected, name

    signed = {}
    for name in ("evidence/mail/03.eml", "evidence/mail/06.eml"):
        for group, hexdigits in re.findall(
            r"WN-14 / group ([ABCD]) / ([0-9A-F]{8})",
            files[name].decode("utf-8"),
        ):
            assert group not in signed
            signed[group] = bytes.fromhex(hexdigits)
    assert set(signed) == set("ABCD")
    assert b"No replacement groups were issued" in files["evidence/mail/14.eml"]
    ink = oriented(sorted(signed.items()))

    recorder = files["evidence/recorder/trip-recorder.raw"]
    controls = [
        (f"TRP2 row{i}", recorder[16 + 24*i + 12:16 + 24*i + 16])
        for i in range(88)
    ]
    procedure = files["evidence/procedures/RC-17-scans.txt"].decode()
    for j, section in enumerate(procedure.split("\f")):
        match = re.search(r"Footer control strip: ([0-9A-F]{8})", section)
        if match:
            controls.append((f"RC17 section{j}", bytes.fromhex(match.group(1))))
    assert len(controls) == 100
    external = oriented(controls)
    print("signed_WN14_groups", len(signed), "oriented", len(ink))
    print("preexisting_TRP2_RC17_fields", len(controls), "oriented", len(external))

    for name, (mask, target) in FINGERPRINTS.items():
        cross = [
            (left[0], left[1], right[0], right[1])
            for left in ink for right in external
            if ((left[2] ^ right[2]) & mask) == target
        ]
        paired = [
            (left[0], left[1], right[0], right[1])
            for left, right in itertools.combinations(ink, 2)
            if left[0] != right[0]
            and ((left[2] ^ right[2]) & mask) == target
        ]
        print(name, f"mask={mask:08X}", f"target_xor={target:08X}",
              "new_cross_matches", cross, "new_within_WN14_matches", paired)
        assert not cross and not paired
    print("selected_K04_coupon_bits_from_this_test", 0)


if __name__ == "__main__":
    main(sys.argv[1])
