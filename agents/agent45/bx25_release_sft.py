"""SFT: recover the four-digit release for the original encrypted BX25/08 folio.

Invoke with the checked-out corporate PDF as the positional path.
Requires pypdf and pyca/cryptography. Reads but never modifies the file.
No REC8 acceptance commitment, archive coupon, K08 text, or hash oracle is used.
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

from pypdf import PdfReader
from pypdf._encryption import AlgV5

EXPECTED_SHA256 = "b6a6156f596575b988126c6d3e5cbb88d5794cc927a5564c37b6ddb8cecc3425"
EXPECTED_U = bytes.fromhex(
    "18108C9BF8E9E12068D2598F26096D95FFFBBE1C83E0BA0687D26C2099D9FE126"
    "9992C7F0E1044E812D21B7106A59830"
)


def recover(path: Path) -> tuple[str, list[str]]:
    original = path.read_bytes()
    assert hashlib.sha256(original).hexdigest() == EXPECTED_SHA256
    reader = PdfReader(path)
    assert reader.is_encrypted
    encrypt = reader.trailer["/Encrypt"]
    assert encrypt["/R"] == 6
    user_hash = bytes(encrypt["/U"])
    assert user_hash == EXPECTED_U and len(user_hash) == 48

    # ISO 32000 revision-6 user password validation: the original /U first
    # 32 bytes are a hash using the salt in the next 8 bytes.
    matches = [
        f"{value:04d}"
        for value in range(10000)
        if AlgV5.calculate_hash(
            6, f"{value:04d}".encode("ascii"), user_hash[32:40], b""
        ) == user_hash[:32]
    ]
    assert matches == ["8131"], matches
    password = matches[0]
    assert reader.decrypt(password)
    pages = [page.extract_text() for page in reader.pages]
    assert len(pages) == 1
    assert "Noyes Energy Group" in pages[0]
    assert "FA-17" in pages[0] and "BX25/08" in pages[0]
    print("PDF_SHA256", EXPECTED_SHA256)
    print("R6_FOUR_DIGIT_RELEASE", password)
    print("PAGE_COUNT", len(pages))
    print("ACCOUNT_CROSSWALK_AND_NAMED_INSURED PASS")
    print("NO_REC8_CANDIDATE_DERIVED")
    return password, pages


if __name__ == "__main__":
    assert len(sys.argv) == 2
    recover(Path(sys.argv[1]))
