"""Source-pinned hidden-object audit of the human-released encrypted BX25/08 PDF.

Looks beyond extracted page text at every indirect PDF object, embedded files,
annotations, catalog actions, metadata and decoded streams. Read-only.
"""
from __future__ import annotations

import hashlib
import io
import re
import sys
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from pypdf.generic import IndirectObject, StreamObject

EXPECTED = "b6a6156f596575b988126c6d3e5cbb88d5794cc927a5564c37b6ddb8cecc3425"
PATTERN = re.compile(rb"IR[- ]?261003|PS[- ]?261003|ESC[- ]?N|recover|Emily|desk|lamp|watch|mug|caption|K0[48]", re.I)


def inspect(reader: PdfReader) -> tuple[int, list[tuple[str, str]]]:
    assert len(reader.pages) == 1
    root = reader.root_object
    print("ROOT_KEYS", sorted(str(x) for x in root.keys()), flush=True)
    print("TRAILER_KEYS", sorted(str(x) for x in reader.trailer.keys()), flush=True)
    print("ATTACHMENT_NAMES", sorted(reader.attachments.keys()), flush=True)
    print("PAGE_ANNOTS", len(reader.pages[0].get("/Annots", [])), flush=True)
    print("DOCUMENT_METADATA", dict(reader.metadata) if reader.metadata else None, flush=True)

    scanned: set[tuple[int, int]] = set()
    markers: list[tuple[str, str]] = []
    counts: dict[str, int] = {}

    def scan(obj, location: str) -> None:
        if isinstance(obj, IndirectObject):
            identity = (obj.idnum, obj.generation)
            if identity in scanned:
                return
            scanned.add(identity)
            obj = obj.get_object()
        cls = type(obj).__name__
        counts[cls] = counts.get(cls, 0) + 1
        if isinstance(obj, StreamObject):
            payload = obj.get_data()
            assert len(payload) <= 1000000
            hits = sorted(set(m.group().decode("ascii", "replace") for m in PATTERN.finditer(payload)))
            if hits:
                markers.append((location, ",".join(hits)))
        if isinstance(obj, dict):
            for key, value in obj.items():
                scan(value, location + "/" + str(key))
        elif isinstance(obj, list):
            for n, value in enumerate(obj):
                scan(value, location + f"[{n}]")
        elif isinstance(obj, (str, bytes)):
            raw = obj.encode("utf-8") if isinstance(obj, str) else obj
            hits = sorted(set(m.group().decode("ascii", "replace") for m in PATTERN.finditer(raw)))
            if hits:
                markers.append((location, ",".join(hits)))

    for generation, entries in reader.xref.items():
        for objnum in sorted(entries):
            if objnum:
                scan(IndirectObject(objnum, generation, reader), f"OBJECT:{objnum}:{generation}")
    print("INDIRECT_OBJECTS", len(scanned), flush=True)
    print("OBJECT_TYPES", counts, flush=True)
    print("TARGET_MARKER_LOCATIONS", markers, flush=True)
    return len(scanned), markers


def main(source: Path) -> None:
    blob = source.read_bytes()
    assert hashlib.sha256(blob).hexdigest() == EXPECTED
    reader = PdfReader(io.BytesIO(blob))
    assert reader.is_encrypted and reader.decrypt("8131")
    print("SOURCE_SHA256", EXPECTED, flush=True)
    count, markers = inspect(reader)
    assert count >= 4
    assert not reader.attachments
    for i, ref in enumerate(reader.pages[0].get("/Annots", [])):
        annotation = ref.get_object()
        fields = {str(k): str(v)[:800] for k, v in annotation.items() if str(k) not in ("/AP", "/P")}
        print("ORIGINAL_ANNOTATION", i, fields, flush=True)
    assert "/OpenAction" not in reader.root_object
    assert "/AcroForm" not in reader.root_object
    assert "/Names" not in reader.root_object
    print("ORIGINAL_HIDDEN_ATTACHMENT_OR_ANNOTATION", "FOUND" if any("Embedded" in loc or "Annots" in loc for loc, _ in markers) else "NONE", flush=True)

    writer = PdfWriter()
    writer.add_blank_page(width=100, height=100)
    writer.add_attachment(filename="synthetic.txt", data=b"H17_RECOVER_attachment_test")
    temporary = io.BytesIO()
    writer.write(temporary)
    temporary.seek(0)
    control = PdfReader(temporary)
    assert control.attachments["synthetic.txt"] == [b"H17_RECOVER_attachment_test"]
    print("SYNTHETIC_ATTACHMENT_CONTROL PASS", flush=True)


if __name__ == "__main__":
    main(Path(sys.argv[1]))
