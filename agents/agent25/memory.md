# Agent 25 continuity: evidence-first H-17 investigation

**Current incarnation:** original mode draw 8 (normal), genuine cryptographic RNG. Successfully claimed previously unleased identity via `agents/agent25/.lease.json`, run ID `8cc770e6d29c4a6e97bed19743fcf3e2`, original claim `2026-10-18T03:55:54Z`; read-back confirmed. Increased root COUNTER from 41 to 42. Do not refresh lease; check age by real UTC clock after each checkpoint, release only when >=70 minutes and all useful writes pushed. Root README prohibits per-commit CI.

## Baseline and source review

Original attached `c-energy-group-documents2026.zip` with 43 members. Read original START_HERE, records custodian, routing, acceptance, verify.py, full keeper notes, principal emails, printer spool tail and file metadata, and existing research synthesis/broadcasts. The best-supported canonical six remain K01/K02/K03/K05/K06/K07 individually PASS. K04 (printer escrow) and K08 (Emily's final margin caption) remain null, combined INCOMPLETE, accepted false. Preserved original verifier unchanged.

Source-selected K04: incident-date ESC-N -> PS-261003-0417, last ACK RECOVER attempt 2, `A9A9DC5731A5E2AE879C47215C2559D5` XOR `8556C8CB6140A7F9A5123AC7571BEE1C` = `2CFF149C50E54557228E7DE60B3EB7C9`, SHA256 `11a7f6064781a6ac7678dc6dd24759af95981c8a927f8da4436515354d34549b`, original commitment NO_MATCH. Neither printer payload nor transcribed mask has independent validation. N02/N06 are K08 drafts, N17/N18 different labels, N23 final wording reference but no quoted original. Previous agents have exhaustively scanned many bounded source classes; avoid redundant brute-force families or six-slot replays as new research.

## Distinct contribution

Investigated whether ZIP metadata can independently corroborate original mail / printer timestamps. All 43 ZIP central directory dates are exactly (2026,10,4,11,40,0); independently parsed local headers using ZIP DOS date/time fields and found all 43 pair `(0x5D00,0x5D44)`, matching central date and the START_HERE export-preparation time. ZIP DOS time lacks timezone; there is no independent original-source timestamp evidence in this packaging. This refines the chronology uncertainty: ZIP entries cannot resolve mail13 vs AX-7782 or mail16 vs printer chronology. Added bounded, method-backed section to `results/h17-chronology-cross-slot-control.md`, commit `f4d4c41f431a5afed233f6baea726fc18c1640f7`; remote fetched and confirmed.

Other exploratory local checks: 133 16-byte printer spool PAYLOADs contain no straightforward self-authentication via head/tail CRC32, head/tail 4-byte truncated SHA256 of other 12 bytes (multiple orientations), or aligned XOR parity across 32-bit words. This unpromoted null test has very limited evidentiary scope and lacks a source-prescribed internal checksum; no claim that an ECC schema was disproven. Eight Emily-authored numbered notes, but the naive nth-word index exceeds several note lengths and produces no intelligible phrase, so no plausible deterministic index witness.

## User-facing deliverable

Created `/mnt/data/H17_recovery_partial_2026-10-18.zip` in current conversation: `candidate.json`, `verification.json`, `derivation.md`, original unchanged `verify.py` and `acceptance.json`. Freshly ran original verifier; six PASS, two MISSING, combined INCOMPLETE, `accepted=false`, expected exit 1. Local ZIP SHA256 `15bfc8e6e7ae0b4e3089c287c418f3bafd5c4898676c69e4acc13a05d2998dcc`. This is a user-facing partial handoff only, not new missing-slot evidence, and must not be treated as a completed recovery.

## Next

Continue looking only for a source-supported authenticated local K04 coupon/mask correction mechanism or an exact final K08 caption witness; always require unchanged slot acceptance. Check new communications selectively. Do not operate facility equipment or contact people; local-case scope forbids original-source external collection. Preserve partial evidence and uncertainty. If no viable mechanism emerges, retain null K04/K08 and do not make unsupported claims of recovery.
