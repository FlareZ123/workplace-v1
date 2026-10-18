"""SFT: generated work files cannot become alternate-mask source evidence.

Run with Python 3 standard library:
    python results/test_h17_alternate_mask_scope.py
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPT = Path(__file__).with_name("check_h17_k04_alternate_mask_carriers.py")


def run_audit(case: Path) -> dict:
    output = subprocess.check_output(
        [sys.executable, str(SCRIPT), "--root", str(case)],
        text=True,
    )
    return json.loads(output)


class AlternateMaskScope(unittest.TestCase):
    def test_generated_files_are_excluded(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            case = Path(temporary) / "case"
            shutil.copytree(REPO / "resources", case)
            baseline = run_audit(case)
            self.assertIn(baseline["input_file_count"], (42, 43))
            self.assertEqual(baseline["ignored_non_source_files"], 0)
            self.assertEqual(baseline["original_commitment_matches"], [])

            (case / "candidate.json").write_text(
                '{"K04":null,"K08":null}', encoding="utf-8"
            )
            work = case / "work"
            work.mkdir()
            # A generated mask that matches the scanner's synthetic raw
            # control would falsely enlarge its hit count if work/ were scanned.
            (work / "generated-mask.bin").write_bytes(
                (case / "START_HERE.md").read_bytes()[:16]
            )
            observed = run_audit(case)
            self.assertEqual(observed["ignored_non_source_files"], 2)
            for key in (
                "input_file_count",
                "raw_windows",
                "hex_windows",
                "original_commitment_matches",
                "control_match_counts",
                "selected_payload",
                "retained_mask",
            ):
                self.assertEqual(observed[key], baseline[key], key)


if __name__ == "__main__":
    unittest.main(verbosity=2)
