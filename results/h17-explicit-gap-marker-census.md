# H-17: explicit export-omission marker census

**Agent 8, 18 October 2026. Result:** the original retained export explicitly marks missing pages of an unrelated maintenance notebook and omitted supporting RC-17 process/signature text, and documents removal of duplicated quoted mail. It does **not** contain a direct marker identifying a missing original ESC-N coupon fragment or Emily's exact final caption. No recovered K04 or K08 value results. This audits *visible omission signalling*, not completeness.

## Original-record anchor and hypothesis

The custodian writes in resources/evidence/records-custodian.txt: “Textual export gaps are marked where the export tool could identify them. The absence of a gap marker is not a completeness certificate.” START_HERE.md independently calls the export trimmed and notes that original mailboxes/devices are unavailable.

A discriminating question is whether a retained explicit omission marker points to either missing component's historical original, rather than merely unmarked absence or a corrupted transcription. An original-source bracketed gap near an ESC-N payload or keeper caption would be a directly testable observation. This study enumerates what the supplied text actually marks.

## Read-only method

[Reproducer](check_h17_explicit_gap_markers.py) scans all 43 original archive members, decodes the 42 UTF-8 members (excluding the binary TRP2 dump), and records literal case-insensitive line matches for the phrases “omitted”, “not included”, “export gap” or “extraction gap”. Separately it counts literal [censored] tokens, other bracketed markers within evidence/ (excluding archive-labels.ini section headings), and literal three-dot ellipses. Results use original byte line breaks and 1-based line numbers.

The script accepts either the unmodified supplied ZIP as its path argument or the repository's resources/ directory by default. The original ZIP SHA-256 is a801d9b32715305b4a889e3c091a88455090a5c4bd56b6cf7f6c07ba8e4527ec, matching the existing manifest. It modifies no source files or commitments.

## Observed census

- **15 omission-declaration lines:** evidence/mail/INDEX.md line 3 (quoted-message repeats removed); evidence/records-custodian.txt line 5 (same policy); evidence/maintenance/inspection-rounds.log line 10 (rest of notebook not included in export); 12 repeated supporting-process/signature omission notices in evidence/procedures/RC-17-scans.txt (lines 7, 19, 31, 43, 55, 67, 79, 91, 103, 115, 127, 139).
- **288 literal redaction tokens** across the export's UTF-8 text, consistent with the stated personal/company redaction policy. The custodian specifically says these markers are not recovery material.
- **One non-redaction bracketed marker within the evidence texts**, the inspection notebook's explicit missing-pages note above. No source-evidence line contains the literal three-dot ellipsis. The scan excludes programming-language brackets in verify.py and INI section headings from the bracket-marker count.
- The selected K04 printer row in evidence/print/spool-reconstruction.log and the relevant K08 crew-note/mail sections contain **no flagged omission declaration or bracketed gap marker** under these test rules. This says nothing about unidentified damage or omitted originals.

## Interpretation and limits

The explicit notebook gap concerns a maintenance source that has no routing role in K04/K08; RC-17 supporting instructions and signatures are outside the four footer strips used for accepted K06. Quoted-email deletion has been separately qualified in [K08 textual coverage](h17-k08-textual-coverage.md). None of the enumerated markers supplies printer coupon bytes or exact caption words.

Crucially, the custodian's own warning means **no visible gap marker is not evidence that the retained spool is correct or the final desk phrase is somewhere in the export**. The spool is a retained-fragment reconstruction with no independent checksum for every line, and Emily's final margin is described without quotation. The filename/line and marker test cannot rule out undocumented omission phrases, encoding, damaged bytes, absent attachments or uncaptured physical originals.

This bounded census strengthens the provenance description of *visible* missing material, while preserving the existing evidence boundary: six original slot commitments PASS, K04 and K08 MISSING, combined INCOMPLETE, accepted false. See [current recovery status](README.md) and [source-sufficiency matrix](h17-source-sufficiency-matrix.md).


## ZIP-mode source-membership hardening (Agent 15, 18 October 2026)

The initial read-only scanner correctly excluded generated `work/` and `candidate.json` files when called on an extracted directory, but its **ZIP path** consumed all archive members indiscriminately. A derived handoff ZIP containing generated notes with phrases such as "export gap" could therefore be reported as though it were an original source omission. This is a reproducibility/source-provenance defect in the *wrapper*, not evidence that the original 43-member case was mis-scanned.

The corrected [source scanner](check_h17_explicit_gap_markers.py) now uses the immutable original [43-path manifest](h17-source-blob-manifest.json) for both directory and ZIP inputs, ignores generated ZIP members, rejects duplicate original-member names, requires all 43 original manifest paths in ZIP mode, and permits the one intentional repository deletion of `AGENT_PROMPT.txt` only in directory mode. [The existing text-source SFT](test_h17_text_source_scope.py) was extended to construct a ZIP containing `work/synthetic-marker.txt` and `candidate.json`, verify byte-for-byte identical omission-census fields to the clean original-resource directory, and verify a ZIP missing `START_HERE.md` fails rather than silently returning a truncated scan. These tests do **not** claim to recover a new record.

The manually triggered [read-only CI regression run 39175127404](https://github.com/FlareZ123/workplace-v1/actions/runs/39175127404) on `main` (head `0b017c8b9ccdd1bc344985885c67fbc4a4fc1be8`) passed every stage including the expanded text-and-omission scope check. An independent standard-library reading of the immutable original supplied ZIP reconfirmed **43 members, 42 UTF-8 text members, 15 explicit omission lines, 288 redaction tokens, one non-redaction evidence bracket marker, and zero literal three-dot ellipsis lines**. The source census, no direct original K04/K08 gap marker, and six-of-eight REC8 status remain unchanged. The CI test fixture uses the current 42-file checkout with its intentional instructions-file deletion; the original 43-member ZIP counts were reproduced separately.


### Original-ZIP versus current-directory provenance contract

Agent 33 identified that the initial source-presence exception allowed a **42-member ZIP** without `AGENT_PROMPT.txt` to pass as though its original-source membership were complete. That exception properly belongs to the current 42-file repository directory, whose maintenance deletion is documented independently. The ZIP scanner now **requires all 43 original file paths**, while the extracted-directory scanner allows exactly the documented instructions-file omission. This validates *presence and uniqueness of expected paths*, not bytes or historical authenticity. Check the original ZIP SHA-256 and immutable per-file manifest separately for integrity claims.

The updated SFT constructs two synthetic 43-member ZIP fixtures (a clean one and one additionally carrying generated `work/` and `candidate.json`). Because the repository deliberately removed its original instructions file, these **test-only fixtures** contain a clearly identified synthetic placeholder under that path. They test path coverage and generated-work exclusion; they do not claim the placeholder matches original evidence. A separate regression asserts that a 42-member ZIP missing just `AGENT_PROMPT.txt` is rejected, while the current 42-file *directory* remains a valid specified subset. The [manual-only CI run 39175589773](https://github.com/FlareZ123/workplace-v1/actions/runs/39175589773), pinned to `30b3f87ad1e165edf44f782a2db20fee0019bb2c`, completed successfully. The earlier historical original-ZIP census is still 43 members, 15 omission declarations, and no K04/K08 source witness.
