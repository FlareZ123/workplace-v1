# Agent 8 continuity: H-17 preserved evidence boundary

Identity claimed at 2026-10-17T21:23:38Z (mode draw 7 = normal). Increased COUNTER 7→8. Follow the original lease timestamp; do not refresh or delete until its 70-minute release threshold.

## Findings and validation

- Independently reran original ZIP `verify.py` with shared six-slot candidate. K01/K02/K03/K05/K06/K07 PASS; K04/K08 MISSING; combined INCOMPLETE, accepted false.
- Structural ZIP audit: 43 unique DEFLATE members, member CRC tests PASS, no ZIP/member comments, extras, encryption, inter-record gaps, prefix or suffix. ZIP SHA-256 a801d9b32715305b4a889e3c091a88455090a5c4bd56b6cf7f6c07ba8e4527ec. These checks exclude simple hidden bytes in standard metadata or unused file regions only; not steganography or missing external evidence.
- K08 source-grounded two-fragment composition: from six Emily-authored notes N02/N06/N10/N13/N20/N23, 1,030 unique 2–12 word spans; all ordered pairs with five connectors (" ", " and ", " while ", " as ", " when ") yielded 5,304,500 HMAC+SHA acceptance trials, no match. This is one bounded, explicit hypothesis, not an exhaustive test of all language.
- Complete raw-DEFLATE re-encoding control: all 43 extracted ZIP members re-compress *bit-for-bit identically* with Python 3.13.5 / zlib 1.3.1 `compressobj(level=6,wbits=-15)`; 43/43 exact matches, 0 differences. Check reproducibly with `results/audit_h17_zip.py`, now updated to report these counts. This weakens a covert alternate-compression hypothesis but does not authenticate originals. Repo report `results/h17-secondary-evidence-audit.md` updated; distinctive broadcast `communications/broadcast/2026-10-17T215831Z_agent8-deflate-reproduction.md` sent.
- Also committed `results/h17-missing-evidence-intake.md` enumerating original provenance needed for both missing components. The human-readable source-to-result status remains 6 PASS, 2 MISSING; no synthetic completion claimed. Local user package `/mnt/data/H17_recovery_partial_2026-10-17.zip` was atomically rebuilt with candidate, verifier output, original verifier/acceptance and derivation notes and tested CRC/content/unchanged checker.
- Additional DEFLATE-container check used zlib Z_BLOCK end-of-block data_type to count **151 unused high padding bits across the 43 members; all zero**, plus no unused compressed stream trailers. Reproducible programs are `results/audit_h17_zip.py` and `results/measure_raw_deflate_slack.c`; the C code was locally compiled and the driver run against uploaded ZIP. The measured padding-bit distribution is 0:3,1:7,2:3,3:10,4:6,5:5,6:4,7:5. This is a limited forensic negative test.
- K04 derived baseline payload A9A9DC5731A5E2AE879C47215C2559D5 XOR unchanged mask = 2CFF149C50E54557228E7DE60B3EB7C9; SHA256 11a7f606... mismatch. Added a stand-alone original-evidence K04 coupon payload checker; no new authenticated coupon has been located.

## Committed artifacts

- `results/check_h17_coupon.py`: read-only 16-byte coupon payload K04 checker (locally syntax-tested and run against original ACK; NO_MATCH).
- `results/test_h17_k08_splices.py`: read-only bounded desk-caption search; locally executed on the independent supplied ZIP and reported 5,304,500 tests, no match.
- `results/h17-secondary-evidence-audit.md`: method, scopes, reproducible counts, evidence limitations.

An attempt to link this audit from `results/README.md` encountered a concurrent 409 and a subsequent connector safety block; avoid retrying the blocked mutation without reason. The report still exists in `results/`.

## Next promising work

Only independently integrity-checked ESC-N coupon/buffer bytes or authenticated exact final keeper-caption wording can establish the unresolved K04/K08 values under the unchanged route and acceptance. Agent 3 is separately testing one complete 32-bit word corruption model and Agent 4 exhausted 0..5 bit flips; avoid duplicate blind brute force. Preserve six-slot baseline and evidence. Check messages and remote changes when useful. Do not access live facility controls or outside mailboxes.

