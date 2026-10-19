# Agent 48: H-17 preservation verification and blocked-source assessment

Identity claimed at 2026-10-18T04:56:08.511Z (run h17-emergency-recovery-r48-20261018T0456Z). Normal research mode; random draw 1/10.

## Current finding

Locally unpacked the original supplied 43-member ZIP, without changing any original case member. Independently created `candidate.json` from the previously confirmed six values and ran the original `verify.py --candidate candidate.json --json`: K01, K02, K03, K05, K06, K07 PASS; K04, K08 MISSING; six PASS; combined INCOMPLETE; accepted false. Local copy exists in this invocation at `/mnt/data/h17-case/`, with `work/recovery-log.md`, `verifier-result.json`, and a self-contained deliverable `/mnt/data/h17-partial-recovery.zip`. Original ZIP SHA256 a801d9b32715305b4a889e3c091a88455090a5c4bd56b6cf7f6c07ba8e4527ec.

Read original `START_HERE.md`, `records-custodian.txt`, `recovery-routing.json`, `mail/11,16,20`, full 24-note crew extract and all three original commitments. The recorded incident ESC-N last ACK produces K04=2CFF149C50E54557228E7DE60B3EB7C9, which conflicts with original SHA target, and the export lacks a payload integrity witness; both mask and logical map are transcriptions. The exact final Emily K08 keeper caption remains unquoted. These conditions agree with existing `results/README.md`, `h17-recovery.md`, `h17-evidence-audit.md`, `h17-source-sufficiency-matrix.md`, and Critic's 18 Oct evidence-first guidance.

I found no source-backed new K04/K08 witness or valid full key. Avoid publishing a duplicate six-of-eight 'new result' or inventing a source repair. Six accepted components remain the only canonical candidate. Any real progress requires a source-anchored method and an unchanged original acceptance PASS.

## Active question

Could the current *local* export establish an overlooked independent witness for one of K04's three unauthenticated layers (mask, logical route, selected printer media) or Emily's exact final margin? Existing exhaustive source-carrier and provenance studies are extensive; inspect their exact coverage before spending effort on another encoding grammar. Source `mail/16` has 07:49Z timestamp preceding the 18:02/18:03Z record it discusses, a known witness-status issue, not a correction rule.

No remote facility, people or devices contacted; no source or commitment altered.

## Additional independent confirmation (same invocation)

Wrote local `work/rederive.py` using only Python standard library; it parses source mail, telemetry highest revision, signed seal receipts, binary TRP2 with CRC exclusions, revision-C RC-17 strips, and final-transfer chunks, and checks each of the six original SHA-256 slot commitments. It also computes the selected K04 recorded XOR and asserts the original target rejects it. Ran this script both in the working extraction and a fresh temporary extraction of the unchanged ZIP; each printed exactly the canonical candidate (six PASS values, K04/K08 null), with K04 diagnostic 2CFF149C50E54557228E7DE60B3EB7C9. Ran the original verifier and confirmed 6 PASS + 2 MISSING / INCOMPLETE / not accepted. `/mnt/data/h17-partial-recovery.zip` contains candidate, original verifier output, log, read-only source rederive, source replay output. These are user-facing deliverables, not a new original-source witness or a novel canonical research result.

A strictly exploratory check found zero simple MD5/SHA1/SHA256/BLAKE2s digest identities between 133 printer payloads and obvious job/time/attempt identifiers; a speculative Python RNG first-row seed search 0..100000 also found zero. Those unsourced hypotheses do not justify extrapolation or promotion into `results/`. All 133 spool lines are structurally complete; only the first line is a comment. Current status remains unchanged.

## Later source-forensics and hypothesis triage

Inspected original `AGENT_PROMPT.txt`, custodian note, full `recovery-routing.json`, original `acceptance.json` and `verify.py`, K08 mails 11/14/20, K04 mail16, the complete 24-note crew text, printer tail and printer route labels, galley and maintenance logs. A direct grep over original source records locates the K04 XOR and K08 nonce only in the route transcription; other mentions add context/selection and lack independent K04 coupon integrity or final K08 wording. All three same-job RECOVER attempts are far apart in bits; no documented error-correcting relation. No evidence-supported new source witness.

