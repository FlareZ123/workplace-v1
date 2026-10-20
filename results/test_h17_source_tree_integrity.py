"""SFT: original 43-file evidence and separately authorized supplements are intact.

The original ZIP manifest remains immutable. The maintainer removed AGENT_PROMPT.txt,
revised START_HERE.md, and added four office supplements on 20 October.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "results" / "h17-source-blob-manifest.json"
SOURCE = ROOT / "resources"
ALLOWED_OMISSION = frozenset({"AGENT_PROMPT.txt"})

# Repository-only changes, independently pinned from the original 43-file ZIP.
AUTHORIZED_REPO_ONLY = {
    "START_HERE.md": (1979, "452f5ef26acd27cca453975929a4c2a50712df8b"),
    "evidence/h17-supplemental-office-files/BX25-08.pdf": (
        5407, "cd69d8da88c7704a50a4199e190909e31015dc99"
    ),
    "evidence/h17-supplemental-office-files/print-fleet-retirement-note.txt": (
        1390, "dd0496b516438cebfa5c720972417ea745ca5c3c"
    ),
    "evidence/h17-supplemental-office-files/retired-office-bookmarks.html": (
        2499, "d4cbde7f6ad6931be4946987348d7fdc3f1d2a9b"
    ),
    "evidence/h17-supplemental-office-files/supplier-reconciliation-L29.csv": (
        1607, "9654507764b3b983fd2c141669a6b02cf5a7d8c7"
    ),
}


def source_differences(source: Path, expected: dict[str, dict]) -> list[str]:
    actual = {
        path.relative_to(source).as_posix(): path
        for path in source.rglob("*")
        if path.is_file()
    }
    differences = []
    for name in sorted(actual.keys() - expected.keys()):
        differences.append(f"Unexpected source: {name}")
    for name in sorted(expected.keys() - actual.keys() - ALLOWED_OMISSION):
        differences.append(f"Missing source: {name}")
    for name in sorted(actual.keys() & expected.keys()):
        payload = actual[name].read_bytes()
        blob = hashlib.sha1(
            b"blob " + str(len(payload)).encode("ascii") + b"\0" + payload
        ).hexdigest()
        record = expected[name]
        if len(payload) != record["bytes"] or blob != record["git_blob_sha1"]:
            differences.append(f"Source content changed: {name}")
    return differences


class CurrentSourceIntegrity(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        cls.expected = {item["path"]: item for item in manifest["files"]}
        assert len(cls.expected) == manifest["file_count"] == 43
        for name, (size, blob_sha) in AUTHORIZED_REPO_ONLY.items():
            cls.expected[name] = {"bytes": size, "git_blob_sha1": blob_sha}
        assert len(cls.expected) == 47

    def test_preserved_files_are_byte_identical(self) -> None:
        self.assertEqual(source_differences(SOURCE, self.expected), [])

    def test_generated_files_and_source_edits_are_detected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            case = Path(temporary) / "resources"
            shutil.copytree(SOURCE, case)
            self.assertEqual(source_differences(case, self.expected), [])

            supplemental = case / "evidence/h17-supplemental-office-files/retired-office-bookmarks.html"
            initial = supplemental.read_bytes()
            supplemental.write_bytes(initial + b"\\n")
            self.assertIn(
                "Source content changed: evidence/h17-supplemental-office-files/retired-office-bookmarks.html",
                source_differences(case, self.expected),
            )
            supplemental.write_bytes(initial)

            (case / "work").mkdir()
            (case / "work" / "notes.txt").write_text("generated", encoding="utf-8")
            self.assertIn(
                "Unexpected source: work/notes.txt",
                source_differences(case, self.expected),
            )
            (case / "work" / "notes.txt").unlink()
            (case / "work").rmdir()

            label = case / "evidence" / "archive-labels.ini"
            label.write_bytes(label.read_bytes() + b"\\n")
            self.assertIn(
                "Source content changed: evidence/archive-labels.ini",
                source_differences(case, self.expected),
            )

            label.unlink()
            self.assertIn(
                "Missing source: evidence/archive-labels.ini",
                source_differences(case, self.expected),
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
