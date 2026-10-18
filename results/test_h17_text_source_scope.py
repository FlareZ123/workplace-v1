"""SFT: text/control and export-gap reports must ignore generated recovery work.

Run with Python 3 standard library:
    python results/test_h17_text_source_scope.py
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

REPO = Path(__file__).resolve().parents[1]
RESULTS = Path(__file__).resolve().parent


def scan_text(root: Path) -> dict:
    output = subprocess.check_output(
        [sys.executable, str(RESULTS / "check_h17_text_controls.py"),
         "--root", str(root)],
        text=True,
    )
    return json.loads(output)


def scan_gaps(root: Path) -> dict:
    output = subprocess.check_output(
        [sys.executable, str(RESULTS / "check_h17_explicit_gap_markers.py"),
         str(root)],
        text=True,
    )
    return json.loads(output)


class OriginalSourceMembership(unittest.TestCase):
    def test_generated_notes_never_enter_original_census(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "case"
            shutil.copytree(REPO / "resources", root)
            baseline_text = scan_text(root)
            baseline_gaps = scan_gaps(root)
            self.assertIn(baseline_text["input_files"], (42, 43))
            self.assertEqual(baseline_text["ignored_non_source_files"], 0)
            self.assertEqual(baseline_gaps["members"], baseline_text["input_files"])

            (root / "candidate.json").write_text(
                '{"K04":null,"K08":null}', encoding="utf-8"
            )
            work = root / "work"
            work.mkdir()
            (work / "synthetic-marker.txt").write_text(
                "export gap: [unrelated] zero-width:\u200b\n",
                encoding="utf-8",
            )

            observed_text = scan_text(root)
            observed_gaps = scan_gaps(root)
            self.assertEqual(observed_text["ignored_non_source_files"], 2)
            for key in (
                "input_files",
                "utf8_text_files",
                "text_files_with_unusual_bytes",
            ):
                self.assertEqual(observed_text[key], baseline_text[key], key)
            self.assertEqual(observed_gaps, baseline_gaps)


    def test_text_mode_rejects_missing_original(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "case"
            shutil.copytree(REPO / "resources", root)
            (root / "START_HERE.md").unlink()
            outcome = subprocess.run(
                [sys.executable, str(RESULTS / "check_h17_text_controls.py"),
                 "--root", str(root)],
                capture_output=True, text=True,
            )
            self.assertNotEqual(outcome.returncode, 0)
            self.assertIn("START_HERE.md", outcome.stderr)

    def test_zip_mode_ignores_generated_records(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "case"
            shutil.copytree(REPO / "resources", root)
            baseline = scan_gaps(root)
            bundle = Path(temporary) / "with-work.zip"
            with ZipFile(bundle, "w", compression=ZIP_DEFLATED) as archive:
                for original in sorted(root.rglob("*")):
                    if original.is_file():
                        archive.write(original, original.relative_to(root).as_posix())
                archive.writestr("candidate.json", '{"K04":null,"K08":null}')
                archive.writestr(
                    "work/synthetic-marker.txt",
                    "export gap: [unrelated] synthetic ZIP-only omission\n",
                )
            observed = scan_gaps(bundle)
            self.assertIn("source_zip_sha256", observed)
            observed.pop("source_zip_sha256")
            self.assertEqual(observed, baseline)

    def test_zip_mode_rejects_missing_original(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "case"
            shutil.copytree(REPO / "resources", root)
            bundle = Path(temporary) / "missing.zip"
            with ZipFile(bundle, "w", compression=ZIP_DEFLATED) as archive:
                for original in sorted(root.rglob("*")):
                    if original.is_file() and original.name != "START_HERE.md":
                        archive.write(original, original.relative_to(root).as_posix())
            outcome = subprocess.run(
                [sys.executable, str(RESULTS / "check_h17_explicit_gap_markers.py"),
                 str(bundle)],
                capture_output=True, text=True,
            )
            self.assertNotEqual(outcome.returncode, 0)
            self.assertIn("START_HERE.md", outcome.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
