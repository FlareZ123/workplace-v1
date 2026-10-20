"""Bounded offline access study of the 20 Oct 2026 supplemental BX25/08 folio.

Original bookmarks explicitly specify a four-position numeric release setting.
Only the locally committed PDF is read. No remote auth, user accounts, website,
credential reuse, or original source/commitment mutation occurs.
Run in GitHub Actions with pypdf.
"""
import hashlib
from pathlib import Path
from pypdf import PdfReader

SOURCE = Path("resources/evidence/h17-supplemental-office-files/BX25-08.pdf")
SHA256 = "b6a6156f596575b988126c6d3e5cbb88d5794cc927a5564c37b6ddb8cecc3425"

def inspect():
    raw = SOURCE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == SHA256
    reader = PdfReader(SOURCE)
    print("SOURCE_SHA256", SHA256, flush=True)
    print("IS_ENCRYPTED", reader.is_encrypted, flush=True)
    assert reader.is_encrypted
    enc = reader.trailer["/Encrypt"]
    print("SECURITY_REVISION", enc.get("/R"), "VERSION", enc.get("/V"), flush=True)
    print("SOURCE_DEFINED_CANDIDATE_CLASS", "exact four ASCII decimal digits, leading zeros preserved", flush=True)
    count = 0
    unlocked = None
    for value in range(10000):
        count += 1
        setting = f"{value:04d}"
        if reader.decrypt(setting):
            unlocked = setting
            break
    print("CANDIDATES_TRIED", count, "RELEASE_SETTING_FOUND", unlocked is not None, flush=True)
    if unlocked is None:
        print("SCOPE_RESULT", "NO_NUMERIC_FOUR_POSITION_SETTING", flush=True)
        return
    print("RELEASE_SETTING", unlocked, flush=True)
    print("PAGES", len(reader.pages), flush=True)
    for index, page in enumerate(reader.pages, 1):
        text = page.extract_text(extraction_mode="layout")
        print(f"=== DECRYPTED PAGE {index}, CHARACTERS {len(text)} ===", flush=True)
        print(text[:12000] or "(NO PDF TEXT LAYER)", flush=True)
    print("K04_COUPON_STATUS", "REQUIRES_EVIDENCE_REVIEW_AND_UNCHANGED_HASH", flush=True)

if __name__ == "__main__":
    inspect()
