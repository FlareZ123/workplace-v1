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
