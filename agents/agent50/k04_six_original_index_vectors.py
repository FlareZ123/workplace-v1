"""Read-only acquisition of the six unpublished p949..954 original source-only layouts.

Runs existing Agent45 verified Z3/GF2 solver on the SHA-pinned original spool;
never reads the disputed selected payload, REC8 hashes, mask or K08 caption.
Prints full source-consistent row-start vectors for later independent original
TRP2 target projection. The already archived p955 vector is deliberately omitted.
"""
from __future__ import annotations
import hashlib
import json
import tempfile
import zipfile
from pathlib import Path

from agents.agent45.k04_z3_target_sft import probe

ROOT = Path(__file__).resolve().parents[2]
ORIGINAL = ROOT / "resources" / "evidence" / "print" / "spool-reconstruction.log"
EXPECTED = "7d71d8bef7f01596e705ac14e24c5c4352042512b3088125afca40f3841b6083"


def main():
    assert hashlib.sha256(ORIGINAL.read_bytes()).hexdigest() == EXPECTED
    with tempfile.TemporaryDirectory(prefix="h17-a50-source-") as folder:
        path = Path(folder) / "source_spool_only.zip"
        with zipfile.ZipFile(path, "w") as archive:
            archive.write(ORIGINAL, "evidence/print/spool-reconstruction.log")
        for target_index in range(949, 955):
            print("BEGIN_ORIGINAL_SOURCE_ONLY", target_index, flush=True)
            result = probe(path, target_index)
            print("ORIGINAL_SOURCE_ONLY_VECTOR",
                  json.dumps(result, sort_keys=True), flush=True)
            assert result["status"] == "source_consistent", result


if __name__ == "__main__":
    main()
