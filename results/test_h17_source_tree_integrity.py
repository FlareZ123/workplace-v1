"""SFT: current preservation sources match the immutable original source manifest.

The maintainer intentionally removed only AGENT_PROMPT.txt from resources/.
All remaining original evidence bytes must be identical to their recorded blobs.
No case files are changed by this test.
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
            b"blob " + str(len(payload)).encode("ascii") + b"\\0" + payload
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

    def test_preserved_files_are_byte_identical(self) -> None:
        self.assertEqual(source_differences(SOURCE, self.expected), [])

    def test_generated_files_and_source_edits_are_detected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            case = Path(temporary) / "resources"
            shutil.copytree(SOURCE, case)
            self.assertEqual(source_differences(case, self.expected), [])

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
