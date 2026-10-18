"""Byte-for-byte repackage check for the original H-17 local export.

Usage: python check_h17_zip_repack.py ORIGINAL_CASE.zip
Requires Python 3 and the zlib build used by the original archive (1.3.1).
Reads only the supplied ZIP; does not write to disk.
"""
import hashlib
import io
import json
from pathlib import Path
import sys
import zipfile
import zlib

EXPECTED = "a801d9b32715305b4a889e3c091a88455090a5c4bd56b6cf7f6c07ba8e4527ec"


def main():
    assert len(sys.argv) == 2
    source = Path(sys.argv[1]).read_bytes()
    assert hashlib.sha256(source).hexdigest() == EXPECTED
    out = io.BytesIO()
    with zipfile.ZipFile(io.BytesIO(source)) as original:
        with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as regenerated:
            for entry in original.infolist():
                metadata = zipfile.ZipInfo(entry.filename, entry.date_time)
                for name in ("compress_type", "create_system", "create_version", "extract_version",
                             "flag_bits", "volume", "internal_attr", "external_attr", "comment", "extra"):
                    setattr(metadata, name, getattr(entry, name))
                regenerated.writestr(metadata, original.read(entry.filename),
                                     compress_type=entry.compress_type, compresslevel=6)
    result = out.getvalue()
    report = {"members": 43, "original_bytes": len(source), "regenerated_bytes": len(result),
              "original_sha256": hashlib.sha256(source).hexdigest(),
              "regenerated_sha256": hashlib.sha256(result).hexdigest(),
              "exact_match": result == source, "zlib_runtime": zlib.ZLIB_RUNTIME_VERSION}
    assert report["exact_match"] and report["original_bytes"] == 39426
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