## Continuation: 18 October 2026 (new eligible claim)
- Claimed Agent 8 again after previous lease exceeded the 100-minute eligibility threshold; new original claimed_at for **this incarnation** is `2026-10-18T09:36:46.159Z`. Do not use the old 17 October lease date for this incarnation's 70-minute check.
- Read current canonical status and the 07:42/09:17 Critic interventions. Kept K04/K08 null and avoided any duplicate six-slot replay or local-only packaging.
- Investigated a distinct bounded ZIP metadata carrier: local versus central ZIP header redundancy and member attribute variations. The original 43-member archive has **473/473 local header checks consistent** and **one central-metadata equivalence class for all 43**. Entry order is lexicographic. Disposable-copy positive controls toggling a local CRC byte and DOS-time byte were both reported as mismatches by the read-only script.
- Committed reproducible code `results/check_h17_zip_headers.py` and `results/h17-zip-header-redundancy.md`. This is evidence only against a narrow hidden carrier; it supplies neither K04 nor K08.
- Current original verifier state remains **six PASS, K04/K08 MISSING, combined INCOMPLETE, accepted false**.
- More productive future effort needs a specific source-provenance mechanism for an original coupon or exact caption. Exhaustive arbitrary mutation and new six-slot delivery packs are low priority per Critic.

## Continuation: 18 October 2026, claim 14:56:40 UTC
- Invocation mode draw 8: normal research; successfully claimed this identity via `agents/agent8/.lease.json` with run_id `85bcf823-58a4-4f1d-a6f4-b2dfab3af216`. Increased `COUNTER` from 95 to 96 before claiming.
- Reviewed current canonical `results/README.md`, K04 source-layer ambiguity, K08 nonce provenance, source-sufficiency matrix, evidence, Critic's 09:17 intervention and this identity's earlier findings. No new local authenticated witness for K04 or K08 emerged; preserve both null rather than guessing.
- Reproduced unchanged original `verify.py --candidate candidate.json --json` on the 43-member case export with the canonical six values. Expected process exit code 1 signifies incomplete acceptance: K01,K02,K03,K05,K06,K07 PASS, K04/K08 MISSING, combined INCOMPLETE, accepted false.
- Prepared **current-user-facing** local preservation package `/mnt/data/H17_recovery_20261018.zip` (46 files, 41,797 bytes, SHA256 `a0b27f5a7ffb6460538f0b8fd62392b60a52e809d5abde2d12f5a00687330f6d`), with original evidence/verifier, candidate, verifier result and derivation notes. Unlike repeated transient research packaging, this was for the actual user handoff; the path is invocation-local, not a persistent shared research result.
- Original ZIP SHA256 independently measured `a801d9b32715305b4a889e3c091a88455090a5c4bd56b6cf7f6c07ba8e4527ec`, matching preservation manifest. Source-selected K04 XOR `2CFF149C50E54557228E7DE60B3EB7C9` still fails; K08 final phrase still unquoted. All original source evidence remains unchanged.
- No substantive new source hypothesis or accepted value is asserted by this continuation. Future researcher should seek a discriminating local historical witness or transformation; avoid another general brute-force, carrier, or six-slot replay merely for activity.

## Focused source audit: omission markers (18 October)
- The custodian explicitly says identifiable textual export gaps were marked, while warning that unmarked omissions remain possible. Wrote and locally ran a read-only 43-member census on the original ZIP, then committed the reproducer and report to results/check_h17_explicit_gap_markers.py and results/h17-explicit-gap-marker-census.md.
- Observed 42 UTF-8 members; 15 lines explicitly declaring omission: 2 mail quoted-repeat policies, 1 maintenance notebook page-gap marker, 12 RC-17 supporting-instruction/signature omission notices. Counted 288 literal [censored] redaction tokens, one nonredaction bracket marker in evidence/ (the maintenance note), zero literal three-dot ellipses. Neither selected K04 printer row nor K08 crew/mail content has an explicit marked gap under these rules.
- This narrows only *visible* omission signalling. It does not establish source completeness, recover bytes/words, or change 6 PASS / 2 MISSING. No broad blind candidate work was undertaken.
