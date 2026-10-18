"""SFT: original-source membership is invariant to generated recovery work files.

Run with Python's standard library from a repository checkout. The scanner
must use only the 43 manifest-listed preservation files, allowing current
42-file checkout after the maintainer's removal of AGENT_PROMPT.txt.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from check_h17_all_carriers import search


REPO = Path(__file__).resolve().parents[1]
SOURCE = REPO / "resources"


class SourceScopeRegression(unittest.TestCase):
    def test_added_recovery_work_is_never_source_evidence(self) -> None:
        acceptance = json.loads((SOURCE / "acceptance.json").read_text(encoding="utf-8"))
        routing = json.loads(
            (SOURCE / "evidence/recovery-routing.json").read_text(encoding="utf-8")
        )
        original_k04 = bytes.fromhex(acceptance["slot_sha256"]["K04"])
        original_k08 = bytes.fromhex(acceptance["slot_sha256"]["K08"])
        baseline = search(SOURCE, original_k04, original_k08)
        self.assertEqual(baseline["hits"], [])
        self.assertEqual(baseline["counts"]["ignored_non_source_files"], 0)

        expected = {
            42: (106928, 432, 612736),
            43: (108021, 432, 618316),
        }
        source_count = baseline["counts"]["files"]
        self.assertIn(source_count, expected)
        self.assertEqual(
            (
                baseline["counts"]["k04_raw_windows"],
                baseline["counts"]["k04_hex_windows"],
                baseline["counts"]["k08_word_spans"],
            ),
            expected[source_count],
        )

        fake_coupon = bytes.fromhex("0123456789ABCDEF0123456789ABCDEF")
        fake_caption = "a manufactured caption for the regression scope control"
        mask = bytes.fromhex(routing["K04"]["masked_component"])
        nonce = bytes.fromhex(routing["K08"]["desk_nonce"])
        fake_k04 = hashlib.sha256(
            bytes(a ^ b for a, b in zip(fake_coupon, mask))
        ).digest()
        fake_k08 = hashlib.sha256(
            hmac.digest(nonce, fake_caption.encode("utf-8"), "sha256")[:16]
        ).digest()
        clean_synthetic = search(SOURCE, fake_k04, fake_k08)
        self.assertEqual(clean_synthetic["hits"], [])

        with tempfile.TemporaryDirectory() as temporary:
            dirty = Path(temporary) / "resources"
            shutil.copytree(SOURCE, dirty)
            (dirty / "candidate.json").write_text(
                '{"K04": null, "K08": null}', encoding="utf-8"
            )
            work = dirty / "work"
            work.mkdir()
            (work / "raw-coupon.bin").write_bytes(fake_coupon)
            (work / "working-notes.txt").write_text(
                f"{fake_coupon.hex().upper()}\\n{fake_caption}\\n", encoding="utf-8"
            )

            observed = search(dirty, original_k04, original_k08)
            self.assertEqual(observed["hits"], baseline["hits"])
            self.assertEqual(
                {k: v for k, v in observed["counts"].items()
                 if k != "ignored_non_source_files"},
                {k: v for k, v in baseline["counts"].items()
                 if k != "ignored_non_source_files"},
            )
            self.assertEqual(observed["counts"]["ignored_non_source_files"], 3)

            synthetic_dirty = search(dirty, fake_k04, fake_k08)
            self.assertEqual(synthetic_dirty["hits"], [])
            self.assertEqual(
                {k: v for k, v in synthetic_dirty["counts"].items()
                 if k != "ignored_non_source_files"},
                {k: v for k, v in clean_synthetic["counts"].items()
                 if k != "ignored_non_source_files"},
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
