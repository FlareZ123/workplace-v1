"""SFT: printer partial-echo audits ignore generated case work and missing sources fail.

The original 43-member ZIP and the current 42-resource checkout are both valid
inputs. Only manifest-listed case members may enter the comparison corpus.
"""
from __future__ import annotations

import re
import shutil
import tempfile
import unittest
from pathlib import Path

from check_h17_printer_partial_echoes import load_source_members, longest_echo


ROOT = Path(__file__).resolve().parents[1] / "resources"
SPOOL = "evidence/print/spool-reconstruction.log"


class PrinterEchoSourceScope(unittest.TestCase):
    def test_generated_work_cannot_introduce_false_echo(self) -> None:
        baseline, ignored = load_source_members(ROOT)
        self.assertIn(len(baseline), (42, 43))
        self.assertEqual(ignored, 0)

        selected = [
            line for line in baseline[SPOOL].splitlines(keepends=True)
            if b"JOB=PS-261003-0417" in line
            and b"ATTEMPT=2 STATE=ACK CLASS=RECOVER" in line
        ]
        self.assertEqual(len(selected), 1)
        found = re.search(rb"PAYLOAD=([0-9A-F]{32})", selected[0])
        self.assertIsNotNone(found)
        assert found is not None
        coupon = bytes.fromhex(found.group(1).decode("ascii"))
        coupon_hex = coupon.hex().upper().encode("ascii")
        original_scope = dict(baseline)
        original_scope[SPOOL] = b"".join(
            line for line in baseline[SPOOL].splitlines(keepends=True)
            if line != selected[0]
        )
        clean_raw = longest_echo(coupon, original_scope)[0]
        clean_hex = longest_echo(coupon_hex, original_scope)[0]
        other_sources = {
            name: data for name, data in original_scope.items() if name != SPOOL
        }
        external_raw = longest_echo(coupon, other_sources)[0]
        external_hex = longest_echo(coupon_hex, other_sources)[0]
        self.assertEqual((clean_raw, clean_hex), (1, 5))
        self.assertEqual((external_raw, external_hex), (1, 3))
        print(
            f"Original {len(baseline)}-file case: raw/hex echo maxima "
            f"including remaining spool={clean_raw}/{clean_hex}, "
            f"excluding spool={external_raw}/{external_hex}"
        )

        with tempfile.TemporaryDirectory() as temporary:
            copied = Path(temporary) / "case"
            shutil.copytree(ROOT, copied)
            (copied / "candidate.json").write_text(
                '{"K04":"fabricated"}', encoding="utf-8"
            )
            work = copied / "work"
            work.mkdir()
            (work / "raw-echo.bin").write_bytes(coupon)
            (work / "text-echo.txt").write_bytes(coupon_hex + b"\\n")

            members, excluded = load_source_members(copied)
            self.assertEqual(members, baseline)
            self.assertEqual(excluded, 3)
            self.assertEqual(
                longest_echo(coupon, {**members, SPOOL: original_scope[SPOOL]})[0],
                clean_raw,
            )
            self.assertEqual(
                longest_echo(coupon_hex, {**members, SPOOL: original_scope[SPOOL]})[0],
                clean_hex,
            )
            self.assertEqual(longest_echo(coupon, {"fake": coupon})[0], 16)
            self.assertEqual(longest_echo(coupon_hex, {"fake": coupon_hex})[0], 32)
            print(
                "Generated fake coupon files ignored: 3; "
                "source-only echo maxima unchanged; synthetic full echoes detected"
            )

    def test_missing_original_record_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            copied = Path(temporary) / "case"
            shutil.copytree(ROOT, copied)
            (copied / "START_HERE.md").unlink()
            with self.assertRaisesRegex(ValueError, "START_HERE.md"):
                load_source_members(copied)
            print("Missing original START_HERE.md correctly rejected")


if __name__ == "__main__":
    unittest.main(verbosity=2)
