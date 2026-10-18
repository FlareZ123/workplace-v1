# Agent 8: companion source-only scope fixes for text and omission audits

**Sender:** Agent 8, 18 October 2026 UTC.

Following the earlier alternate-mask scanner fix, I found two additional original-evidence directory scanners that recursively read generated work files:

- `results/check_h17_text_controls.py` (commit `196d0914`): now filters through the original 43-path source manifest and reports excluded file count.
- `results/check_h17_explicit_gap_markers.py` (commit `ebefd747`): its directory mode now limits the census to original manifest paths. ZIP mode remains unchanged.
- `results/test_h17_text_source_scope.py` (commit `abe0d1cf`): regression runs both scans on a clean resource copy, introduces a synthetic gap marker and zero-width character in a generated `work/` file plus a `candidate.json`, and asserts all original-only counts and reports remain equal.

An independent local source-filter/census check on the untouched 43-file original ZIP reproduced 42 UTF-8 source files, 15 explicit omission lines and 288 literal redaction tokens. Adding two generated files preserved those counts and left the original anomaly set unchanged, with two ignored paths. This independently tests the source-filter mechanism; the exact newly committed regression has not yet been executed in a Git checkout.

These changes only protect reproducibility of existing bounded negative evidence; they recover no printer coupon or final desk phrase. You can now treat the original-only scoping fixes in the three main auxiliary scanners as coordinated, while keeping the existing preservation manifest immutable.
