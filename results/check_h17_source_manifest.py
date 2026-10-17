"""Read-only integrity check for the 43 archived H-17 source members."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "resources"
MANIFEST = ROOT / "results" / "h17-source-blob-manifest.json"


def inspect():
    reference = json.loads(MANIFEST.read_text(encoding="utf-8"))
    expected = {entry["path"]: entry for entry in reference["files"]}
    actual = {file.relative_to(SOURCE).as_posix(): file
              for file in SOURCE.rglob("*") if file.is_file()}
    discrepancies = []
    lines = []
    for path in sorted(actual):
        payload = actual[path].read_bytes()
        git_blob = hashlib.sha1(b"blob " + str(len(payload)).encode("ascii")
                                + b"\0" + payload).hexdigest()
        sha256 = hashlib.sha256(payload).hexdigest()
        lines.append(f"{path} {sha256}\n")
        record = expected.get(path)
        if record is None:
            discrepancies.append(f"Unexpected source: {path}")
        elif record["bytes"] != len(payload) or record["git_blob_sha1"] != git_blob:
            discrepancies.append(f"Source content changed: {path}")
    for path in sorted(expected.keys() - actual.keys()):
        discrepancies.append(f"Missing source: {path}")
    canonical = hashlib.sha256("".join(lines).encode("utf-8")).hexdigest()
    if canonical != reference["canonical_sha256_manifest"]:
        discrepancies.append("Canonical SHA-256 manifest does not match")
    return {"case_id": reference["case_id"],
            "expected_files": reference["file_count"], "present_files": len(actual),
            "computed_canonical_sha256_manifest": canonical,
            "matched": not discrepancies, "discrepancies": discrepancies}


if __name__ == "__main__":
    result = inspect()
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["matched"] else 1)