Checked original ZIP member metadata via Python `zipfile`: all 43 members have `create_system=0`, `create_version=20`, `extract_version=20`, `flag_bits=0`, compression method8, `internal_attr=0`, identical `external_attr=25165824`, `volume=0`, `reserved=0`, identical export timestamp Oct4 11:40. This closes trivial variation in otherwise overlooked standard entry metadata, without establishing source completeness or excluding arbitrary steganography. Existing detailed ZIP audit covers compressed content and trailing/padding checks. Not worth a new results/ report without a substantive recovery mechanism.

Conducted only small exploratory same-job XOR parity combinations; none accepts original K04 commitment. No source instruction authorizes mixing attempts, so this is not recovery evidence. Inspected the all-file carrier scanner's raw/hex/text normalization logic; no obvious untested canonical extraction bug found.

Current user deliverable checked again: `/mnt/data/h17-partial-recovery.zip`, SHA256 `e2c2849c58195b710773fa9a5b9a9b1e8f6b523bbad1e55fbc7cbc4a0086ac43`, ZIP members CRC-good. Source original ZIP hash unchanged. Partial status disclosed to user with download and component table. Avoid additional duplicate workpacks absent changed source. Continue evidence-first source model research until the real 70-minute lease threshold.


## 19 October 2026 incarnation: new K04 cracking (~06:22 UTC onward)

Claimed with run_id `h17-a48-k04k08-new-cracking-20261019-0622Z`. Distinct from previous six-slot verification work. **Major new source-conditioned K04 discovery**, preserved in [cross-source TRP2 MT report](../../results/h17-k04-cross-source-recorder-mt-anchor.md), [reproducer](k04_recorder_bridge.py), and [broadcast](../../communications/broadcast/2026-10-19T0648Z_agent48-cross-source-recorder-mt-word-bridge.md).

Source-only printer MT19937 42-witness groups plus fixed-point inverse closure were cross-matched with all node49/event82 TRP2 control words (even non-K05-valid records are preserved bytes). Group containing spool row41 has consecutive untempered positions -623..-621 fully known; independent recorder samples seq992,203,903 reproduce their complete values, and seq993 matches 31 known bits of position -620, supplying its missing high bit. Details: positions -623/-622/-621/-620 respectively align to TRP2 record28 `9359AC1F` (32/32), record17 `BFB00270` (32/32), record72 `F2595C84` (32/32, **bad CRC**), record45 `30D78977` (31/32). Position -620 full untempered `96DF5138`. These record IDs are not sequential, so avoid assuming their recorder row/sequence order is RNG emission order. Four out of sixteen node49/event82 words match; other 72 event records omitted from this exact matching claim. Historical printer-producer relation remains an interpretation, not authenticated code.

Using Agent2's DEST 2-bit rejection sampler, two more group-relative previously unobserved 32-bit MT outputs are forced by original DEST=bench: spool row21 offset+4 = `9ACC8EED`, row22 offset+5 = `ADFF876E`; both fill a formerly unknown high bit. Row80's two immediately inferred post-payload words decode DEST=bench then row81 CLASS=LABEL, yielding conditional six-draw bridge between groups; source closure is consistent. Source-informed 20 regular-row sampler draw-floor improvements do **not** reduce prior 945..955 conditional target-start interval, nor does closure yield any of selected row129's four full/partial words across d43→44=11..21.

Local exploratory scripts currently under `/mnt/data/k04_long_seed_a48.py`, `/mnt/data/k04_cross_source_rng_a48.py`, `/mnt/data/k04_seed_phrases_a48.py`, with test log `/mnt/data/k04_a48_run.txt`. These local paths are not shared repo artifacts; critical reproducible pieces are committed as above. The bounded 2,096 source-phrase CPython string-seed trial found zero 4-word printer matches in first 5,000 outputs per seed; not generalized. The source-fingerprint experiment (2,297 other decoded 32-bit tokens) found three full matches only in TRP2 controls; a separate 31-bit partial comparison found fourth. Neither trial loaded original REC8 commitment.

**Next high-value novel attack:** infer how K05/TRP2 records were produced/shuffled relative to the MT spool stream; if an independently supported source ordering places more recorder control words into unknown MT output positions, it could bridge K04's two hidden gaps. Require a fresh held-out 32-bit source prediction. K08 remains absent as exact final-margin sentence; no source-backed new word-order clue yet. Original archive, `resources/` and acceptance unchanged. No K04/K08 original PASS.

