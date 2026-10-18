# Agent 27: H-17 source replay and custodial handoff

Claimed 2026-10-18T01:14:20.187Z. Objective is archive records reconstruction only. User explicitly requested no Work mode.

## Work performed
- Confirmed primary `resources/README` scope and original 43-member case ZIP. This invocation had an identical uploaded ZIP extracted locally for a completely independent standard-library replay; the original archive was untouched.
- Implemented a fresh read-only replay of K01, K02, K03, K05, K06, K07 from their original evidence selectors, including telemetry filtering, receipt revision rules, recorder CRC, procedure revision and transfer retries. Each value matched the original `acceptance.json` slot SHA-256; original unmodified `verify.py` reported six PASS, K04/K08 MISSING, combined INCOMPLETE, accepted false.
- K04: independently selected incident-date ESC-N => PS-261003-0417; last acknowledged RECOVER attempt 2; printed 16-byte payload A9A9DC5731A5E2AE879C47215C2559D5 XOR mask yields 2CFF149C50E54557228E7DE60B3EB7C9, SHA256 11a7f6064781a6ac7678dc6dd24759af95981c8a927f8da4436515354d34549b, not original target 930a52a1bab97ca2966332137c99e99298ea6182fb32ab63a3421dfb4fd8c9e0.
- K08: independently checked N02/N06 draft captions and N17/N18 alternative-envelope labels against recorded HMAC nonce and SHA-256 commitment. All rejected. N23/mail/11/mail/20 describe final personal caption without authenticating exact words.
- Prepared a user handoff package locally with candidate.json, unchanged verifier output, read-only independent six-slot replay, replay output, source derivation notes. Local package SHA256 may be determined by next user execution; package is not a GitHub repository artifact.

## Primary conclusion
No new authenticated K04 coupon or K08 phrase was found. Retain the six accepted slots unchanged and null for both missing slots. The determinant accepted K04 check fails; extraction ACK is not payload-integrity proof. Do not derive a valid eight-slot key from guessed original bytes or wording.

## Sources and follow-up
- Canonical existing repository synthesis: `results/README.md`, `results/h17-recovery.md`, `results/h17-source-sufficiency-matrix.md`, `results/h17-evidence-audit.md`, `results/replay_h17.py`.
- The 43-source-member ZIP has a preservation SHA256 a801d9b32715305b4a889e3c091a88455090a5c4bd56b6cf7f6c07ba8e4527ec. Case `acceptance.json` SHA256 681739241b757b471acca4c0fef9d9d97e9493883887736d5db3b92bfb0c137f; `verify.py` SHA256 01cedbfa08a28b388f8ab09b96c9c562a920d8ae9a7cc582ba3c79d138681cd0.
- Useful future advance requires a source-anchored discriminating local mechanism for missing printer original/keeper verbatim caption. Avoid fresh arbitrary mutation/HMAC grammar expansion without provenance.

## New incarnation: 18 October 2026, 17:07 UTC onward

- Claimed this existing identity at `2026-10-18T17:07:35.787Z` (run `h17-agent27-20261018-sourcescan-a8fc`), via committed GitHub lease claim. Original lease timestamp remains fixed; compare actual UTC at future checkpoints.
- Read current root README and full public `results/README.md`, selected Critic communications, existing source-sufficiency and K04/K08 search reports, and freshly inspected the original supplied 43-member ZIP. The source ZIP SHA256 was independently measured as `a801d9b32715305b4a889e3c091a88455090a5c4bd56b6cf7f6c07ba8e4527ec`.
- Fresh-extracted original unmodified verifier against the canonical six known components returned exactly six PASS, K04/K08 MISSING, combined INCOMPLETE and accepted=false (exit 1). The K04 incident selected ACK and transcribed mask remain a hard original-hash NO_MATCH; the K08 signed exact margin remains unquoted. No complete accepted candidate was found.
- Avoided duplicating previously exhaustive source-window alternate-mask tests, retry mosaics, K08 note-span grammars, and printer bit/byte brute force. Reviewed `k04-three-byte-scan.c` and `k04-four-nibble-scan.c` source for index-loop/checking soundness; observed no obvious logical gap, though did not independently rerun their billion-scale scans. A quick local exploratory test of obvious 128-bit affine and SplitMix64 sequential RNG models for the 128 regular spool payloads found no fit (neither a source-grounded generation model nor public result).
- GitHub repository currently has only `main` and no issues. Existing public source-history and manifest audits already show no additional retained original K04 coupon or K08 final caption within permitted repository/ZIP locations. Prioritize a concrete local witness/transformation if found, with untouched per-slot and combined acceptance. Do not publish redundant negative sweeps or fabricate missing components.

## Reproducibility repair checkpoint, 18 October 2026 ~17:26 UTC

- Audited all 45 Markdown documents under root README and `results/` using the remote recursive Git tree as the reference set: exactly one broken relative link, `results/h17-zip-deflate-padding.md` -> `check_h17_zip_deflate_padding.py`; this problem was already identified by Agent 25 and acknowledged in Agent 13 memory.
- Implemented the absent read-only **pure-standard-library RFC 1951 DEFLATE parser** at `results/check_h17_zip_deflate_padding.py`; tested before pushing and confirmed remote source blob SHA1 `ab75ef26b207730b475950a4308d77e9fd371fd7`. Commit `f61753325e9c904081265dd2348f452dc283ccdf` repairs the existing report's broken link without rewriting original evidence or the report.
- Original ZIP audit output exactly matches published report: 43 source members, 43 blocks (42 dynamic/1 fixed), padding-bit counts [3,7,3,10,6,5,4,5] for unused-bit sizes 0..7 (151 total), every padding value zero; positive control mutating first stream's unused high bit yields padding value 4 without changing decompressed source bytes. All 180 synthetic zlib compressed samples spanning stored/fixed/dynamic, multiple-block streams and diverse lengths decoded with correct lengths. SHA1 Git blob of local test source matched remote readback, so reproducibility repair is verified.
- Sent targeted notification to report author Agent 13 at `communications/agent13/20261018T172614Z_agent27-deflate-reproducer-restored.md`, commit `4db6d90d6ee7b2d97319e7619521ff247b3d010f`. No K04/K08 value found. Source ZIP/commitments unchanged. Return attention to source-bearing missing-slot mechanisms; this infrastructure patch should not be advertised as recovery-key progress.
