"""Read-only original BX25/08 decrypted PDF page-layer text/annotation audit.

Checks independently that the released page doesn't hide a second surface
containing an original 2026 printer coupon, route XOR mask or K08 caption.
Run with the original source PDF path. No external hyperlinks are opened.
"""
import hashlib
import sys
from collections import Counter
from pathlib import Path

from pypdf import PdfReader

SOURCE_SHA256 = "b6a6156f596575b988126c6d3e5cbb88d5794cc927a5564c37b6ddb8cecc3425"


def audit(source: Path) -> None:
    assert hashlib.sha256(source.read_bytes()).hexdigest() == SOURCE_SHA256
    reader = PdfReader(source)
    assert reader.decrypt("8131")
    assert len(reader.pages) == 1
    page = reader.pages[0]
    assert "/XObject" not in page["/Resources"]
    contents = page.get_contents()
    assert contents is not None
    ops = contents.operations
    types = Counter(operator.decode("ascii") for _, operator in ops)
    prints = []
    for arguments, operator in ops:
        if operator == b"Tj":
            prints.append(str(arguments[0]))
        elif operator == b"TJ":
            prints.extend(str(arg) for arg in arguments[0] if isinstance(arg, (bytes, str)))
    visible = page.extract_text()
    concealed = [value for value in prints if value and value not in visible]
    annotations = page.get("/Annots", [])
    assert len(annotations) == 1
    annotation = annotations[0].get_object()
    assert annotation["/Subtype"] == "/Link"
    assert annotation["/A"]["/S"] == "/URI"
    assert len(reader.pages) == 1
    print("PDF_SHA256", SOURCE_SHA256)
    print("PAGE_OPERATIONS", len(ops), "OPERATOR_COUNTS", dict(types))
    print("DRAWN_TEXT_FRAGMENTS", len(prints), "NOT_IN_EXTRACT_TEXT", concealed)
    print("GRAPHICAL_XOBJECTS", 0)
    print("ANNOTATIONS", len(annotations), "kind", annotation["/A"]["/S"])
    print("DOCUMENT_INFO", dict(reader.metadata or {}))
    print("STREAM_BYTES", len(contents.get_data()))
    print("STREAM_TEXT_COUNT", sum(map(len, prints)))
    print("SELECTED_GUARDRAIL", "do not visit external URI; original K04/K08 not read")


if __name__ == "__main__":
    assert len(sys.argv) == 2
    audit(Path(sys.argv[1]))
